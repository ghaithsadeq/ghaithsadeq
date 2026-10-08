# -*- coding: utf-8 -*-
import os, re, sys

P = "build/final/Nasaq-v2-INDEX.html"
DIR = "pkg/Nasaq-v2-Final"
NAME = "غيث صادق كيوان"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    got = s.count(old)
    if got != n:
        print("!! expected %d got %d for: %s" % (n, got, old[:70])); sys.exit(1)
    s = s.replace(old, new)

rep("<title>نَسَق v2 · فهرس المرحلة الثانية</title>",
    "<title>نَسَق v2 · الحزمة النهائية</title>")

rep("<h1>نَسَق<span class=\"v2\">v2</span> · حزمة المرحلة الثانية</h1>",
    "<h1>نَسَق<span class=\"v2\">v2</span> · الحزمة النهائية</h1>")

rep('<div class="s">من نموذجٍ يعمل… إلى أداةٍ تُستخدَم · GEN CODE TEAM · ' + NAME + ' · مدرسة السدرة الخاصة — كلباء</div>',
    '<div class="s">من نموذجٍ يعمل… إلى أداةٍ تُستخدَم · إعداد وتقديم: '
    '<b style="color:#FBBF24;font-weight:800">' + NAME + '</b> · GEN CODE TEAM · مدرسة السدرة الخاصة — كلباء</div>')

rep('<div class="st"><b>04</b>اعرضوا بالعرض التفاعلي مع نصّ الإلقاء.</div>',
    '<div class="st"><b>04</b>اطبعوا البوستر A2 وخطّة الجاهزية، واعرضوا بالعرض التفاعلي مع نصّ الإلقاء.</div>')

CARDS = (
 '<a class="c" href="Nasaq-v2-Poster-A2.pdf"><div class="im ic">🖼️</div><div class="b">'
 '<div class="r"><b>🖼️ بوستر A2 · v2</b><span class="bd">للطباعة</span></div>'
 '<p>بوستر مقاس A2 جاهز للطباعة: المشكلة، المحرّك، الجديد في v2، النتائج المقاسة، وخطوات التحقّق — ومعه نسخة PNG.</p>'
 '<div class="f"><span>Nasaq-v2-Poster-A2.pdf</span><span>SZ:Nasaq-v2-Poster-A2.pdf</span></div></div></a>'
 '<a class="c" href="Nasaq-User-Guide.pdf"><div class="im ic">📙</div><div class="b">'
 '<div class="r"><b>📙 دليل المستخدم</b></div>'
 '<p>كيف يستخدم فريق المدرسة البرنامج خطوةً بخطوة: الإعداد، التوليد، التعديل، التصدير، ومعالجة الغياب.</p>'
 '<div class="f"><span>Nasaq-User-Guide.pdf</span><span>SZ:Nasaq-User-Guide.pdf</span></div></div></a>'
 '<a class="c" href="Nasaq-Report-EN.pdf"><div class="im ic">🇬🇧</div><div class="b">'
 '<div class="r"><b>🇬🇧 التقرير بالإنجليزية</b></div>'
 '<p>النسخة الإنجليزية من التقرير التقني، لمحكّم يفضّل الإنجليزية. (محتوى المرحلة الأولى.)</p>'
 '<div class="f"><span>Nasaq-Report-EN.pdf</span><span>SZ:Nasaq-Report-EN.pdf</span></div></div></a>')
# insert the new cards just before the grid's closing tag
GRID_END = '</div></a></div>\n<div class="h">'
rep(GRID_END, '</div></a>' + CARDS + '</div>\n<div class="h">')

rep('ضعوا كلّ الملفّات في مجلّد واحد حتى تعمل روابط هذا الفهرس.',
    'ضعوا كلّ الملفّات في مجلّد واحد حتى تعمل روابط هذا الفهرس. '
    'لم تُستورَد بعد بيانات مدرسةٍ حقيقية — ما جُرِّب هو مدرسة افتراضية مختلفة الحجم لإثبات أنّ المحرّك غير مرتبطٍ ببيانات العرض.')

rep('<footer><span>نَسَق v2 · GEN CODE TEAM · ' + NAME + '</span>',
    '<footer><span>نَسَق v2 · إعداد وتقديم: ' + NAME + ' · GEN CODE TEAM · 2026</span>')

# real file sizes
def human(n):
    return "%.0f KB" % (n/1024) if n < 1024*1024 else "%.1f MB" % (n/1024/1024)
for fn in sorted(os.listdir(DIR)):
    s = s.replace("SZ:" + fn, human(os.path.getsize(os.path.join(DIR, fn))))
for m in re.finditer(r'<span>([A-Za-z0-9.\-]+\.(?:html|pdf|pptx|csv|mp4|png))</span><span>([^<]+)</span>', s):
    fn, shown = m.group(1), m.group(2)
    p = os.path.join(DIR, fn)
    if os.path.exists(p):
        real = human(os.path.getsize(p))
        if real != shown:
            s = s.replace(m.group(0), m.group(0).replace("<span>%s</span>" % shown, "<span>%s</span>" % real))
            print("size fixed  %-30s %s -> %s" % (fn, shown, real))
assert "SZ:" not in s
open(P, "w", encoding="utf-8").write(s)
print("index patched:", len(s), "bytes · name mentions:", s.count(NAME))
