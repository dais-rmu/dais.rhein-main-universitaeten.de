#!/usr/bin/env python3
"""Build the DAIS semester posters from layout.svg and the talk files.

Usage:
    poster/build_poster.py 2026-WiSe [2027-SoSe ...]   build the given semesters
    poster/build_poster.py --all                       build every semester in src/content/talks
    options: --pdf         also export an A3 PDF via Inkscape
             --a4 --a3 --a2 --a1 --a0
                       export a PDF in that paper size (implies --pdf, may be combined);
                       the file name always carries the size, e.g. ...-A3.pdf, ...-A0.pdf
             --out DIR output directory (default: poster/build)
The SVG itself is always A3; sizes only scale the PDF.

Posters up to 2025-SoSe use layout_until_2025-SoSe.svg (old RMU logo), later ones layout.svg.

Text that doesn't fit on the page is detected (via Inkscape) and you are asked for a
shorter version, e.g. "Ecole Polytechnique Federale de Lausanne" -> "EPFL Lausanne".
An answer may contain \\n (typed as backslash-n) to wrap onto two lines.
Answers are stored in poster/shortenings.yaml and reused on later runs; the talk
files are never changed. Without a terminal the build fails and lists the problems.

Requires: python3 with lxml and PyYAML; Inkscape (overflow check and --pdf); Montserrat font.
"""

import argparse
import itertools
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import yaml
from lxml import etree

sources = {}  # text element id -> unshortened text, filled by text()
shortenings = {}

HERE = Path(__file__).resolve().parent
TALKS = HERE.parent / "src" / "content" / "talks"
LAYOUT = HERE / "layout.svg"
# Posters up to this semester use layout_until_2025-SoSe.svg (older RMU logo).
LAST_OLD_LAYOUT = "2025-SoSe"
OLD_LAYOUT = HERE / "layout_until_2025-SoSe.svg"
SHORTENINGS = HERE / "shortenings.yaml"

SVG = "http://www.w3.org/2000/svg"
NS = {"s": SVG}

# Per-city rectangle colour and the location lines shown on the poster.
CITIES = {
    "darmstadt": ("#86888b", ["TU Darmstadt", "(Campus Stadtmitte)"]),
    "mainz": ("#eb193c", ["Johannes Gutenberg", "University Mainz"]),
    "frankfurt": ("#0089c9", ["Goethe University Frankfurt", "(Campus Bockenheim)"]),
}

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Geometry in mm (page is 297 x 420). The free area between header and logos is
# centred around y = 233; days are stacked there without gaps.
PAPER_MM = {"a4": (210, 297), "a3": (297, 420), "a2": (420, 594),
            "a1": (594, 841), "a0": (841, 1189)}
DEFAULT_SIZE = "a3"

PAGE_W = 297
DAY_H = 60
# Each rectangle reaches this far under the next one, so anti-aliasing in PDF
# viewers/printers can't leave a thin white line between neighbouring days.
OVERLAP = 1
CENTER_Y = 233
LEFT_X = 10
RIGHT_X = 149
TALK_PITCH = 25
NAME_LH = 9.28 * 1.25  # line heights for wrapped (multi-line) names/affiliations
AFF_LH = 7.06 * 1.25
MARGIN_RIGHT = 10  # text must end this far from the right page edge (like LEFT_X on the left)
PX_PER_MM = 96 / 25.4  # Inkscape reports bounding boxes in px

FONT = "font-family:Montserrat;fill:#ffffff;stroke:none"


def semester_key(semester):
    year, term = semester.split("-")
    return int(year), {"SoSe": 0, "WiSe": 1}[term]


def layout_for(semester):
    old = semester_key(semester) <= semester_key(LAST_OLD_LAYOUT)
    return OLD_LAYOUT if old else LAYOUT


