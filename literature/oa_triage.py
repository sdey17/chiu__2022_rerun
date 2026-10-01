"""
Which papers are legally free, and which genuinely need institutional access?

Queries Unpaywall for every DOI in studies.csv and splits them into:

    FREE   -- a lawful open-access copy exists; fetch it, no subscription
    NEEDS  -- genuinely paywalled; these are the ones to take to a librarian

That second list is the point. "I need access to paywalled journals" is
not an actionable request; "I need TDM access to these two titles, from
these two publishers" is.

A CAVEAT ON UNPAYWALL'S publisher FIELD
---------------------------------------
Do not trust it. Unpaywall reports the publisher of Environmental
Health Perspectives (NIEHS) as "American Chemical Society (ACS)", which
is simply wrong, and it is wrong in a way that would send you to the
wrong publisher. The DOI PREFIX is authoritative and is what this
script uses; the Unpaywall string is carried through only so you can
see the disagreement.

    10.1289 -> Environmental Health Perspectives (NIEHS)
    10.1016 -> Elsevier
    10.1021 -> American Chemical Society
    10.1136 -> BMJ

Usage:
    export UNPAYWALL_EMAIL=you@uic.edu       # the API requires one
    python oa_triage.py                      # writes oa_status.csv
"""
import os
import sys
import time

import pandas as pd
import requests

# Unpaywall asks for a contact address rather than an API key. It is not
# a secret, but it is personal, so it comes from the environment rather
# than being committed here.
EMAIL = os.environ.get("UNPAYWALL_EMAIL")
if not EMAIL:
    sys.exit("set UNPAYWALL_EMAIL first, e.g.\n"
             "    export UNPAYWALL_EMAIL=you@uic.edu")

ENDPOINT = "https://api.unpaywall.org/v2/{doi}?email=" + EMAIL

# Authoritative: the registrant prefix of a DOI identifies the publisher.
PREFIX = {
    "10.1289": "Environmental Health Perspectives (NIEHS)",
    "10.1016": "Elsevier",
    "10.1021": "American Chemical Society",
    "10.1136": "BMJ",
    "10.1002": "Wiley",
    "10.1007": "Springer Nature",
}


def publisher_of(doi):
    return PREFIX.get(str(doi).split("/")[0], "unknown (see doi prefix)")


def lookup(doi):
    try:
        r = requests.get(ENDPOINT.format(doi=doi), timeout=25)
        if r.status_code != 200:
            return dict(status=f"http {r.status_code}")
        j = r.json()
        loc = j.get("best_oa_location") or {}
        return dict(
            status="OA" if j.get("is_oa") else "closed",
            oa_status=j.get("oa_status"),          # gold/green/hybrid/bronze
            journal=j.get("journal_name"),
            publisher=publisher_of(doi),           # from the DOI prefix
            publisher_unpaywall=j.get("publisher"),   # unreliable, for contrast
            title=(j.get("title") or "")[:70],
            url=loc.get("url_for_pdf") or loc.get("url") or "",
            host=loc.get("host_type") or "",
            licence=loc.get("license") or "",
        )
    except Exception as e:
        return dict(status=f"error: {type(e).__name__}")


def main():
    df = pd.read_csv("studies.csv")
    dois = df.dropna(subset=["doi"]).drop_duplicates("doi")
    rows = []
    print(f"Checking {len(dois)} DOIs against Unpaywall\n")
    for _, r in dois.iterrows():
        info = lookup(r.doi)
        info.update(doi=r.doi, study=r.study)
        rows.append(info)
        flag = {"OA": "FREE ", "closed": "NEEDS"}.get(info["status"], "  ?  ")
        print(f"   [{flag}] {r.study:<34s} "
              f"{info.get('oa_status') or info['status']:<8s} "
              f"{str(info.get('journal'))[:38]}")
        time.sleep(0.3)                  # be polite to a free service

    out = pd.DataFrame(rows)
    out.to_csv("oa_status.csv", index=False)

    free, need = out[out.status == "OA"], out[out.status == "closed"]
    print(f"\n{'=' * 66}\nFREE ({len(free)}) -- lawful open-access copy exists:\n")
    for _, r in free.iterrows():
        print(f"   {r.study:<34s} {r.oa_status:<7s} {r.host}")
        print(f"      {r.url}")

    print(f"\nNEEDS INSTITUTIONAL ACCESS ({len(need)}):\n")
    for _, r in need.iterrows():
        print(f"   {r.study:<34s} {r.publisher}")
        print(f"      {r.journal}")

    if len(need):
        print("\nPublishers to request access from (by DOI prefix):")
        print(need.publisher.value_counts().to_string())

    disagree = out[(out.publisher.notna())
                   & (out.publisher_unpaywall.notna())
                   & (~out.apply(lambda r: str(r.publisher).split()[0].lower()
                                 in str(r.publisher_unpaywall).lower(), axis=1))]
    if len(disagree):
        print(f"\nNOTE: Unpaywall's publisher string disagrees with the DOI "
              f"prefix for {len(disagree)} of {len(out)} records.")
        print("      The DOI prefix is the one to trust. Examples:")
        for _, r in disagree.head(3).iterrows():
            print(f"        {r.journal[:40]:<42s} "
                  f"unpaywall says {r.publisher_unpaywall}")

    print("\nwrote oa_status.csv")


if __name__ == "__main__":
    main()
