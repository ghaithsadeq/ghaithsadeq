# -*- coding: utf-8 -*-
import os, sys
P = "build/phase1/Nasaq-INDEX.html"
D = "build/phase1"
s = open(P, encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    got = s.count(old)
    if got != n:
        print("!! expected %d got %d :: %s" % (n, got, old[:70])); sys.exit(1)
    s = s.replace(old, new)

def human(p):
    n = os.path.getsize(os.path.join(D, p))
    return "%.0f KB" % (n/1024) if n < 1024*1024 else "%.1f MB" % (n/1024/1024)

GRID_END = '<span>Nasaq-User-Guide.pdf</span><span>211 KB</span></div></div></a></div>'
CARDS = (
 '<span>Nasaq-User-Guide.pdf</span><span>' + human('Nasaq-User-Guide.pdf') + '</span></div></div></a>'
 '<a class="c" href="Nasaq-AI-Brain-Setup.pdf"><div class="im ic">🧠</div><div class="b">'
 '<div class="r"><b>🧠 ربط عقل ذكاء اصطناعي</b><span class="bd">جديد</span></div>'
 '<p>صفحتان: كيف تربط «اسأل نَسَق» بنموذج لغة حقيقي على Cloudflare Workers AI في ٤ خطوات، '
 'وجدول يبيّن ما يخرج من جهازك عند كلّ مستوى خصوصية، وحلّ المشكلات.</p>'
 '<div class="f"><span>Nasaq-AI-Brain-Setup.pdf</span><span>' + human('Nasaq-AI-Brain-Setup.pdf') + '</span></div></div></a>'
 '<a class="c" href="Nasaq-Brain-Worker.js"><div class="im ic">⚡</div><div class="b">'
 '<div class="r"><b>⚡ كود الـ Worker</b></div>'
 '<p>ملفّ واحد تلصقه في Cloudflare فيصير «عقل» التطبيق. يحتفظ بالمفتاح عنده ولا يصل المتصفّح، '
 'ويصلح Worker مستقلّاً أو Pages Function على المسار <code>/api/ask</code>.</p>'
 '<div class="f"><span>Nasaq-Brain-Worker.js</span><span>' + human('Nasaq-Brain-Worker.js') + '</span></div></div></a></div>'
)
rep(GRID_END, CARDS)

# the app card should say the brain box exists
rep('<p>النموذج الأوّلي الكامل: توليد، صفوف، معلّمون، غياب وبديل، طاقة، قيود، ثقة رقمية، اسأل نَسَق. يعمل دون إنترنت.</p>',
    '<p>النموذج الأوّلي الكامل: توليد، صفوف، معلّمون، غياب وبديل، طاقة، قيود، ثقة رقمية، اسأل نَسَق. يعمل دون إنترنت — '
    'ومع مربّع اختياري لربط <b>عقل ذكاء اصطناعي</b> على Cloudflare.</p>')

# real sizes everywhere
for m in __import__("re").finditer(r'<span>([A-Za-z0-9.\-]+\.(?:html|pdf|pptx|csv|mp4|png|js))</span><span>([^<]+)</span>', s):
    fn, shown = m.group(1), m.group(2)
    if os.path.exists(os.path.join(D, fn)):
        real = human(fn)
        if real != shown:
            s = s.replace(m.group(0), m.group(0).replace("<span>%s</span>" % shown, "<span>%s</span>" % real))
            print("size fixed  %-28s %s -> %s" % (fn, shown, real))
open(P, "w", encoding="utf-8").write(s)
print("v1 index patched · cards:", s.count('class="c" href='))
