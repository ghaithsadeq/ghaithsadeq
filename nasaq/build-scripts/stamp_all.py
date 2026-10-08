# -*- coding: utf-8 -*-
"""Overlay the participant credit onto every delivered PDF, in a strip measured
to be free of ink on every page, then recompress so the file barely grows."""
import os, glob, json, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from pypdf import PdfReader, PdfWriter, Transformation

SLOTS = json.load(open("build/slots.json"))
DARK_COVER = {"Nasaq-v2-Report.pdf", "Nasaq-Report-AR.pdf", "Nasaq-Report-EN.pdf"}
COVER = "build/st-cover.pdf"

for path in sorted(glob.glob("build/final/*.pdf")) + sorted(glob.glob("build/phase1/*.pdf")):
    base = os.path.basename(path)
    if base == "Nasaq-v2-Poster-A2.pdf":   # authored with the credit already in it
        continue
    body = "build/st-" + base + ".pdf"
    before = os.path.getsize(path)
    w = PdfWriter(clone_from=path)
    for i, p in enumerate(w.pages):
        s = PdfReader(COVER if (base in DARK_COVER and i == 0) else body).pages[0]
        t = Transformation().scale(float(p.mediabox.width) / float(s.mediabox.width),
                                   float(p.mediabox.height) / float(s.mediabox.height))
        p.merge_transformed_page(s, t)
        p.compress_content_streams(level=9)
    w.compress_identical_objects()
    with open(path + ".tmp", "wb") as f:
        w.write(f)
    os.replace(path + ".tmp", path)
    after = os.path.getsize(path)
    print("%-28s %2d pages  %6.0f KB -> %6.0f KB" % (base, len(w.pages), before/1024, after/1024))
