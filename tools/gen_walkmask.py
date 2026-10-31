# -*- coding: utf-8 -*-
"""预生成可走/阻挡掩码图（连通域分析，白=可走 黑=阻挡）。"""
import numpy as np
from PIL import Image
from collections import deque

MAP = r"C:\Users\30891\Desktop\校园物志侯\gameV3\assets\map_base.png"
OUT = r"C:\Users\30891\Desktop\校园物志侯\gameV3\assets\walkmask.png"

img = Image.open(MAP).convert("RGB")
a = np.asarray(img).astype(np.int16)
H, W = a.shape[:2]
R, G, B = a[...,0], a[...,1], a[...,2]
MX = np.maximum(np.maximum(R, G), B); MN = np.minimum(np.minimum(R, G), B); SAT = MX - MN

water = (B>=90)&(B>R+40)&(B>G+10)
building_like = ((MX>=150)&(SAT<=60)) | ((R>G+40)&(R>B+40)&(R>=70)&(MX<220))
black = (MX<=45)

# 连通域（下采样2加速）
ds = 2
bl = building_like[::ds, ::ds]
h, w = bl.shape
lab = np.zeros((h, w), dtype=np.int32)
cur = 0
big_ids = set()
for y in range(h):
    for x in range(w):
        if bl[y, x] and lab[y, x] == 0:
            cur += 1
            q = deque([(y, x)]); lab[y, x] = cur; area = 0
            while q:
                cy, cx = q.popleft(); area += 1
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < h and 0 <= nx < w and bl[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = cur; q.append((ny, nx))
            if area >= 500:  # 下采样面积阈值，约等于 2000 px²
                big_ids.add(cur)

# 上采样回原分辨率
big = np.zeros((H, W), dtype=bool)
for y in range(h):
    for x in range(w):
        if lab[y, x] in big_ids:
            big[y*ds:(y+1)*ds, x*ds:(x+1)*ds] = True

blocked = water | big | black
walk = ~blocked

mask_img = Image.fromarray((walk * 255).astype(np.uint8), 'L')
mask_img.save(OUT)
print(f"已生成 {OUT} ({W}x{H})")
print(f"可走 {walk.mean()*100:.1f}% / 阻挡 {blocked.mean()*100:.1f}%")
print(f"建筑块数量（大块）: {len(big_ids)}")
