# -*- coding: utf-8 -*-
"""鸟类贴图处理：缩放到128x128、英文命名，复制进 gameV2/assets/birds/；并用新分类生成掩码预览。"""
import os
from PIL import Image

SRC_DIR = r"C:\Users\30891\Desktop\校园物志侯\鸟类\鸟类（像素手绘风）"
DST_DIR = r"C:\Users\30891\Desktop\校园物志侯\gameV2\assets\birds"

# 中文名 -> 英文文件名 映射
BIRDS = {
    "01白头鹎_像素手绘风.png": "bulbul.png",
    "02灰喜鹊_像素手绘风.png": "magpie.png",
    "03乌鸫_像素手绘风.png": "blackbird.png",
    "03乌鸫雌鸟_像素手绘风.png": "blackbird_female.png",
    "04珠颈斑鸠_像素手绘风.png": "dove.png",
    "05白鹡鸰_像素手绘风.png": "wagtail.png",
    "06白鹭_像素手绘风.png": "egret.png",
    "07夜鹭_像素手绘风.png": "night_heron.png",
    "07夜鹭亚成鸟_像素手绘风.png": "night_heron_juvenile.png",
    "08鹊鸲_像素手绘风.png": "robin.png",
    "08鹊鸲雌鸟_像素手绘风.png": "robin_female.png",
    "09棕背伯劳_像素手绘风.png": "shrike.png",
    "10麻雀_像素手绘风.png": "sparrow.png",
}

os.makedirs(DST_DIR, exist_ok=True)
SIZE = 128
for src_name, dst_name in BIRDS.items():
    src = os.path.join(SRC_DIR, src_name)
    dst = os.path.join(DST_DIR, dst_name)
    if not os.path.exists(src):
        print(f"缺失: {src_name}")
        continue
    img = Image.open(src).convert("RGBA")
    # 等比缩放（图片是方形，直接缩放到128）
    img = img.resize((SIZE, SIZE), Image.LANCZOS)
    img.save(dst)
    print(f"{src_name} -> {dst_name} ({SIZE}x{SIZE}, {os.path.getsize(dst)//1024}KB)")

# ---- 用新分类生成掩码预览 ----
import numpy as np
def walkable(r,g,b):
    mx=max(r,g,b); mn=min(r,g,b); sat=mx-mn
    if b>=90 and b>r+40 and b>g+10: return False
    if r>g+40 and r>b+40 and r>=120: return False
    if mx>=150 and sat<=20: return False
    if mx<=45: return False
    return True

map_img = Image.open(r"C:\Users\30891\Desktop\校园物志侯\gameV2\assets\map_base.png").convert("RGB")
a = np.asarray(map_img).astype(np.int16)
R,G,B = a[...,0], a[...,1], a[...,2]
MX = np.maximum(np.maximum(R,G),B); MN = np.minimum(np.minimum(R,G),B); SAT = MX-MN
blocked = ((B>=90)&(B>R+40)&(B>G+10)) | ((R>G+40)&(R>B+40)&(R>=120)) | ((MX>=150)&(SAT<=20)) | (MX<=45)
wk = ~blocked
overlay = np.asarray(map_img).copy().astype(np.int16)
overlay[blocked,0] = overlay[blocked,0]*0.35 + 255*0.65
overlay[blocked,1] = overlay[blocked,1]*0.35 + 60*0.65
overlay[blocked,2] = overlay[blocked,2]*0.35 + 60*0.65
out = Image.fromarray(overlay.astype(np.uint8), "RGB")
out = out.resize((map_img.width//2, map_img.height//2), Image.NEAREST)
prev = r"C:\Users\30891\Desktop\校园物志侯\gameV2\tools\mask_preview.png"
os.makedirs(os.path.dirname(prev), exist_ok=True)
out.save(prev)
print(f"\n掩码预览已生成 {prev} ({out.width}x{out.height})")
print(f"新分类：可走 {wk.mean()*100:.1f}% / 阻挡 {blocked.mean()*100:.1f}%")
