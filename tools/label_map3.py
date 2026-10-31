# -*- coding: utf-8 -*-
"""按用户参考图 + 实际楼体中心重新标注地图，生成核对图。"""
import os
from PIL import Image, ImageDraw, ImageFont

MAP = r"C:\Users\30891\Desktop\校园物志侯\gameV2\assets\map_base.png"
OUT = r"C:\Users\30891\Desktop\校园物志侯\gameV2\tools\labeled_map3.png"

# (名字, x, y, 类型)  类型: b=建筑(红框) r=区域(绿) w=水域(蓝)
SPOTS = [
    ("体育馆",        850, 294, "b"),
    ("图书馆",        450, 506, "b"),
    ("学生活动中心", 1075, 638, "b"),
    ("求知楼",       1050, 775, "b"),
    ("同济楼",        750, 825, "b"),
    ("同仁楼",        463, 938, "b"),
    ("旭光厅",        438, 675, "b"),
    ("同德楼",        463, 1175, "b"),
    ("同心楼",        625, 1313, "b"),
    ("校友林",        700, 563, "r"),
    ("喷泉广场",      500, 625, "r"),
    ("生命大道",      713, 1100, "r"),
    ("百草园",        300, 1350, "r"),
    ("南门广场",      888, 1350, "r"),
    ("西门",          231, 850, "r"),
]
WATER = [
    ("水面",   838, 525),
    ("东河",  1063, 1180),
    ("西河",   175, 1063),
]

FONT_CANDIDATES = [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\simsun.ttc"]
font_path = next((f for f in FONT_CANDIDATES if os.path.exists(f)), None)
font = ImageFont.truetype(font_path, 30) if font_path else ImageFont.load_default()

img = Image.open(MAP).convert("RGB")
draw = ImageDraw.Draw(img)

def text_center(x, y, text, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.rectangle([x-w//2-5, y-h//2-4, x+w//2+5, y+h//2+4], fill=(255,255,255))
    draw.rectangle([x-w//2-5, y-h//2-4, x+w//2+5, y+h//2+4], outline=(80,60,40), width=2)
    draw.text((x-w//2, y-h//2-1), text, fill=color, font=font)

for name, x, y, kind in SPOTS:
    if kind == "b":
        draw.rectangle([x-12, y-12, x+12, y+12], outline=(200, 30, 30), width=4)
        text_center(x, y-28, name, (180, 20, 20))
    else:
        draw.ellipse([x-12, y-12, x+12, y+12], outline=(30, 150, 60), width=4)
        text_center(x, y-28, name, (20, 110, 40))

for name, x, y in WATER:
    draw.ellipse([x-14, y-14, x+14, y+14], outline=(30, 120, 220), width=4)
    text_center(x, y-30, name, (20, 90, 200))

img = img.resize((int(img.width*0.8), int(img.height*0.8)), Image.LANCZOS)
img.save(OUT)
print(f"已生成 {OUT} ({img.width}x{img.height})")
