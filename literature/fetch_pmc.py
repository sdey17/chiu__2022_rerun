"""
Fetch open-access full text from PubMed Central and strip it to plain text.

NCBI E-utilities returns JATS XML, which keeps section headings, so the
methods can be read directly rather than guessed from the abstract.
Files land in fulltext/<PMCID>.txt.
"""
import html
import re
import sys
import time
import urllib.request

EUTILS = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
          "?db=pmc&id={}&retmode=xml")


def fetch(pmcid):
    num = pmcid.replace("PMC", "")
    with urllib.request.urlopen(EUTILS.format(num), timeout=90) as r:
        xml = r.read().decode("utf8", "ignore")
    # keep section titles as headings so the structure survives
    text = re.sub(r"<title>", "\n\n## ", xml)
    text = re.sub(r"</title>", "\n", text)
    text = re.sub(r"</(p|sec|td|tr|abstract)>", "\n", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


if __name__ == "__main__":
    for pmcid in sys.argv[1:]:
        try:
            t = fetch(pmcid)
            open(f"fulltext/{pmcid}.txt", "w").write(t)
            print(f"{pmcid}: {len(t):,} chars")
        except Exception as e:
            print(f"{pmcid}: FAILED {e}")
        time.sleep(0.5)      # be polite to NCBI
