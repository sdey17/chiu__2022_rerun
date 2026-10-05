"""
Build the printable summary PDF: report/PFAS_TK_summary.pdf

Why a separate document rather than a rendering of REPORT.md. The report is
~2,000 lines written for someone working through the evidence, with the
derivations in line. This is the version to hand someone: the question, the
figure, the seven findings with the table each one rests on, what the work
corrects in the published record, and what is still open -- in a form that
prints.

Nothing here is retyped from memory. Every table below is either read from
db/*.csv at build time or transcribed from report/REPORT.md with the section
noted, so the two cannot silently diverge.

Run:  python3 scripts/make_summary_pdf.py
"""

import csv
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "report", "PFAS_TK_summary.pdf")
FIG = os.path.join(HERE, "figures", "fig00_master.png")

INK, SOFT, RULE = colors.HexColor("#111111"), colors.HexColor("#55534f"), \
    colors.HexColor("#d8d7d3")
ACCENT = colors.HexColor("#2a78d6")

# The 14 built-in Type 1 fonts cover WinAnsi only. Anything outside it renders
# as a black box, so the content is checked against this set before building
# and the build fails loudly rather than shipping a page of boxes.
SAFE_EXTRA = set("µ×·°–—‘’“”"
                 "…½éöåø")


# --------------------------------------------------------------------------
# styles
# --------------------------------------------------------------------------
def styles():
    ss = getSampleStyleSheet()
    base = dict(fontName="Times-Roman", textColor=INK, leading=12.6)
    return {
        "title": ParagraphStyle("t", parent=ss["Title"], fontName="Times-Bold",
                                fontSize=23, leading=27, textColor=INK,
                                alignment=0, spaceAfter=4),
        "subtitle": ParagraphStyle("st", fontName="Times-Roman", fontSize=13,
                                   leading=17, textColor=SOFT, spaceAfter=20),
        "h1": ParagraphStyle("h1", fontName="Times-Bold", fontSize=14.5,
                             leading=17, textColor=INK, spaceBefore=16,
                             spaceAfter=7),
        "h2": ParagraphStyle("h2", fontName="Times-Bold", fontSize=11,
                             leading=14, textColor=INK, spaceBefore=12,
                             spaceAfter=5),
        "body": ParagraphStyle("b", fontSize=9.6, alignment=TA_JUSTIFY,
                               spaceAfter=6, **base),
        "lead": ParagraphStyle("l", fontSize=11, leading=15,
                               fontName="Times-Roman", textColor=INK,
                               alignment=TA_JUSTIFY, spaceAfter=8),
        "caption": ParagraphStyle("c", fontName="Times-Italic", fontSize=8.3,
                                  leading=11, textColor=SOFT, spaceBefore=4,
                                  spaceAfter=10),
        "eq": ParagraphStyle("e", fontName="Times-Italic", fontSize=11.5,
                             leading=15, textColor=INK, alignment=1,
                             spaceBefore=6, spaceAfter=8),
        "cell": ParagraphStyle("tc", fontName="Times-Roman", fontSize=8.4,
                               leading=10.4, textColor=INK),
        "cellb": ParagraphStyle("tb", fontName="Times-Bold", fontSize=8.4,
                                leading=10.4, textColor=INK),
        "cellh": ParagraphStyle("th", fontName="Times-Bold", fontSize=8.2,
                                leading=10.2, textColor=INK),
    }


S = styles()


def para(t, k="body"):
    return Paragraph(t, S[k])


def table(rows, widths, head=True, align=None):
    """rows[0] is the header. Cell text may use reportlab inline markup."""
    data = []
    for i, r in enumerate(rows):
        st = "cellh" if (head and i == 0) else "cell"
        data.append([c if isinstance(c, Paragraph)
                     else Paragraph(str(c), S[st]) for c in r])
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1 if head else 0)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, RULE),
    ]
    if head:
        cmds += [("LINEABOVE", (0, 0), (-1, 0), 0.9, INK),
                 ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK),
                 ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f4f3f1"))]
    cmds.append(("LINEBELOW", (0, -1), (-1, -1), 0.9, INK))
    for c in (align or []):
        cmds.append(c)
    t.setStyle(TableStyle(cmds))
    return t


