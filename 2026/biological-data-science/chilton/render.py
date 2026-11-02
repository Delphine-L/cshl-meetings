"""Compile poster.typ to poster.pdf and poster.svg with the vendored fonts only."""
import sys
from pathlib import Path

import typst

here = Path(__file__).resolve().parent
kw = dict(root=str(here), font_paths=[str(here / "fonts")], ignore_system_fonts=True)
src = str(here / "poster.typ")

for out, fmt in (("poster.pdf", "pdf"), ("poster.svg", "svg")):
    _, warnings = typst.compile_with_warnings(src, output=str(here / out), format=fmt, **kw)
    for w in warnings:
        print("warning:", w, file=sys.stderr)
    print("wrote", out)
