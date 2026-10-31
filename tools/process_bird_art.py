# -*- coding: utf-8 -*-
"""把 docx 手绘鸟插画处理为图集素材（缩放到480，存 gameV5/assets/birds_art/）。"""
import os
from PIL import Image

SRC = r"C:\Users\30891\Desktop\校园物志侯\gameV5\tools\docx_media"
DST = r"C:\Users\30891\Desktop\校园物志侯\gameV5\assets\birds_art"
os.makedirs(DST, exist_ok=True)
SIZE = 480

# docx image -> 图标key
MAP = {
    'image1.jpeg':'bulbul',
    'image2.jpeg':'magpie',
    'image3.jpeg':'blackbird',
    'image4.jpeg':'blackbird_female',
    'image5.jpeg':'dove',
    'image6.jpeg':'wagtail',
    'image7.jpeg':'egret',
    'image8.jpeg':'night_heron',
    'image9.jpeg':'night_heron_juvenile',
    'image10.jpeg':'robin',
    'image11.jpeg':'robin_female',
    'image12.jpeg':'shrike',
    'image13.jpeg':'sparrow',
}

for fn, key in MAP.items():
    p = os.path.join(SRC, fn)
    im = Image.open(p).convert("RGB")
    im.thumbnail((SIZE, SIZE), Image.LANCZOS)
    out = os.path.join(DST, key + ".jpg")
    im.save(out, "JPEG", quality=88)
    print(f"{fn} -> {key}.jpg {im.size}")
print("完成")
