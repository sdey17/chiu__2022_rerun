"""
Build notebooks/NN_*.ipynb from the lesson scripts.

The .py files stay the single source of truth. Run this after editing a
lesson and the notebook follows; nothing has to be kept in sync by hand.

WHAT IT CONVERTS

    module docstring            -> a title markdown cell
    # ---- / # A. Heading /     -> a "## A. Heading" markdown cell
    # ---- banner comments
    print(\"\"\"...\"\"\")   (plain) -> a markdown cell  (prose, no code)
    everything else             -> code cells, in order

f-string prints stay code, because their text depends on values computed
at run time. Only the prose blocks become markdown.

Indented runs inside a prose block (tables, formulas, parameter lists)
are wrapped in fenced code blocks so markdown does not reflow them.

Usage:  python make_notebooks.py           # all lessons
        python make_notebooks.py 09        # just one
"""
import json
import os
import re
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "notebooks")

BANNER = re.compile(r"^#\s*-{20,}\s*$")
HEADING = re.compile(r"^#\s*([A-Z])\.\s+(.*)$")
PRINT_OPEN = re.compile(r'^print\("""\s*$')
PRINT_INLINE = re.compile(r'^print\("""(.*)$')


SECTION = re.compile(r"^([A-Z]\.\s+\S.*|[A-Z][A-Z ]{3,})$")
ITEM = re.compile(r"^([0-9]+|[a-z])\.\s+")


def _render_body(lines, listy=False):
    """One run of prose at a single conceptual indent level.

    Terminal prose uses indentation for three different things, and
    markdown needs each handled differently:
        paragraph text      -> plain markdown
        deeper-indented     -> a fenced block, so tables and formulas
          tables/formulas      keep their alignment
        '*' or numbered     -> real markdown lists
    """
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return ""
    base = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
    lines = [l[base:] if len(l) >= base else l for l in lines]

    if listy:
        # a QUESTIONS / EXERCISES block: items at indent 0, wrapped
        # continuation lines deeper. Join each item onto one line.
        out, cur = [], None
        for l in lines:
            if not l.strip():
                continue
            if ITEM.match(l):
                if cur:
                    out.append(cur)
                cur = "1. " + ITEM.sub("", l).strip()
            elif cur:
                cur += " " + l.strip()
            else:
                out.append(l.strip())
        if cur:
            out.append(cur)
        return "\n".join(out)

    out, run = [], []

    def flush_run():
        if not run:
            return
        if run[0].lstrip().startswith(("* ", "- ")):
            out.extend("- " + l.strip().lstrip("*- ") if l.strip().startswith(("*", "-"))
                       else "  " + l.strip() for l in run if l.strip())
        else:
            while run and not run[-1].strip():
                run.pop()
            k = min(len(l) - len(l.lstrip()) for l in run if l.strip())
            out.append("")
            out.append("```text")
            out.extend(l[k:] for l in run)
            out.append("```")
            out.append("")
        run.clear()

    for l in lines:
        if l.startswith("  ") and l.strip():
            run.append(l)
        elif run and not l.strip():
            run.append(l)                       # blank inside a block
        else:
            flush_run()
            out.append(l)
    flush_run()
    return "\n".join(out).strip()


def prose_to_markdown(text):
    """Split a prose block at its own headings, then render each part.

    The lesson text carries headings at column 0 ('C. What the second
    compartment bought you', 'QUESTIONS') with the body indented under
    them. Dedenting the whole block at once mistakes that body for
    preformatted text, so split first and dedent each part separately.
    """
    text = text.strip("\n").rstrip()
    parts, head, body = [], None, []
    for line in text.split("\n"):
        if SECTION.match(line.rstrip()):
            parts.append((head, body))
            head, body = line.strip(), []
        else:
            body.append(line)
    parts.append((head, body))

    out = []
    for head, body in parts:
        listy = False
        if head:
            listy = head.isupper()
            label = head.title() if head.isupper() else head
            out.append(f"### {label}")
        rendered = _render_body(body, listy=listy)
        if rendered:
            out.append(rendered)
    return "\n\n".join(out).strip()


def docstring_to_markdown(doc):
    """First line becomes an H1; 'Run: python ...' is dropped."""
    lines = doc.strip("\n").split("\n")
    title = lines[0].strip().rstrip(".")
    title = re.sub(r"^LESSON (\d+)\s*--\s*", r"Lesson \1 — ", title)
    body = "\n".join(lines[1:])
    body = re.sub(r"\nRun:\s+python[^\n]*\n?", "\n", body)
    return f"# {title}\n\n{prose_to_markdown(body)}".rstrip()


