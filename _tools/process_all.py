#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gameV7 风格切换 · 规整管线：_gen 生成图 -> 去背景 -> 硬边像素化 -> 精确尺寸 -> gameV7/assets/

用法:
  py -3 process_all.py --dry        # 只预检映射与人物宽高比
  py -3 process_all.py              # 全量处理
  py -3 process_all.py --only birds # 只跑某组: map/birds/person/npc/bld/ui
"""
import os
import sys
import glob
import argparse

from PIL import Image

SKILL = r"C:\Users\30891\.workbuddy\skills\pixel-asset-forge\scripts"
sys.path.insert(0, SKILL)
from pixel_artify import pixel_artify, auto_remove_bg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # gameV7
GEN = os.path.join(ROOT, "_gen")
CROP = os.path.join(GEN, "_crop")
os.makedirs(CROP, exist_ok=True)


def find_gen(prefix):
    hits = [p for p in glob.glob(os.path.join(GEN, "*.png"))
            if os.path.basename(p).startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit("find_gen(%s) -> %d hits" % (prefix, len(hits)))
    return hits[0]


def crop_content(src, margin_frac=0.10, min_margin=16):
    """去白底后按内容 bbox 裁剪(带边距)，返回(临时文件, bbox, 内容宽高)。"""
    im = Image.open(src).convert("RGBA")
    im = auto_remove_bg(im, 26)
    bbox = im.getchannel("A").getbbox()
    if not bbox:
        raise SystemExit("crop_content: empty bbox %s" % src)
    x0, y0, x1, y1 = bbox
    cw, ch = x1 - x0, y1 - y0
    m = max(int(max(cw, ch) * margin_frac), min_margin)
    box = (max(0, x0 - m), max(0, y0 - m),
           min(im.size[0], x1 + m), min(im.size[1], y1 + m))
    im2 = im.crop(box)
    out = os.path.join(CROP, os.path.splitext(os.path.basename(src))[0][:10] + "_crop.png")
    im2.save(out)
    return out, box, (cw, ch)


def save(im, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)


def qc(name, im):
    a = im.getchannel("A")
    n = float(im.size[0] * im.size[1])
    trans = sum(1 for v in a.getdata() if v == 0)
    print("  QC %-26s %dx%d 透明%.0f%%" % (name, im.size[0], im.size[1], 100.0 * trans / n))


def do_map():
    mp = find_gen("把这张校园俯瞰地图")
    im = Image.open(mp).convert("RGB")
    # 水印覆盖：右下角区域 <- 同 x 带正上方草地
    patch = im.crop((760, 840, 1024, 934))          # 264x94
    im.paste(patch, (760, 930))
    tmp = os.path.join(CROP, "map_nowm.png")
    im.save(tmp)
    mim, _ = pixel_artify(tmp, 1434, 1395, 96, 0,
                          outline=False, denoise_on=False, merge_tol=32)
    save(mim, os.path.join(ROOT, "assets", "map_base.png"))
    qc("map_base", mim)


def do_person():
    persons = {
        "把这个像素小人": "person_front",
        "角色背影": "person_back",
        "角色左侧面": "person_left",
        "角色右侧面": "person_right",
    }
    for prefix, name in sorted(persons.items()):
        src = find_gen(prefix)
        csrc, _, (cw, ch) = crop_content(src, 0.08, 12)
        aspect = cw / float(ch)
        W, H = 40, 72
        if 0.45 <= aspect <= 0.75:
            im, _ = pixel_artify(csrc, W, H, 18, 26, outline=True, denoise_on=True)
            treat = "stretch"
        else:
            s = min(W / float(cw), H / float(ch))
            fw, fh = max(1, round(cw * s)), max(1, round(ch * s))
            im, _ = pixel_artify(csrc, fw, fh, 18, 26, outline=True, denoise_on=True)
            canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            canvas.paste(im, ((W - fw) // 2, H - fh))
            im = canvas
            treat = "letterbox"
        save(im, os.path.join(ROOT, "assets", "person", name + ".png"))
        qc(name, im)
        print("     person %s aspect=%.2f -> %s" % (name, aspect, treat))


def do_birds():
    birds = {
        "把这只麻雀": "sparrow",
        "白头鹎": "bulbul",
        "灰喜鹊": "magpie",
        "乌鸫雄鸟": "blackbird",
        "乌鸫雌鸟": "blackbird_female",
        "珠颈斑鸠": "dove",
        "白鹡鸰": "wagtail",
        "白鹭": "egret",
        "夜鹭成鸟": "night_heron",
        "夜鹭幼鸟": "night_heron_juvenile",
        "鹊鸲雄鸟": "robin",
        "鹊鸲雌鸟": "robin_female",
        "棕背伯劳": "shrike",
    }
    for prefix, name in sorted(birds.items()):
        src = find_gen(prefix)
        csrc, _, _ = crop_content(src, 0.10, 16)
        im, _ = pixel_artify(csrc, 128, 128, 28, 26, outline=True, denoise_on=True)
        save(im, os.path.join(ROOT, "assets", "birds", name + ".png"))
        qc("bird_" + name, im)


def do_npc():
    src = find_gen("观鸟NPC")
    csrc, _, _ = crop_content(src, 0.10, 16)
    im, _ = pixel_artify(csrc, 128, 128, 24, 26, outline=True, denoise_on=True)
    save(im, os.path.join(ROOT, "assets", "npc_magpie.png"))
    qc("npc_magpie", im)


def do_bld():
    bld = {
        "同心楼": ("tongxin", 500, 500),
        "同德楼": ("tongde", 400, 400),
        "同济楼": ("tongji", 400, 400),
        "同仁楼": ("tongren", 400, 400),
        "喷泉": ("fountain_plaza", 400, 400),
        "图书馆": ("library", 400, 400),
        "旭光厅": ("xuguang_hall", 400, 400),
    }
    for prefix, (name, W, H) in sorted(bld.items()):
        src = find_gen(prefix)
        csrc, _, _ = crop_content(src, 0.06, 12)
        im, _ = pixel_artify(csrc, W, H, 48, 26, outline=False, denoise_on=True)
        save(im, os.path.join(ROOT, "assets", "buildings", name + ".png"))
        qc("bld_" + name, im)


def do_ui():
    ui = {"木板纹理": "wood", "羊皮纸纹理": "parchment"}
    for prefix, name in sorted(ui.items()):
        src = find_gen(prefix)
        im, _ = pixel_artify(src, 512, 512, 64, 0,
                             outline=False, denoise_on=False, merge_tol=32)
        save(im, os.path.join(ROOT, "assets", "ui", name + ".png"))
        qc("ui_" + name, im)


def dry():
    groups = {
        "map": ["把这张校园俯瞰地图"],
        "person": ["把这个像素小人", "角色背影", "角色左侧面", "角色右侧面"],
        "birds": ["把这只麻雀", "白头鹎", "灰喜鹊", "乌鸫雄鸟", "乌鸫雌鸟", "珠颈斑鸠",
                  "白鹡鸰", "白鹭", "夜鹭成鸟", "夜鹭幼鸟", "鹊鸲雄鸟", "鹊鸲雌鸟", "棕背伯劳"],
        "npc": ["观鸟NPC"],
        "bld": ["同心楼", "同德楼", "同济楼", "同仁楼", "喷泉", "图书馆", "旭光厅"],
        "ui": ["木板纹理", "羊皮纸纹理"],
    }
    for g, prefixes in groups.items():
        for p in prefixes:
            src = find_gen(p)
            if g == "person":
                csrc, _, (cw, ch) = crop_content(src, 0.08, 12)
                print("DRY %-10s -> %s aspect=%.2f" % (p[:10], os.path.basename(src)[:30], cw / float(ch)))
            else:
                print("DRY %-10s -> %s" % (p[:10], os.path.basename(src)[:30]))
    print("DRY OK: 全部映射唯一")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--only", default=None)
    args = ap.parse_args()
    if args.dry:
        dry()
        return
    order = ["map", "person", "birds", "npc", "bld", "ui"]
    if args.only:
        order = [args.only]
    for g in order:
        print("== %s ==" % g)
        {"map": do_map, "person": do_person, "birds": do_birds,
         "npc": do_npc, "bld": do_bld, "ui": do_ui}[g]()
    print("ALL DONE")


if __name__ == "__main__":
    main()
