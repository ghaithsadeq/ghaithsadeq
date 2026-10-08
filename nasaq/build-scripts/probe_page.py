import sys, subprocess, re, os
CH="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
page=sys.argv[1]
s=open(page,encoding='utf-8').read()
probe="""<script>window.__errs=[];addEventListener('error',e=>__errs.push('error: '+(e.message||e)));
addEventListener('unhandledrejection',e=>__errs.push('rejection: '+(e.reason&&e.reason.message||e.reason)));
(function(){const ce=console.error;console.error=function(){__errs.push('console.error: '+[].join.call(arguments,' '));ce.apply(console,arguments);};})();
addEventListener('load',function(){setTimeout(function(){var p=document.createElement('pre');p.id='__probe';
p.textContent='ERRS '+JSON.stringify(__errs);document.body.appendChild(p);},600);});</script>"""
h,sep,t=s.rpartition('</body>')
out='verify/_probe.html'
open(out,'w',encoding='utf-8').write((h+probe+sep+t) if sep else s+probe)
dom=subprocess.run([CH,"--headless","--no-sandbox","--disable-gpu","--allow-file-access-from-files",
    "--virtual-time-budget=20000","--dump-dom","file://"+os.path.abspath(out)],
    capture_output=True,text=True).stdout
m=re.search(r'<pre id="__probe">(.*?)</pre>',dom,re.S)
print("%-34s %s" % (os.path.basename(page), m.group(1) if m else "NO PROBE (dom %d bytes)"%len(dom)))
