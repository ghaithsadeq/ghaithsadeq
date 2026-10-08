# -*- coding: utf-8 -*-
import sys, os
NAME = "غيث صادق كيوان"
TEAM = "GEN CODE TEAM"
HL   = '<span style="color:#FBBF24;font-weight:800">' + NAME + '</span>'
BOTH = TEAM + " · " + NAME

FILES = ["build/final/Nasaq-v2-App.html", "build/final/Nasaq-v2-Presentation.html",
         "build/final/Nasaq-v2-INDEX.html", "build/phase1/Nasaq-App.html",
         "build/phase1/Nasaq-Presentation.html", "build/phase1/Nasaq-INDEX.html"]

# applied AFTER the global pass, so they match the already-rewritten text
COVERS = {
 "build/final/Nasaq-v2-Presentation.html": [
   ('<div class="who">' + BOTH + ' · مدرسة السدرة الخاصة — كلباء</div>',
    '<div class="who">إعداد وتقديم: ' + HL + ' · ' + TEAM + ' · مدرسة السدرة الخاصة — كلباء</div>', 1),
   ('<div class="who">شكراً لكم · ' + BOTH + ' · مدرسة السدرة الخاصة — كلباء</div>',
    '<div class="who">شكراً لكم · إعداد وتقديم: ' + HL + ' · ' + TEAM + ' · مدرسة السدرة الخاصة — كلباء</div>', 1),
 ],
 "build/final/Nasaq-v2-App.html": [
   ('<div class="who">الإصدار الثاني · مولّد جداول ذكيّ للمدارس · ' + BOTH + ' · مدرسة السدرة الخاصة — كلباء</div>',
    '<div class="who">الإصدار الثاني · مولّد جداول ذكيّ للمدارس · إعداد: ' + HL + ' · ' + TEAM + ' · مدرسة السدرة الخاصة — كلباء</div>', 1),
 ],
}

for path in FILES:
    s = open(path, encoding="utf-8").read()
    n = s.count(TEAM)
    assert NAME not in s, "name already present in " + path
    s = s.replace(TEAM, BOTH)                      # global, uniform
    for old, new, cnt in COVERS.get(path, []):
        got = s.count(old)
        if got != cnt:
            print("!! mismatch", path, got, "!=", cnt, "::", old[:70]); sys.exit(1)
        s = s.replace(old, new)
    assert s.count(NAME) == n, "name count drift in " + path
    open(path, "w", encoding="utf-8").write(s)
    print("OK", os.path.basename(path), "— mentions:", n)
