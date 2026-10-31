# -*- coding: utf-8 -*-
"""把自动检测的建筑/水面矩形预置进标记工具，供用户在此基础上修改。"""
import json
import io
import numpy as np
from PIL import Image
from collections import deque

ROOT = r"C:\Users\30891\Desktop\校园物志侯\gameV3"
img = Image.open(ROOT + r"\assets\map_base.png").convert("RGB")
a = np.asarray(img).astype(np.int16)
H, W = a.shape[:2]
R,G,B = a[...,0],a[...,1],a[...,2]
MX = np.maximum(np.maximum(R,G),B); MN = np.minimum(np.minimum(R,G),B); SAT = MX-MN
water = (B>=90)&(B>R+40)&(B>G+10)
building_like = ((MX>=150)&(SAT<=60)) | ((R>G+40)&(R>B+40)&(R>=70)&(MX<220))

def comps(mask, min_area, ds=2):
    m = mask[::ds, ::ds]
    h, w = m.shape
    lab = np.zeros((h,w), dtype=np.int32); cur = 0; out = []
    for y in range(h):
        for x in range(w):
            if m[y,x] and lab[y,x]==0:
                cur += 1
                q = deque([(y,x)]); lab[y,x]=cur; area=0
                miny=maxy=y; minx=maxx=x
                while q:
                    cy,cx=q.popleft(); area+=1
                    miny=min(miny,cy); maxy=max(maxy,cy); minx=min(minx,cx); maxx=max(maxx,cx)
                    for dy in (-1,0,1):
                        for dx in (-1,0,1):
                            ny,nx=cy+dy,cx+dx
                            if 0<=ny<h and 0<=nx<w and m[ny,nx] and lab[ny,nx]==0:
                                lab[ny,nx]=cur; q.append((ny,nx))
                if area >= min_area:
                    out.append((max(0,minx*ds-3), max(0,miny*ds-3), min(W-1,maxx*ds+ds+2), min(H-1,maxy*ds+ds+2)))
    return out

rects = []
for (x1,y1,x2,y2) in comps(building_like, 400) + comps(water, 600):
    rects.append({"points":[[x1,y1],[x2,y1],[x2,y2],[x1,y2]]})

# 生成 PRESHAPES JS
js = "var PRESHAPES = " + json.dumps(rects, ensure_ascii=False) + ";"

# 注入到 mark_tool.html
path = ROOT + r"\mark_tool.html"
html = io.open(path, encoding="utf-8").read()
html = html.replace("var shapes = [];", js + "\n  var shapes = PRESHAPES.slice();")
io.open(path, "w", encoding="utf-8").write(html)
print(f"已注入 {len(rects)} 个预置形状到 mark_tool.html")