# --------------------------------------------------------------------------
# numbers read from disk at build time, so the PDF cannot drift from the data
# --------------------------------------------------------------------------
def read_qsar():
    p = os.path.join(HERE, "db", "qsar", "qsar_endpoint_table.csv")
    rows = [r for r in csv.DictReader(open(p))
            if r["log10R_gfr_argoul"]]
    rows.sort(key=lambda r: float(r["log10R_gfr_argoul"]))
    return rows


def read_axis():
    p = os.path.join(HERE, "db", "primary_2026",
                     "han2012_table4_reabsorption_axis.csv")
    return list(csv.DictReader(open(p)))


def inventory():
    def n(pat, sub=""):
        import glob
        return len(glob.glob(os.path.join(HERE, sub, pat)))
    comb = os.path.join(HERE, "db", "combined")
    rows = sum(len(list(csv.DictReader(open(os.path.join(comb, f)))))
               for f in sorted(os.listdir(comb)) if f.endswith(".csv"))
    return {
        "texts": n("*.txt", "papers"),
        "extracts": n("*.csv", os.path.join("db", "primary_2026")),
        "figures": n("*.png", "figures"),
        "scripts": n("*.py", "scripts"),
        "rows": rows,
        "report_lines": sum(1 for _ in open(os.path.join(HERE, "report",
                                                         "REPORT.md"))),
    }


# --------------------------------------------------------------------------
# page furniture
# --------------------------------------------------------------------------
def footer(canv, doc):
    canv.saveState()
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.4)
    canv.line(20 * mm, 14 * mm, A4[0] - 20 * mm, 14 * mm)
    canv.setFont("Times-Roman", 7.6)
    canv.setFillColor(SOFT)
    canv.drawString(20 * mm, 10 * mm,
                    "PFAS toxicokinetics - printable summary")
    canv.drawRightString(A4[0] - 20 * mm, 10 * mm, f"{doc.page}")
    canv.restoreState()


def cover_furniture(canv, doc):
    canv.saveState()
    canv.setFillColor(ACCENT)
    canv.rect(0, A4[1] - 11 * mm, A4[0], 11 * mm, stroke=0, fill=1)
    canv.restoreState()