def read_talks(semester):
    talks = []
    for path in sorted((TALKS / semester).glob("*.md")):
        m = re.match(r"---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
        if not m:
            raise ValueError(f"{path}: no front matter")
        meta = yaml.safe_load(m.group(1))
        # PyYAML parses `2026-09-18 13:00` as a datetime on its own.
        date = meta["date"]
        if not isinstance(date, datetime):
            date = datetime.strptime(str(date), "%Y-%m-%d %H:%M")
        talks.append({**meta, "date": date, "file": path.name})
    return sorted(talks, key=lambda t: t["date"])


def group_days(talks):
    days = defaultdict(list)
    for t in talks:
        days[t["date"].date()].append(t)
    return [days[d] for d in sorted(days)]


def fmt_date(d):
    return f"{WEEKDAYS[d.weekday()]}, {MONTHS[d.month - 1]} {d.day}, {d.year}"


_text_ids = itertools.count()


def text(parent, lines, x, y, size, weight, line_height=0, source=None):
    """Add a <text> with one <tspan> per line, baselines starting at y.

    `source` is the unshortened string (see shortenings.yaml); the text
    elements that have one are checked for overflow."""
    el = etree.SubElement(parent, f"{{{SVG}}}text")
    el.set("id", f"day-text-{next(_text_ids)}")
    el.set("style", f"font-size:{size}px;font-weight:{weight};{FONT}")
    if source is not None:
        sources[el.get("id")] = source
    for i, line in enumerate(lines):
        span = etree.SubElement(el, f"{{{SVG}}}tspan")
        span.set("x", f"{x}")
        span.set("y", f"{y + i * line_height:.3f}")
        span.text = line
    return el


def build_day(root, talks, top, overlap=0):
    color, location = CITIES[talks[0]["city"]]
    g = etree.SubElement(root, f"{{{SVG}}}g")
    rect = etree.SubElement(g, f"{{{SVG}}}rect")
    for k, v in dict(x=0, y=f"{top:.3f}", width=PAGE_W, height=DAY_H + overlap, fill=color).items():
        rect.set(k, str(v))

    # Left column: date and location, vertically centred in the rectangle.
    text(g, [fmt_date(talks[0]["date"])], LEFT_X, top + 24.5, 8.13, 400)
    text(g, location, LEFT_X, top + 35, 8.13, 300, line_height=10.2)

    # Right column: one block (name + affiliation) per talk. A shortening may
    # contain "\n" to wrap onto several lines; every extra line pushes the
    # following blocks down, and the whole group stays vertically centred.
    blocks = []
    for t in talks:
        name = str(t["speakerName"]).strip()
        aff = str(t.get("speakerAffiliation") or "").strip()
        blocks.append(dict(
            name=name, name_lines=shortenings.get(name, name).split("\n"),
            aff=aff, aff_lines=shortenings.get(aff, aff).split("\n") if aff else []))
    for b in blocks:
        b["extra"] = (len(b["name_lines"]) - 1) * NAME_LH + max(len(b["aff_lines"]) - 1, 0) * AFF_LH
    y = top + DAY_H / 2 - ((len(talks) - 1) * TALK_PITCH + sum(b["extra"] for b in blocks)) / 2 - 0.5
    for b in blocks:
        text(g, b["name_lines"], RIGHT_X, y, 9.28, 400, line_height=NAME_LH, source=b["name"])
        if b["aff_lines"]:
            ay = y + 8.5 + (len(b["name_lines"]) - 1) * NAME_LH
            text(g, b["aff_lines"], RIGHT_X, ay, 7.06, 300, line_height=AFF_LH, source=b["aff"])
        y += TALK_PITCH + b["extra"]


def load_shortenings():
    if SHORTENINGS.exists():
        return yaml.safe_load(SHORTENINGS.read_text(encoding="utf-8")) or {}
    return {}


def _str_representer(dumper, data):
    # multi-line answers as readable block scalars (|-) instead of quoted strings
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|" if "\n" in data else None)


yaml.add_representer(str, _str_representer, Dumper=yaml.SafeDumper)


def save_shortenings():
    header = ("# Shortened texts for the posters, asked for by build_poster.py when a text is too\n"
              "# wide. Format: \"original text\": \"short text\". Edit or delete freely.\n")
    SHORTENINGS.write_text(header + yaml.safe_dump(shortenings, allow_unicode=True, sort_keys=True),
                           encoding="utf-8")


def make_tree(semester, days):
    sources.clear()
    tree = etree.parse(str(layout_for(semester)))
    root = tree.getroot()

    # "Nx Fridays at 13-15" in the header.
    for span in root.xpath("//s:g[@id='header-when'] | //s:text[@id='header-when']//s:tspan", namespaces=NS):
        if span.text and re.match(r"\d+x Fridays", span.text):
            span.text = re.sub(r"^\d+x", f"{len(days)}x", span.text)

    # The empty group `days` in layout.svg is where the day rectangles go.
    group = root.xpath("//s:g[@id='days']", namespaces=NS)[0]
    top = CENTER_Y - len(days) * DAY_H / 2
    for i, day in enumerate(days):
        build_day(group, day, top + i * DAY_H, OVERLAP if i < len(days) - 1 else 0)
    return tree


def find_overflows(tree):
    """Return [(source text, mm too wide)] for day texts reaching past the right margin."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "check.svg"
        tree.write(str(path), xml_declaration=True, encoding="UTF-8")
        res = subprocess.run(["inkscape", "--query-all", str(path)],
                             capture_output=True, text=True, check=True)
    limit = PAGE_W - MARGIN_RIGHT
    over = {}
    for line in res.stdout.splitlines():
        id_, x, _, w, _ = line.split(",")
        if id_ in sources:
            excess = (float(x) + float(w)) / PX_PER_MM - limit
            if excess > 0.01:
                over[sources[id_]] = max(excess, over.get(sources[id_], 0))
    return sorted(over.items())


def build_poster(semester, out_dir, sizes):
    days = group_days(read_talks(semester))
    if not days:
        raise ValueError(f"no talks in {semester}")
    skipped = set()
    while True:
        tree = make_tree(semester, days)
        over = [(t, e) for t, e in find_overflows(tree) if t not in skipped]
        if not over:
            break
        if not sys.stdin.isatty():
            lines = "\n".join(f"  {t!r} is {e:.1f} mm too wide" for t, e in over)
            sys.exit(f"{semester}: text too wide, add shortenings to {SHORTENINGS} "
                     f"or run interactively:\n{lines}")
        for t, e in over:
            print(f"{semester}: {t!r} is {e:.1f} mm too wide.")
            short = input("  shorter version, \\n = line break (empty = keep as is): ").strip()
            short = short.replace("\\n", "\n")
            if short:
                shortenings[t] = short
                save_shortenings()
            else:
                skipped.add(t)
    root = tree.getroot()

    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"DAIS-Poster-{semester}.svg"
    tree.write(str(out), xml_declaration=True, encoding="UTF-8")
    print(f"wrote {out} ({len(days)} days)")
    # The SVG stays A3. For other paper sizes only the physical width/height
    # change; the viewBox (297 x 420) scales the content uniformly.
    for size in sizes:
        w, h = PAPER_MM[size]
        root.set("width", f"{w}mm")
        root.set("height", f"{h}mm")
        pdf_path = out.with_name(f"{out.stem}-{size.upper()}.pdf")
        with tempfile.TemporaryDirectory() as tmp:
            scaled = Path(tmp) / out.name
            tree.write(str(scaled), xml_declaration=True, encoding="UTF-8")
            subprocess.run(["inkscape", str(scaled), "--export-type=pdf",
                            f"--export-filename={pdf_path}"], check=True)
        print(f"wrote {pdf_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("semesters", nargs="*", help="e.g. 2026-WiSe")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--pdf", action="store_true", help=f"also export a {DEFAULT_SIZE.upper()} PDF")
    for size in PAPER_MM:
        ap.add_argument(f"--{size}", dest="sizes", action="append_const", const=size,
                        help=f"export a PDF in {size.upper()} (implies --pdf)")
    ap.add_argument("--out", type=Path, default=HERE / "build")
    args = ap.parse_args()
    shortenings.update(load_shortenings())
    semesters = sorted(p.name for p in TALKS.iterdir() if p.is_dir()) if args.all else args.semesters
    if not semesters:
        ap.error("give at least one semester or --all")
    sizes = args.sizes or ([DEFAULT_SIZE] if args.pdf else [])
    for s in semesters:
        build_poster(s, args.out, sizes)


if __name__ == "__main__":
    sys.exit(main())
