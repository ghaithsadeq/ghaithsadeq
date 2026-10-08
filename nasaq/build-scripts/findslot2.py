# -*- coding: utf-8 -*-
from PIL import Image
import subprocess, os, glob, tempfile, json
DPI = 150; S = DPI / 72.0
BANDS = [("below-rule", 16, 30), ("above-rule", 40, 58), ("above-rule2", 46, 64)]
NEED = 170
OUT = {}
for f in sorted(glob.glob('build/final/*.pdf')) + sorted(glob.glob('build/phase1/*.pdf')):
    base = os.path.basename(f)
    res = {}
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(['pdftoppm', '-r', str(DPI), '-png', f, td + '/p'], check=True)
        pngs = sorted(glob.glob(td + '/p-*.png'))
        for name, b0, b1 in BANDS:
            cols = None; Wpt = None
            for png in pngs:
                im = Image.open(png).convert('L'); w, h = im.size; Wpt = w / S
                strip = im.crop((0, int(h - b1 * S), w, int(h - b0 * S)))
                sw, sh = strip.size; px = list(strip.get_flattened_data())
                if cols is None: cols = [0] * sw
                med = sorted(px)[len(px) // 2]
                for y in range(sh):
                    row = px[y * sw:(y + 1) * sw]
                    for x, v in enumerate(row):
                        if abs(v - med) > 22: cols[x] = 1
            best = (0, 0, 0); run = 0
            for x in range(len(cols) + 1):
                if x < len(cols) and cols[x] == 0: run += 1
                else:
                    if run > best[0]: best = (run, x - run, x); 
                    run = 0
            res[name] = (round(best[0]/S,1), round(best[1]/S,1), round(best[2]/S,1))
    pick = next((n for n,_,_ in BANDS if res[n][0] >= NEED), None)
    OUT[base] = dict(w=round(Wpt,1), bands=res, pick=pick)
    print("%-28s %s  -> %s" % (base, "  ".join("%s=%5.0f[%4.0f-%4.0f]"%(n,)+"" for n in []) or
          "  ".join("%s:%5.0fpt[%4.0f..%4.0f]"%(n,res[n][0],res[n][1],res[n][2]) for n,_,_ in BANDS), pick))
json.dump(OUT, open('build/slots.json','w'), indent=1)
