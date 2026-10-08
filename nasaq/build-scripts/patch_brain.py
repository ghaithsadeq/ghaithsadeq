# -*- coding: utf-8 -*-
"""Wire the optional Cloudflare Workers AI brain into the phase-1 app."""
import sys
P = "build/phase1/Nasaq-App.html"
s = open(P, encoding="utf-8").read()
ui = open("brain/ui.html", encoding="utf-8").read()
js = open("brain/logic.js", encoding="utf-8").read()

def rep(old, new, n=1):
    global s
    got = s.count(old)
    if got != n:
        print("!! expected %d got %d :: %s" % (n, got, old[:70])); sys.exit(1)
    s = s.replace(old, new)

# 1) honest subtitle — the local engine is still the default, the brain is opt-in
rep('<p class="sub">اسأل بالعربية عن الجدول: محرّك محلّي يفهم أسماء المعلّمين والأيام والحصص والصفوف ويجيب من الجدول الحيّ مباشرة، دون إنترنت ودون مفتاح.</p>',
    '<p class="sub">اسأل بالعربية عن الجدول: محرّك محلّي يفهم أسماء المعلّمين والأيام والحصص والصفوف ويجيب من الجدول الحيّ مباشرة، دون إنترنت ودون مفتاح. '
    'ويمكنك اختيارياً ربط <b>عقل ذكاء اصطناعي</b> على Cloudflare من المربّع أسفل المحادثة.</p>')

# 2) the brain card, right after the chat card inside #v-ask
anchor = '''    <div class="chips" id="chips"></div>
  </div>
</section>

<!-- REPORT -->'''
rep(anchor, '''    <div class="chips" id="chips"></div>
  </div>
''' + ui + '''</section>

<!-- REPORT -->''')

# 3) the logic, appended to the main script so its ask() overrides the original
tail = "\n</script>\n</body>\n</html>\n"
if not s.endswith(tail):
    print("!! unexpected file ending:", repr(s[-60:])); sys.exit(1)
s = s[:-len(tail)] + js + "\nbrainLoad();brainPill();" + tail

open(P, "w", encoding="utf-8").write(s)
print("brain wired into", P, "| size", len(s))
