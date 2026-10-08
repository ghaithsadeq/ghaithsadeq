# -*- coding: utf-8 -*-
import subprocess, os
CH = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FONTS = open("build/fonts.css", encoding="utf-8").read()
NAME = "غيث صادق كيوان"

def card(out, top, size, text, color="#FBBF24", ls="1px"):
    html = ("<!doctype html><html lang=ar dir=rtl><head><meta charset=utf-8><style>%s"
            "html,body{margin:0;padding:0;width:1920px;height:1080px;background:transparent;"
            "font-family:'Tajawal',sans-serif}"
            ".c{position:absolute;left:0;right:0;top:%dpx;text-align:center;font-size:%dpx;"
            "font-weight:800;color:%s;letter-spacing:%s;text-shadow:0 2px 14px rgba(0,0,0,.65)}"
            "</style></head><body><div class=c>%s</div></body></html>" % (FONTS, top, size, color, ls, text))
    src = os.path.abspath("build/_ov.html")
    open(src, "w", encoding="utf-8").write(html)
    subprocess.run([CH, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--default-background-color=00000000", "--window-size=1920,1080",
                    "--virtual-time-budget=5000", "--screenshot=" + out, "file://" + src],
                   check=True, capture_output=True)
    print("built", out, os.path.getsize(out))

card("build/ov-intro.png", 812, 40, "إعداد وتقديم: " + NAME)
card("build/ov-outro.png", 972, 34, "إعداد وتقديم: " + NAME)
