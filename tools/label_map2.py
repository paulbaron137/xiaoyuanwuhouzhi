# -*- coding: utf-8 -*-
"""按用户参考图重新标注地图（建筑/区域/水域），生成核对图。"""
import os
from PIL import Image, ImageDraw, ImageFont

MAP = r"C:\Users\30891\Desktop\校园物志侯\gameV2\assets\map_base.png"
OUT = r"C:\Users\30891\Desktop\校园物志侯\gameV2\tools\labeled_map2.png"

# 按用户参考图（preview 1302x1267 -> 实际 1434x1395，×1.101）标注
# (名字, x, y, 类型)  类型: b=建筑(红框) r=区域(绿) w=水域(蓝)
SPOTS = [
    ("体育馆",       1195, 322, "b"),
    ("图书馆",        542, 547, "b"),
    ("学生活动中心", 1184, 677, "b"),
    ("求知楼",       1112, 809, "b"),
    ("同济楼",        773, 826, "b"),
    ("同仁楼",        481, 925, "b"),
    ("旭光厅",        435, 699, "b"),
    ("同德楼",        459, 1167, "b"),
    ("同心楼",        661, 1349, "b"),
    ("校友林",        701, 567, "r"),
    ("喷泉广场",      597, 683, "r"),
    ("生命大道",      716, 1112, "r"),
    ("百草园",        314, 1371, "r"),
    ("南门广场",      892, 1371, "r"),
    ("西门",          242, 859, "r"),
]
WATER = [
    ("同心湖", 412, 592),
    ("水面",   840, 524),
    ("东河",  1213, 1202),
    ("西河",   176, 1058),
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
        text_center(x, y-26, name, (180, 20, 20))
    else:
        draw.ellipse([x-12, y-12, x+12, y+12], outline=(30, 150, 60), width=4)
        text_center(x, y-26, name, (20, 110, 40))

for name, x, y in WATER:
    draw.ellipse([x-14, y-14, x+14, y+14], outline=(30, 120, 220), width=4)
    text_center(x, y-30, name, (20, 90, 200))

img = img.resize((int(img.width*0.8), int(img.height*0.8)), Image.LANCZOS)
img.save(OUT)
print(f"已生成 {OUT} ({img.width}x{img.height})")
