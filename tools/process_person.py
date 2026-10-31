# -*- coding: utf-8 -*-
"""人物图片处理：去背景 + 裁剪 + 统一 40x72 居中适配。"""
import os
import numpy as np
from PIL import Image
from collections import deque

SRC = r"C:\Users\30891\Desktop\校园物志侯\pictures\person"
DST = r"C:\Users\30891\Desktop\校园物志侯\gameV4\assets\person"
os.makedirs(DST, exist_ok=True)
TW, TH = 40, 72  # 固定帧尺寸

def remove_bg(a, thresh=230):
    H, W = a.shape[:2]
    light = (a[:,:,0] > thresh) & (a[:,:,1] > thresh) & (a[:,:,2] > thresh)
    visited = np.zeros((H,W), dtype=bool); q = deque()
    for x in range(W):
        if light[0,x]: visited[0,x]=True; q.append((0,x))
        if light[H-1,x]: visited[H-1,x]=True; q.append((H-1,x))
    for y in range(H):
        if light[y,0]: visited[y,0]=True; q.append((y,0))
        if light[y,W-1]: visited[y,W-1]=True; q.append((y,W-1))
    while q:
        y,x=q.popleft()
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and light[ny,nx] and not visited[ny,nx]:
                visited[ny,nx]=True; q.append((ny,nx))
    return visited

files = ["person_front.png","person_back.png","person_left.png","person_right.png"]
for f in files:
    a = np.asarray(Image.open(os.path.join(SRC,f)).convert("RGB"))
    bg = remove_bg(a)
    ys, xs = np.where(~bg)
    if len(xs)==0: print(f"{f}: 无人物"); continue
    x1,x2 = xs.min(), xs.max(); y1,y2 = ys.min(), ys.max()
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    crop = np.dstack([a, alpha])[y1:y2+1, x1:x2+1]
    im = Image.fromarray(crop, "RGBA")
    # 等比缩放到 40x72 内（contain）
    ratio = min(TW/im.width, TH/im.height)
    nw, nh = max(1,round(im.width*ratio)), max(1,round(im.height*ratio))
    im = im.resize((nw,nh), Image.LANCZOS)
    # 居中放到透明画布
    canvas = Image.new("RGBA", (TW,TH), (0,0,0,0))
    canvas.paste(im, ((TW-nw)//2, (TH-nh)//2), im)
    canvas.save(os.path.join(DST, f))
    # 报告不透明占比
    a2 = np.asarray(canvas)[:,:,3]
    print(f"{f}: 内容 {nw}x{nh} -> 居中于 {TW}x{TH}, 不透明占比 {np.mean(a2>0)*100:.1f}%")
print("完成")