def as_source(text):
    """nbformat concatenates a source list verbatim, so every line but
    the last must carry its own newline. Forgetting this silently runs
    the whole cell onto one line."""
    lines = text.split("\n")
    return [l + "\n" for l in lines[:-1]] + [lines[-1]]


def cells_from(path):
    src = open(path).read()
    lines = src.split("\n")
    cells, code = [], []

    def flush():
        body = "\n".join(code).strip("\n")
        code.clear()
        if body.strip():
            cells.append({"cell_type": "code", "metadata": {},
                          "execution_count": None, "outputs": [],
                          "source": as_source(body)})

    def md(text):
        if text.strip():
            cells.append({"cell_type": "markdown", "metadata": {},
                          "source": as_source(text)})

    i = 0
    # module docstring
    if lines[0].startswith('"""'):
        j = 1
        while not lines[j].rstrip().endswith('"""'):
            j += 1
        md(docstring_to_markdown("\n".join(lines[1:j])))
        i = j + 1

    dedent_rest = False
    while i < len(lines):
        raw = lines[i]
        line = raw[4:] if dedent_rest and raw.startswith("    ") else raw

        # `if __name__ == "__main__":` -- unwrap, a notebook is always main
        if raw.strip().startswith('if __name__'):
            flush()
            dedent_rest = True
            i += 1
            continue

        # banner comment block around a section heading
        if BANNER.match(line.strip()):
            j, heading = i + 1, None
            while j < len(lines):
                cand = lines[j][4:] if dedent_rest and lines[j].startswith("    ") else lines[j]
                if BANNER.match(cand.strip()):
                    break
                m = HEADING.match(cand.strip())
                if m:
                    heading = m
                j += 1
            if heading and j < len(lines):
                flush()
                md(f"## {heading.group(1)}. {heading.group(2)}")
                i = j + 1
                # drop the print() that merely repeats this heading
                nxt = lines[i].strip() if i < len(lines) else ""
                if nxt.startswith(f'print("{heading.group(1)}.'):
                    i += 1
                continue

        # a plain triple-quoted print: prose, so make it markdown
        stripped = line.strip()
        if PRINT_OPEN.match(stripped) or (
                PRINT_INLINE.match(stripped) and not stripped.startswith('print(f')):
            j, body = i, []
            first = PRINT_INLINE.match(stripped)
            if first and first.group(1):
                body.append(first.group(1))
            j += 1
            while j < len(lines) and '"""' not in lines[j]:
                body.append(lines[j])
                j += 1
            if j < len(lines):
                tail = lines[j].split('"""')[0]
                if tail.strip():
                    body.append(tail)
                flush()
                md(prose_to_markdown("\n".join(body)))
                i = j + 1
                continue

        code.append(line)
        i += 1
    flush()
    return cells


def build(path):
    name = os.path.basename(path)[:-3]
    nb = {
        "cells": cells_from(path),
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python",
                           "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4, "nbformat_minor": 5,
    }
    # the notebook lives one directory down, so it must find tk.py
    nb["cells"].insert(0, {
        "cell_type": "code", "metadata": {}, "execution_count": None,
        "outputs": [],
        "source": as_source(
            "# notebooks/ sits one level down, so point at the lesson "
            "modules and data.\n"
            "# Written to be safe to re-run: it moves up only if it is "
            "not already there.\n"
            "import sys, os\n"
            "if os.path.basename(os.getcwd()) == 'notebooks':\n"
            "    os.chdir('..')\n"
            "sys.path.insert(0, os.getcwd())\n"
            "%matplotlib inline\n"
            "# Print the folder name, not the absolute path: the notebooks are\n"
            "# committed with their outputs, and a machine path would be\n"
            "# baked in and go stale.\n"
            "print('working directory:', os.path.basename(os.getcwd()))"),
    })
    for n, cell in enumerate(nb["cells"]):
        cell["id"] = f"{name}-{n:02d}"          # nbformat >= 4.5 requires ids
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, f"{name}.ipynb")
    with open(dest, "w") as f:
        json.dump(nb, f, indent=1)
        f.write("\n")
    n_md = sum(c["cell_type"] == "markdown" for c in nb["cells"])
    print(f"   {name}.ipynb  {len(nb['cells'])} cells "
          f"({n_md} markdown, {len(nb['cells']) - n_md} code)")


if __name__ == "__main__":
    want = sys.argv[1:]
    files = sorted(f for f in os.listdir(HERE)
                   if re.match(r"^\d\d_.*\.py$", f)
                   and (not want or any(f.startswith(w) for w in want)))
    print(f"building {len(files)} notebooks into notebooks/\n")
    for f in files:
        build(os.path.join(HERE, f))
