"""
Reproduce the PubMed search and screening behind studies.csv.

Run with the PubMed MCP server available. This script does the local
half: given saved metadata JSON, it screens for human studies that report
a numeric half-life and prints the sentences containing them, which is
what the extraction in studies.csv was read from.

The searches used were:
  1. (half-life[Title] OR half-lives[Title] OR elimination[Title]
      OR toxicokinetic*[Title]) AND (perfluor* OR PFAS OR PFOA OR PFOS
      OR PFHxS OR PFNA)                                    -> 199 hits
  2. (perfluoroalkyl OR PFAS OR PFOA OR PFOS OR PFHxS)
      AND (half-life OR elimination OR clearance)
      AND (serum OR plasma) AND human                      -> 224 hits
  3. author-targeted lookups for the classic cohorts
     (Olsen, Bartell, Seals, Worley, Zhang)
"""
import glob
import json
import re
import sys

HUMAN = re.compile(r'\b(human|men|women|worker|resident|firefighter|'
                   r'participant|cohort|volunteer|population)', re.I)


def screen(metadata_dir):
    arts = {}
    for f in glob.glob(f"{metadata_dir}/*get_article_metadata*.txt"):
        for a in json.load(open(f)).get("articles", []):
            arts[a["identifiers"].get("pmid")] = a
    print(f"{len(arts)} unique articles loaded\n")

    for pmid, a in sorted(arts.items(),
                          key=lambda kv: str(kv[1].get("publication_date", {}).get("year", ""))):
        abstract = a.get("abstract") or ""
        if not isinstance(abstract, str):
            abstract = " ".join(abstract)
        title = a.get("title") or ""
        if not re.search(r'half-?li', abstract + title, re.I):
            continue
        if not HUMAN.search(title + " " + abstract):
            continue
        # sentences that actually carry a number
        hits = [s.strip() for s in re.split(r'(?<=[.;]) ', abstract)
                if re.search(r'half-?li', s, re.I) and re.search(r'\d', s)]
        if not hits:
            continue
        year = a.get("publication_date", {}).get("year", "?")
        print(f"--- PMID {pmid} ({year}) doi:{a.get('doi')}")
        print(f"    {title[:110]}")
        for s in hits[:2]:
            print(f"     * {s[:270]}")


if __name__ == "__main__":
    screen(sys.argv[1] if len(sys.argv) > 1 else ".")
