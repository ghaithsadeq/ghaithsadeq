# -*- coding: utf-8 -*-
"""Build transparent stamp PDFs (Tajawal, embedded) for overlaying the
participant's name onto the already-rendered deliverables."""
import subprocess, sys, os
CH = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FONTS = open("build/fonts.css", encoding="utf-8").read()
NAME = "غيث صادق كيوان"

TPL = """<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<style>{fonts}
@page{{size:{size};margin:0}}
html,body{{margin:0;padding:0;width:{w}pt;height:{h}pt;font-family:'Tajawal',sans-serif}}
.l{{position:absolute;left:0;right:0;text-align:center;white-space:nowrap}}
</style></head><body>{body}</body></html>"""

def build(out, size, w, h, lines):
    body = "".join(
        '<div class="l" style="bottom:%spt;font-size:%spt;font-weight:%s;color:%s;letter-spacing:%s">%s</div>'
        % (b, fs, fw, col, ls, txt) for (b, fs, fw, col, ls, txt) in lines)
    html = TPL.format(fonts=FONTS, size=size, w=w, h=h, body=body)
    src = "build/_stamp.html"
    open(src, "w", encoding="utf-8").write(html)
    subprocess.run([CH, "--headless", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", "--virtual-time-budget=4000",
                    "--print-to-pdf=" + out, "file://" + os.path.abspath(src)],
                   check=True, capture_output=True)
    print("built", out, os.path.getsize(out), "bytes")

A4 = ("A4", 595.28, 841.89)
A2 = ("420mm 594mm", 1190.55, 1683.78)

# (bottom_pt, font_pt, weight, color, letter-spacing, text)
build("build/stamp-a4-light.pdf", *A4, lines=[
    (30.5, 6.5, 700, "#64748B", ".2pt", "إعداد وتقديم: " + NAME)])
build("build/stamp-a4-cover.pdf", *A4, lines=[
    (76, 10.5, 700, "#FBBF24", ".3pt", "إعداد وتقديم: " + NAME)])
build("build/stamp-a2-poster.pdf", *A2, lines=[
    (96, 19, 700, "#FBBF24", ".4pt", "إعداد وتقديم: " + NAME)])
