# -*- coding: utf-8 -*-
"""处理灰喜鹊NPC图：去白底 + 裁剪 + 缩放为 128x128 透明PNG。"""
import os
import numpy as np
from PIL import Image
from collections import deque

SRC = r"C:\Users\30891\Desktop\校园物志侯\gameV5\tools\npc_raw.webp"
DST = r"C:\Users\30891\Desktop\校园物志侯\gameV5\assets\npc_magpie.png"
SIZE = 128

a = np.asarray(Image.open(SRC).convert("RGB"))
H, W = a.shape[:2]

# 边缘泛洪去白底
thresh = 240
light = (a[:,:,0] > thresh) & (a[:,:,1] > thresh) & (a[:,:,2] > thresh)
visited = np.zeros((H,W), dtype=bool)
q = deque()
for x in range(W):
    if light[0,x]: visited[0,x]=True; q.append((0,x))
    if light[H-1,x]: visited[H-1,x]=True; q.append((H-1,x))
for y in range(H):
    if light[y,0]: visited[y,0]=True; q.append((y,0))
    if light[y,W-1]: visited[y,W-1]=True; q.append((y,W-1))
while q:
    y,x = q.popleft()
    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
        ny,nx = y+dy, x+dx
        if 0<=ny<H and 0<=nx<W and light[ny,nx] and not visited[ny,nx]:
            visited[ny,nx]=True; q.append((ny,nx))

ys, xs = np.where(~visited)
print(f"前景包围盒: x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
alpha = np.where(visited, 0, 255).astype(np.uint8)
rgba = np.dstack([a, alpha])[ys.min():ys.max()+1, xs.min():xs.max()+1]
im = Image.fromarray(rgba, "RGBA")
# 等比缩放到 SIZE 内
r = min(SIZE/im.width, SIZE/im.height)
nw, nh = max(1, round(im.width*r)), max(1, round(im.height*r))
im = im.resize((nw,nh), Image.LANCZOS)
canvas = Image.new("RGBA", (SIZE,SIZE), (0,0,0,0))
canvas.paste(im, ((SIZE-nw)//2, (SIZE-nh)//2), im)
canvas.save(DST)
print(f"已保存 {DST} ({SIZE}x{SIZE}) 内容 {nw}x{nh}")
