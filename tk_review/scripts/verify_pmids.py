#!/usr/bin/env python3
"""Verify every resolved PMID by comparing the PubMed title against the
spreadsheet title, and retry the unresolved entries with an author+year query.

A fuzzy title ratio below 0.80 is treated as unverified and the PMID is dropped,
so the database never carries a confidently-wrong identifier.
"""
import csv
import difflib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "db"
SRC = DB / "xlsx_source_list_resolved.csv"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
PAUSE = 0.4
THRESHOLD = 0.80


def get(url, tries=4):
    for a in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=30) as fh:
                return fh.read().decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            if a == tries - 1:
                return None
            time.sleep(2 ** a)
    return None


def esearch(term, retmax=10):
    raw = get(f"{EUTILS}/esearch.fcgi?db=pubmed&retmode=json&retmax={retmax}"
              f"&term={urllib.parse.quote(term)}")
    if not raw:
        return []
    try:
        return json.loads(raw)["esearchresult"].get("idlist", [])
    except Exception:  # noqa: BLE001
        return []


def esummaries(pmids):
    if not pmids:
        return {}
    raw = get(f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(pmids)}")
    if not raw:
        return {}
    try:
        res = json.loads(raw)["result"]
    except Exception:  # noqa: BLE001
        return {}
    return {p: res[p] for p in pmids if p in res}


def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def ratio(a, b):
    return difflib.SequenceMatcher(None, " ".join(norm(a)), " ".join(norm(b))).ratio()


def doi_of(summary):
    for aid in summary.get("articleids", []):
        if aid.get("idtype") == "doi":
            return aid.get("value", "")
    return ""


def main():
    rows = list(csv.DictReader(SRC.open()))
    fields = list(rows[0].keys())
    for f in ("title_match_ratio", "pubmed_title"):
        if f not in fields:
            fields.insert(fields.index("raw_citation"), f)

    # Pass 1: verify what we have.
    have = [r for r in rows if r["pmid"]]
    sums = {}
    for i in range(0, len(have), 50):
        chunk = [r["pmid"] for r in have[i:i + 50]]
        sums.update(esummaries(chunk))
        time.sleep(PAUSE)

    dropped = []
    for r in have:
        s = sums.get(r["pmid"], {})
        pt = s.get("title", "")
        rr = ratio(r["title"], pt) if pt else 0.0
        r["pubmed_title"], r["title_match_ratio"] = pt, f"{rr:.3f}"
        if rr < THRESHOLD:
            dropped.append((r["row"], r["pmid"], f"{rr:.2f}", r["title"][:48], pt[:48]))
            r["pmid"] = r["doi"] = r["resolved_how"] = ""

    print(f"verified {len(have) - len(dropped)}/{len(have)}; dropped {len(dropped)} bad matches")
    for d in dropped:
        print(f"  DROP row {d[0]:>2} pmid {d[1]:>9} ratio {d[2]}\n       ours: {d[3]}\n       pm:   {d[4]}")

    # Pass 2: retry everything still unresolved, using author + year + title words.
    todo = [r for r in rows if not r["pmid"]]
    print(f"\nretrying {len(todo)} unresolved")
    for r in todo:
        au = r["first_author"]
        words = [w for w in norm(r["title"]) if len(w) > 4][:6]
        queries = []
        if au and r["year"]:
            queries.append(f"{au}[Author] AND {r['year']}[pdat]")
        if words:
            queries.append(" AND ".join(words))
        best = (0.0, "", "", "")
        for q in queries:
            for pmid, s in esummaries(esearch(q, retmax=20)).items():
                rr = ratio(r["title"], s.get("title", ""))
                if rr > best[0]:
                    best = (rr, pmid, s.get("title", ""), doi_of(s))
            time.sleep(PAUSE)
            if best[0] >= 0.92:
                break
        if best[0] >= THRESHOLD:
            r["pmid"], r["doi"] = best[1], best[3]
            r["pubmed_title"], r["title_match_ratio"] = best[2], f"{best[0]:.3f}"
            r["resolved_how"] = "author_year_retry"
            print(f"  [{r['row']:>2}] FOUND {best[1]:>9} ratio {best[0]:.2f}  {best[2][:58]}")
        else:
            r["title_match_ratio"] = f"{best[0]:.3f}"
            print(f"  [{r['row']:>2}] still missing (best ratio {best[0]:.2f})  {r['title'][:52]}")

    with SRC.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    ok = sum(1 for r in rows if r["pmid"])
    print(f"\nfinal: {ok}/{len(rows)} carry a verified PMID -> {SRC}")


if __name__ == "__main__":
    main()
