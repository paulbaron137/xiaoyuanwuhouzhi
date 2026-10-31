# -*- coding: utf-8 -*-
"""在地图上标注建筑/水域/区域，生成核对图。"""
import os
from PIL import Image, ImageDraw, ImageFont

MAP = r"C:\Users\30891\Desktop\校园物志侯\gameV2\assets\map_base.png"
OUT = r"C:\Users\30891\Desktop\校园物志侯\gameV2\tools\labeled_map.png"

# 建筑（框 + 名字，红色）
BUILDINGS = [
    ("图书馆",   568, 176, 758, 314),
    ("同心楼",   476, 420, 578, 560),
    ("同德楼",  1010, 568, 1166, 686),
    ("同济楼",   296, 870, 546, 1082),
    ("同仁楼",   626, 726, 888, 886),
    ("旭光厅",   318, 762, 468, 896),
    ("教学区南", 314, 984, 748, 1162),
    ("右下建筑", 1110, 1108, 1334, 1288),
    ("南门附近", 538, 1150, 724, 1278),
]
# 水域（蓝色）
WATER = [
    ("同心湖", 412, 592),
    ("水面?",  840, 524),
    ("东河?", 1213, 1202),
    ("西河?",  176, 1058),
]
# 区域（绿色，不确定的带?）
REGIONS = [
    ("南门广场", 717, 1300),
    ("生命大道", 717, 900),
    ("校友林?", 560, 500),
    ("医林?",   450, 450),
    ("百草园?", 900, 1000),
    ("西门?",   120, 1000),
]

# 中文字体
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
]
font_path = next((f for f in FONT_CANDIDATES if os.path.exists(f)), None)
font = ImageFont.truetype(font_path, 26) if font_path else ImageFont.load_default()

img = Image.open(MAP).convert("RGB")
draw = ImageDraw.Draw(img)

def text_center(x, y, text, color, outline=True):
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    if outline:
        draw.rectangle([x-w//2-5, y-h//2-4, x+w//2+5, y+h//2+4], fill=(255,255,255))
        draw.rectangle([x-w//2-5, y-h//2-4, x+w//2+5, y+h//2+4], outline=(80,60,40), width=2)
    draw.text((x-w//2, y-h//2-1), text, fill=color, font=font)

# 建筑框
for name, x1, y1, x2, y2 in BUILDINGS:
    draw.rectangle([x1, y1, x2, y2], outline=(220, 40, 40), width=4)
    text_center((x1+x2)//2, y1-16, name, (200, 30, 30))

# 水域
for name, x, y in WATER:
    draw.ellipse([x-14, y-14, x+14, y+14], outline=(30, 120, 220), width=4)
    text_center(x, y-30, name, (30, 90, 200))

# 区域
for name, x, y in REGIONS:
    draw.ellipse([x-11, y-11, x+11, y+11], outline=(40, 150, 60), width=4)
    text_center(x, y+24, name, (20, 110, 40))

# 缩小便于查看
scale = 0.8
img = img.resize((int(img.width*scale), int(img.height*scale)), Image.LANCZOS)
img.save(OUT)
print(f"已生成 {OUT} ({img.width}x{img.height})  字体:{os.path.basename(font_path) if font_path else 'default'}")