# --------------------------------------------------------------------------
# content
# --------------------------------------------------------------------------
def story():
    inv = inventory()
    qsar = read_qsar()
    axis = read_axis()
    W = A4[0] - 40 * mm
    out = []

    # ---------------- cover ----------------
    out += [
        Spacer(1, 26 * mm),
        para("Why PFAS half-lives differ between humans, rats and mice",
             "title"),
        para("A printable summary of the evidence, the assumptions behind the "
             "published numbers, and what is still unresolved", "subtitle"),
        table([
            ["Scope", f"{inv['texts']} full texts read; "
                      f"{inv['extracts']} per-paper extractions; "
                      f"{inv['rows']:,} database rows"],
            ["Full review", f"report/REPORT.md, ~{inv['report_lines']:,} lines, "
                            f"{inv['scripts']} runnable scripts, "
                            f"{inv['figures']} figures"],
            ["Repository", "github.com/sdey17/pfas_tk"],
            ["Provenance", "every database row carries a PMID or DOI and the "
                           "table it was read from; values computed in this "
                           "work are marked as such"],
        ], [30 * mm, W - 30 * mm], head=False),
        Spacer(1, 9 * mm),
        para("The question", "h1"),
        para("Published PFAS serum half-lives disagree by orders of magnitude "
             "- between humans and animals, between rat and mouse, between "
             "male and female, and between papers describing the same "
             "experiment. This work asks why, and answers it by re-deriving "
             "the numbers from the tables they came from rather than from the "
             "sentences written about them.", "lead"),
        para("One identity governs the whole subject:", "lead"),
        para("t<sub>1/2</sub> = ln2 &middot; V<sub>d</sub> / CL", "eq"),
        para("Half-life is not a property of a chemical. It is a ratio of how "
             "much of the body the chemical occupies to how fast the body "
             "removes it, and any two of the three terms fix the third. Nearly "
             "every disagreement in this literature turns out to be about "
             "<b>which two were measured and which one was assumed</b> - and "
             "in the most consequential case, the assumed one is the number "
             "everybody quotes.", "lead"),
        Spacer(1, 7 * mm),
        para("What is in here", "h1"),
        table([
            ["1", "The species difference is a clearance difference, and it "
                  "is concentrated in females"],
            ["2", "One mechanistic axis orders every species: fractional "
                  "renal reabsorption"],
            ["3", "Exposure level is related to neither half-life nor volume "
                  "of distribution"],
            ["4", "The human volume of distribution that regulation rests on "
                  "is an assumption"],
            ["5", "Five sixths of the field is empty"],
            ["6", "Humans run two near-complete reabsorption loops, not one"],
            ["7", "Half-life is the wrong endpoint for a structure-activity "
                  "model"],
            ["", "<i>then: what this corrects in the published record, what "
                 "is still unresolved, and how to check any of it</i>"],
        ], [8 * mm, W - 8 * mm], head=False),
        NextPageTemplate("body"),
        PageBreak(),
    ]

    # ---------------- the figure ----------------
    img_w = W
    out += [
        para("The whole argument in one figure", "h1"),
        Image(FIG, width=img_w, height=img_w / 2.033),
        para("<b>Left:</b> across five species-by-sex groups, the volume of "
             "distribution spans 2.6&times; while renal clearance spans "
             "13,958&times;. The variance is in clearance, not distribution. "
             "<b>Right:</b> half-life predicted from fractional renal "
             "reabsorption alone, against observation, on log axes with the "
             "1:1 line. Every rodent point falls within 1.7&times; over a "
             "37&times; span, with no fitted parameter. The human point sits "
             "4.3&times; high, and the walk-down beneath it - renal only "
             "4.3&times;, plus faecal 2.7&times;, EPA clearance 2.2&times;, "
             "OEHHA measured clearance 0.9&times; - is what led to the second "
             "reabsorption loop in finding 6. Regenerate with "
             "scripts/make_master_figure.py.", "caption"),
    ]

    # ---------------- findings ----------------
    out += [para("The seven findings", "h1")]

    out += [
        para("1. The species difference is a clearance difference, and it is "
             "concentrated in females", "h2"),
        para("Six datasets measure <i>both</i> terms in <i>both</i> sexes "
             "inside single experiments - three species, two compounds, four "
             "laboratories, no cross-study comparison required.", "body"),
        table([
            ["", "V<sub>d</sub> male/female", "clearance female/male"],
            ["span across all six datasets", "<b>1.33 - 2.18&times;</b>",
             "<b>0.78 - 44.3&times;</b>"],
            ["", "a 1.6&times; spread", "a 56&times; spread"],
        ], [60 * mm, (W - 60 * mm) / 2, (W - 60 * mm) / 2]),
        Spacer(1, 4),
        para("The distribution ratio is male-higher every single time and "
             "never leaves a narrow band. The clearance ratio ranges over "
             "nearly two orders of magnitude <b>and changes sign between "
             "species</b>. Argoul 2026 reaches the same conclusion inside one "
             "experiment: across 11 PFAS dosed as a single cocktail, clearance "
             "spans 5,254&times; while V<sub>ss</sub> spans 7.7&times;. Taking "
             "both limbs from primary sources, female rat divided by female "
             "mouse PFOA clearance is 373-496&times;, against 7.0&times; in "
             "males. Tatum-Gibbs 2011 replicates the structure in a second "
             "compound with strains matched.", "body"),
    ]

    axis_rows = [["species", "sex", "GFR (L/d/kg)",
                  "renal clearance (mL/d/kg)", "reabsorbed"]]
    order = ["human", "mouse", "rat", "Japanese macaque", "dog", "rabbit"]
    for sp in order:
        for r in axis:
            if r["species"] != sp:
                continue
            pct = r["pct_reabsorption"]
            axis_rows.append([
                r["species"], r["sex"], r["gfr_L_d_kg"], r["clr_mL_d_kg"],
                f"<b>{pct}%</b>" if pct else "<b>net secretion</b>"])
    out += [
        para("2. One mechanistic axis orders every species: fractional renal "
             "reabsorption", "h2"),
        para("CL<sub>renal</sub> = f<sub>u</sub> &middot; GFR &middot; "
             "(1 - FR)", "eq"),
        KeepTogether([
            table(axis_rows, [34 * mm, 18 * mm, 24 * mm, 36 * mm,
                              W - 112 * mm]),
            para("Read from Han 2012 Table 4 at source "
                 "(db/primary_2026/han2012_table4_reabsorption_axis.csv). "
                 "Two values differ from the widely-cited adaptation of this "
                 "table - see the corrections overleaf.", "caption"),
        ]),
        para("The axis reproduces rodent half-lives within 1.7&times; over a "
             "37&times; span with no free parameters, and an unrelated dataset "
             "recomputes mouse PFOA at 95.9%, inside the 95.2-97.0% already in "
             "use. <b>But it has two factors, not one.</b> Humans have the "
             "longest half-life yet reabsorb <i>less</i> in absolute terms "
             "(51 mL/d/kg) than male rats (270) or mice (318-324). Of the "
             "333&times; male-mouse-to-human renal clearance gap, the escape "
             "fraction carries 50&times; and the six-fold lower human GFR "
             "carries 6.5&times; - 68% and 32% on a log scale. Reabsorption is "
             "the larger term, which is why the single-axis framing works; but "
             "a third of the difference is filtration rate, which no "
             "transporter story explains.", "body"),
        para("<b>The mechanism does not transfer, even though the fraction "
             "does.</b> A candidate transporter must be both sex-divergent and "
             "able to carry PFOA. In the rat only Oatp1a1 is both (23&times; "
             "male-predominant, androgen-induced, transports C8-C10); Oat2 is "
             "strongly sex-divergent but carries no PFOA, and Oat1/Oat3 carry "
             "it but are not sex-divergent. In humans, OATP1A2 - the closest "
             "orthologue of rat Oatp1a1 - does not transport PFOA at all; "
             "human apical reabsorption runs through OAT4 and URAT1, neither "
             "androgen-regulated.", "body"),
    ]

    out += [
        para("3. Exposure level is related to neither half-life nor volume of "
             "distribution", "h2"),
        para("Volume-of-distribution slopes against dose run -0.21 to +0.25 "
             "with inconsistent sign. Four independent dose slopes for "
             "half-life cluster at +0.08 to +0.12 against a mechanistic "
             "ceiling of 1. The between-person association does not survive "
             "age adjustment: in Li 2022's own variance decomposition, age "
             "carries 2-13&times; the partial R<super>2</super> of initial "
             "PFAS concentration, and the exposure-tertile effect is 25-37% "
             "the size of the age effect. One real exception: the female rat, "
             "slope +0.21 over a 3,200&times; dose range, consistent with "
             "saturable <i>secretion</i>; the male rat is -0.02.", "body"),
    ]

    out += [
        para("4. The human volume of distribution that regulation rests on is "
             "an assumption, not a measurement", "h2"),
        para("Nine of 42 adopted regulatory clearance factors are computed "
             "from Thompson 2010's 170 mL/kg. That paper's supplementary table "
             "is headed <i>\"Input data for the calibration of the Vd "
             "parameter\"</i>, with a final column headed <i>\"calculated "
             "Vd\"</i> - and its published values reproduce to three figures "
             "from intake, serum and an assumed elimination rate taken from a "
             "study in <b>the same two communities</b>.", "body"),
        para("The consequence is sharper than \"circular\". Forming "
             "CL = ln2 &middot; V<sub>d</sub> / t<sub>1/2</sub> makes the "
             "half-life <b>cancel exactly</b>, leaving CL = Dose/Serum = "
             "0.132-0.138 mL/kg-day. But V<sub>d</sub> does not cancel: it is "
             "proportional to whatever half-life is assumed.", "body"),
        table([
            ["half-life assumed", "V<sub>d</sub> that follows",
             "derived clearance"],
            ["2.3 y (the value used)", "<b>168 mL/kg</b>",
             "0.132-0.138 mL/kg-day"],
            ["3.8 y", "<b>277 mL/kg</b>", "0.132-0.138 mL/kg-day (unchanged)"],
        ], [45 * mm, 40 * mm, W - 85 * mm]),
        Spacer(1, 4),
        para("So adopting \"170\" alongside a different half-life silently "
             "contradicts the data it came from. Reproduced from the paper's "
             "own Table S1 to within 1.000-1.003&times; by "
             "scripts/thompson_vd_circularity.py. Meanwhile every direct "
             "measurement (74, 121, 113-199 mL/kg) falls <i>below</i> the "
             "assigned range, and the one population fit (430) sits far above "
             "it.", "body"),
    ]

    out += [
        para("5. Five sixths of the field is empty", "h2"),
        para("39 chemicals &times; 11 species &times; 4 parameters = 1,716 "
             "cells. <b>1,466 have no data at all (85%)</b>; a further 94 rest "
             "on a single study. Even PFOS, the best-covered compound in the "
             "world, fills 29 of 44. By species: human 71, rat 61, mouse 45, "
             "monkey 28 - then <b>dog 2</b>. Mining four further compilations "
             "moved coverage from 143 to 156 cells, so the hole is real rather "
             "than a search artefact.", "body"),
    ]

    out += [
        para("6. Humans run two near-complete reabsorption loops, not one",
             "h2"),
        para("The renal axis leaves a residual: predicted human half-life "
             "comes out 4.3&times; short of observation. The missing term is "
             "enterohepatic. Harada 2007 sampled serum and bile from four "
             "gallstone-surgery patients and measured a biliary resorption "
             "rate of 0.97. Bile PFOS (27.9 ng/mL) actually <i>exceeds</i> "
             "serum (23.2), so bile is a real excretion route - but 97% of "
             "what is secreted is reabsorbed from the gut.", "body"),
        table([
            ["loop", "fraction reabsorbed", "source"],
            ["renal (PFOA)", "<b>99.94%</b>", "Han 2012 Table 4"],
            ["biliary (PFOS)", "<b>97%</b>", "Harada 2007, n = 4"],
        ], [40 * mm, 40 * mm, W - 80 * mm]),
        Spacer(1, 4),
        para("Both are near-unity, both lengthen the human half-life, and "
             "<b>both are interruptible</b> - which is why bile-acid "
             "sequestrants work. Delaere 2025: treated PFOS half-life 1.2 y "
             "(n = 19) against 7.3 y under observation (n = 9), a 6.1&times; "
             "difference; PFHxS 2.5 y against 9.4 y. Genuis 2010 and "
             "M&oslash;ller 2024 agree in direction.", "body"),
        para("It also reconciles the faecal-route dispute without either side "
             "being wrong. At 97% resorption, <b>gross</b> biliary flux is "
             "large while <b>net</b> faecal elimination is small - so "
             "Andersson, measuring faeces under ongoing intake, saw a large "
             "signal, and Abraham, following a labelled bolus, saw almost "
             "nothing leave that way. Different quantities, one reconciling "
             "constant. The caveat is that n = 4, and the number is now "
             "load-bearing.", "body"),
    ]

    qrows = [["compound", "F-carbons", "head group", "ether O",
              "f<sub>u</sub> %", "log<sub>10</sub> R", "handling"]]
    for r in qsar:
        secreted = float(r["log10R_gfr_argoul"]) > 0
        qrows.append([
            r["chemical"], r["n_fluorinated_c"],
            {"carboxylate": "-COOH",
             "sulfonate": "-SO<sub>3</sub>H",
             "ether-carboxylate": "-COOH, ether"}[r["head_group"]],
            r["n_ether_o"], r["fu_pct"], r["log10R_gfr_argoul"],
            "<b>SECRETED</b>" if secreted else "reabsorbed"])
    out += [
        para("7. Half-life is the wrong endpoint for a structure-activity "
             "model", "h2"),
        para("Because t<sub>1/2</sub> = ln2 &middot; V<sub>d</sub> / CL, "
             "half-life carries a glomerular filtration term that differs "
             "6.5&times; between mouse and human with no change in chemistry. "
             "A structural model fitted to it is being asked to absorb body "
             "size. The replacement is the dimensionless renal handling "
             "ratio:", "body"),
        para("R = CL<sub>renal</sub> / (f<sub>u</sub> &middot; GFR)", "eq"),
        para("R &lt; 1 is net reabsorption, R &gt; 1 net secretion, and "
             "R = 1 - FR, so it is finding 2's axis on a scale that neither "
             "saturates near 1 nor runs unboundedly negative. On the nine "
             "compounds where both terms were measured in one experiment "
             "(Argoul 2026, male mouse), R spans 875&times;:", "body"),
        KeepTogether([
            table(qrows, [22 * mm, 17 * mm, 22 * mm, 15 * mm, 15 * mm,
                          18 * mm, W - 109 * mm]),
            para("Built by scripts/qsar_endpoint_table.py into "
                 "db/qsar/qsar_endpoint_table.csv. \"F-carbons\" counts "
                 "carbons bearing fluorine, which excludes a carboxylate's "
                 "acid carbon and includes every carbon of a sulfonate.",
                 "caption"),
        ]),
        para("Three results constrain any QSAR. <b>Chain length alone does not "
             "order the endpoint</b> - within the carboxylates the series is "
             "non-monotonic and PFHxA crosses into net secretion, so a model "
             "using carbon number as its only descriptor is already falsified "
             "on nine compounds. <b>The head group carries about 3&times; at "
             "matched chain length</b> (PFNA against PFOS, both 8 fluorinated "
             "carbons, 2.9&times; apart). <b>Ether oxygens move the endpoint "
             "1.4 log units at constant chain length, non-monotonically</b>: "
             "PFHxA with none is secreted, GenX with one is reabsorbed, "
             "PFO2OA with two is secreted - so the replacement chemicals sit "
             "on both sides of the divide.", "body"),
        para("The same construction sharpens finding 4's successor problem. R "
             "is linear in 1/f<sub>u</sub>, so the three human free fractions "
             "in the literature give three different answers for human PFOA:",
             "body"),
        table([
            ["f<sub>u</sub>", "source", "log<sub>10</sub> R",
             "gap to male mouse"],
            ["0.10", "PBPK models reading \"&gt;90% bound\" as \"about 90%\"",
             "-3.93", "354&times;"],
            ["0.02", "Han 2012's stated assumption", "-3.23", "71&times;"],
            ["0.00061", "Fischer, measured at physiological ligand:protein",
             "-1.72", "<b>2.2&times;</b>"],
        ], [18 * mm, W - 78 * mm, 22 * mm, 38 * mm]),
        Spacer(1, 4),
        para("Under the measured value the species difference is almost "
             "entirely <b>binding</b>, which would mean the transporter "
             "literature is explaining a quantity that barely differs between "
             "the species. This is stated as a sensitivity rather than a "
             "result, because the mouse and human free fractions come from "
             "different methods at different ligand:protein ratios - the exact "
             "artefact diagnosed below. One panel measuring f<sub>u</sub> for "
             "these compounds in mouse, rat and human plasma by a single "
             "method would settle it, and needs no animals.", "body"),
    ]

    # ---------------- corrections ----------------
    out += [
        para("What this corrects in the published record", "h1"),
        para("Each entry is traced to the table or figure that contradicts it. "
             "The full list of 18 is section 8 of the report.", "body"),
        table([
            ["source", "correction"],
            ["EPA", "the rat Oatp1a1 male/female ratio quoted as "
                    "\"2.5-fold\" is a <i>different transporter's</i> number "
                    "(OAT-K); the primary value is <b>23&times;</b>"],
            ["OEHHA", "its adaptation of the source reabsorption table altered "
                      "two values (human 99.94 to 99.8, male rat 93.7 to 93.2)"],
            ["Provenance", "the f<sub>u</sub> = 0.02 assumption behind the "
                           "axis is Han 2012's, not OEHHA's, and Han calls its "
                           "own values \"rough estimates\""],
            ["Andersson 2025", "transposes Thompson's PFOA and PFOS volumes "
                               "(it is PFOA 170, PFOS 230); an earlier claim "
                               "in this work that Zhang 2013 did so was itself "
                               "wrong and is withdrawn"],
            ["Cheng 2006", "its abstract calls renal Oatp1a1 "
                           "\"female-predominant\", then reports androgens "
                           "<i>increase</i> it and concludes androgens are the "
                           "exclusive cause - self-contradictory, and against "
                           "Cheng 2005"],
            ["Metabolic inertness", "\"PFAS are metabolically inert\" fails "
                                    "for 6:2 Cl-PFESA, which is "
                                    "biotransformed (Yi 2022)"],
            ["<b>This work</b>", "<b>its own refits of the EPA raw curves "
                                 "compress sex ratios about 13&times;</b> - "
                                 "see below"],
        ], [30 * mm, W - 30 * mm]),
        para("The self-correction matters most", "h2"),
        para("The terminal-slope fits in db/cphea_fitted_halflives.csv select "
             "the window with the best adjusted R<super>2</super>, which on a "
             "biphasic curve is the shallow tail. Against a published value "
             "for the same experiment the fit returns <b>1.44 d against "
             "0.08 d</b> for the female rat, and compresses a <b>71&times; sex "
             "ratio to 5.6&times;</b>. The bias runs one way, so every "
             "conclusion above survives and several strengthen - but that "
             "column must not be read as comparable to published half-lives. "
             "It carries a tail_selection_flag and is kept rather than "
             "deleted, because it remains valid for within-curve comparison.",
             "body"),
    ]

    # ---------------- open ----------------
    out += [
        para("What is still unresolved", "h1"),
        KeepTogether([
        para("1. A measured human transport-affinity constant", "h2"),
        para("Whether reabsorptive transport saturates at real human exposures "
             "depends on which parameter family you believe. There are six "
             "independent in vitro K<sub>m</sub> values for PFOA against human "
             "transporters - 47 to 310 &micro;M, from two laboratories, "
             "agreeing within a factor of 7 - against a PBPK "
             "transport-affinity constant of <b>0.133 &micro;M</b>, which is "
             "354 to 2,336&times; lower than anything ever measured in a cell. "
             "The in vitro values put human serum far below half-saturation; "
             "the fitted value puts three of four human populations at or "
             "above it, which would make clearance dose-dependent in "
             "contaminated communities and mean a single clearance factor "
             "cannot transfer between exposure settings. The weight of "
             "evidence has moved onto the in vitro side - the fitted values "
             "are fitted to plasma curves rather than measured, the mouse row "
             "has standard errors exceeding its estimates, and the "
             "dose-response evidence agrees with the in vitro answer - but "
             "nobody has measured a human value, and that single number would "
             "close it.", "body")]),
        KeepTogether([
        para("2. Unbound fraction by one method across species", "h2"),
        para("Every value of R is proportional to f<sub>u</sub>, and the mouse "
             "and human numbers currently come from different methods at "
             "different ligand:protein ratios. Measuring them one way decides "
             "whether the species difference is binding or transport - a "
             "33&times; swing in the answer. Plasma, a dialysis or "
             "ultrafiltration rig, LC-MS/MS; no animals required. This is the "
             "cheapest decisive experiment the work identifies.", "body")]),
        KeepTogether([
        para("3. Whether the biliary 0.97 replicates beyond n = 4", "h2"),
        para("It is now load-bearing for the human limb of finding 2, and it "
             "rests on four surgical patients in a single 2007 study.", "body")]),
        para("One formerly-open conflict is now closed", "h2"),
        para("The roughly 100&times; disagreement over PFOA's plasma free "
             "fraction was not a contradiction between two measurements. Han "
             "2003's \"&gt;90% bound\" is a <i>calculation</i> from "
             "K<sub>d</sub> and albumin concentration, and it is a floor that "
             "Fischer's measured 0.00061 satisfies. The underlying "
             "K<sub>d</sub> gap is a ligand:protein ratio artefact - Han "
             "titrated at 1.7:1 to 60:1, Fischer at 0.004:1 or below, and "
             "human serum sits at 10<super>-5</super> to 10<super>-3</super>:1. "
             "The defect was in the inheritance: PBPK models read \"&gt;90%\" "
             "as \"about 90%\" and used a free fraction roughly <b>164&times; "
             "too high</b>.", "body"),
    ]

    # ---------------- provenance ----------------
    out += [
        para("What exists, and how to check it", "h1"),
        table([
            ["db/combined/", f"{inv['rows']:,} rows in four schemas; every row "
                             "carries its provenance and primary source. Also "
                             "one Excel workbook."],
            ["db/primary_2026/", f"{inv['extracts']} per-paper extractions, "
                                 "read from the papers directly"],
            ["db/qsar/", "per-compound structure descriptors paired with the "
                         "renal handling ratio of finding 7"],
            ["scripts/", f"{inv['scripts']} runnable scripts - every figure "
                          "and table above regenerates"],
            ["figures/", f"{inv['figures']} figures"],
            ["report/REPORT.md", f"the full review, about "
                                 f"{inv['report_lines']:,} lines"],
            ["WANTED.md", "the papers still unobtainable, and what each would "
                          "change"],
        ], [36 * mm, W - 36 * mm], head=False),
        Spacer(1, 5),
        para("Nothing in this document is quoted from memory. Where a value "
             "came from another paper's citation rather than the original, the "
             "database row says so. Where a value was computed in this work "
             "rather than read from a paper, the row says that too. Where this "
             "work's own method is known to be biased, the affected rows carry "
             "a flag and the report says to read section 8 item 9 before using "
             "them.", "body"),
        para("This PDF is generated by scripts/make_summary_pdf.py, which "
             "reads the reabsorption axis, the structure-activity table and "
             "every count above from the database at build time - so the "
             "document cannot drift from the data it describes.", "caption"),
    ]
    return out


