#!/usr/bin/env python3
"""Resolve each citation in xlsx_source_list.csv to a PMID and DOI via NCBI
E-utilities, so every entry in the review database carries a stable identifier.

Matching is title-first (exact title search), falling back to a title+year
search. Entries that do not resolve are left blank and reported, never guessed.
"""
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "db"
SRC = DB / "xlsx_source_list.csv"
OUT = DB / "xlsx_source_list_resolved.csv"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
# NCBI allows 3 requests/second without an API key; stay under it.
PAUSE = 0.4


def get(url: str, tries: int = 4):
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=30) as fh:
                return fh.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 - transient network, retry
            if attempt == tries - 1:
                print(f"  ! giving up: {exc}", file=sys.stderr)
                return None
            time.sleep(2 ** attempt)
    return None


def esearch(term: str):
    url = f"{EUTILS}/esearch.fcgi?db=pubmed&retmode=json&retmax=5&term={urllib.parse.quote(term)}"
    raw = get(url)
    if not raw:
        return []
    try:
        return json.loads(raw)["esearchresult"].get("idlist", [])
    except Exception:  # noqa: BLE001
        return []


def esummary(pmid: str):
    url = f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={pmid}"
    raw = get(url)
    if not raw:
        return {}
    try:
        return json.loads(raw)["result"][pmid]
    except Exception:  # noqa: BLE001
        return {}


def clean_title(t: str) -> str:
    # Strip trailing parentheticals and punctuation that break exact title search.
    t = re.sub(r"\s*\([^)]*\)\s*$", "", t).strip(" .?")
    return re.sub(r"[\[\]]", "", t)


def main() -> None:
    rows = list(csv.DictReader(SRC.open()))
    out_fields = list(rows[0].keys())
    for f in ("pmid", "doi", "journal_resolved", "pubdate", "resolved_how"):
        if f not in out_fields:
            out_fields.insert(out_fields.index("raw_citation"), f)

    n_ok = 0
    for r in rows:
        title = clean_title(r["title"])
        pmid, how = "", ""
        if title:
            ids = esearch(f'"{title}"[Title]')
            time.sleep(PAUSE)
            if len(ids) == 1:
                pmid, how = ids[0], "title_exact"
            elif len(ids) > 1:
                pmid, how = ids[0], "title_exact_multi"
            else:
                # Fall back to a looser title search bounded by publication year.
                words = " AND ".join(w for w in re.findall(r"[A-Za-z0-9-]{4,}", title)[:8])
                ids = esearch(f"({words}) AND {r['year']}[pdat]")
                time.sleep(PAUSE)
                if ids:
                    pmid, how = ids[0], "title_words_year"

        doi = journal = pubdate = ""
        if pmid:
            s = esummary(pmid)
            time.sleep(PAUSE)
            journal = s.get("fulljournalname", "") or s.get("source", "")
            pubdate = s.get("pubdate", "")
            for aid in s.get("articleids", []):
                if aid.get("idtype") == "doi":
                    doi = aid.get("value", "")
            n_ok += 1

        r["pmid"], r["doi"] = pmid, doi
        r["journal_resolved"], r["pubdate"] = journal, pubdate
        r["resolved_how"] = how
        print(f"[{r['row']:>2}] {'OK ' if pmid else 'MISS'} {pmid or '-':>9}  {how:<18} {title[:62]}")

    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=out_fields)
        w.writeheader()
        w.writerows(rows)
    print(f"\nresolved {n_ok}/{len(rows)} -> {OUT}")


if __name__ == "__main__":
    main()