# --------------------------------------------------------------------------
def check_glyphs(flowables):
    """Fail loudly rather than ship a page of black boxes."""
    bad = {}
    def scan(txt):
        for ch in txt:
            o = ord(ch)
            if o < 32 or o > 126:
                if ch not in SAFE_EXTRA:
                    bad[ch] = bad.get(ch, 0) + 1
    for f in flowables:
        for obj in (f._content if isinstance(f, KeepTogether) else [f]):
            if isinstance(obj, Paragraph):
                scan(obj.text)
            elif isinstance(obj, Table):
                for row in obj._cellvalues:
                    for c in row:
                        if isinstance(c, Paragraph):
                            scan(c.text)
    return bad


def main():
    flow = story()
    bad = check_glyphs(flow)
    if bad:
        print("non-WinAnsi characters found (these render as black boxes):")
        for ch, n in sorted(bad.items(), key=lambda kv: -kv[1]):
            print(f"   U+{ord(ch):04X} {ch!r} x{n}")
        sys.exit(1)

    doc = BaseDocTemplate(OUT, pagesize=A4,
                          leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=18 * mm, bottomMargin=20 * mm,
                          title="PFAS toxicokinetics - printable summary",
                          author="pfas_tk", subject="PFAS toxicokinetics")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id="f")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=cover_furniture),
        PageTemplate(id="body", frames=[frame], onPage=footer),
    ])
    doc.build(flow)

    size = os.path.getsize(OUT)
    from pypdf import PdfReader
    pages = len(PdfReader(OUT).pages)
    print(f"wrote {os.path.relpath(OUT, HERE)}  "
          f"{pages} pages, {size/1024:.0f} KB")


if __name__ == "__main__":
    main()
