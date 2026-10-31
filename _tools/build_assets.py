#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gameV7 · 按 40 键原序重建 assets.js：新像素素材 base64 内嵌；art_*/walkmask 沿用旧值。"""
import os
import re
import base64

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BIRDS = ["bulbul", "magpie", "blackbird", "blackbird_female", "dove", "wagtail",
         "egret", "night_heron", "night_heron_juvenile", "robin", "robin_female",
         "shrike", "sparrow"]

FILEMAP = {
    "map_base": "assets/map_base.png",
    "bld_tongxin": "assets/buildings/tongxin.png",
    "bld_tongde": "assets/buildings/tongde.png",
    "bld_tongji": "assets/buildings/tongji.png",
    "bld_tongren": "assets/buildings/tongren.png",
    "bld_fountain": "assets/buildings/fountain_plaza.png",
    "bld_library": "assets/buildings/library.png",
    "bld_xuguang": "assets/buildings/xuguang_hall.png",
    "player_front": "assets/person/person_front.png",
    "player_back": "assets/person/person_back.png",
    "player_left": "assets/person/person_left.png",
    "player_right": "assets/person/person_right.png",
    "npc_magpie": "assets/npc_magpie.png",
}
for b in BIRDS:
    FILEMAP[b] = "assets/birds/%s.png" % b
KEEP = set(["walkmask"]) | set("art_" + b for b in BIRDS)

old = open(os.path.join(ROOT, "assets.js"), encoding="utf-8").read()
keys = []
for k in re.findall(r'"([^"]+)"\s*:', old):
    if k not in keys:
        keys.append(k)
values = dict(re.findall(r'"([^"]+)"\s*:\s*"(data:image/[^"]+)"', old))
print("old keys: %d, parsed values: %d" % (len(keys), len(values)))

out = ["// 校园物候志 v7 星露谷像素风 - 内嵌资源（脚本生成，勿手改）",
       "window.ASSETS = {"]
regen, kept = 0, 0
for k in keys:
    if k in FILEMAP:
        p = os.path.join(ROOT, FILEMAP[k])
        uri = "data:image/png;base64,%s" % base64.b64encode(open(p, "rb").read()).decode()
        regen += 1
    elif k in KEEP:
        uri = values[k]
        kept += 1
    else:
        raise SystemExit("unknown key: %s" % k)
    out.append('  "%s": "%s",' % (k, uri))
out.append("};")
open(os.path.join(ROOT, "assets.js"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("regen: %d, keep: %d, total: %d" % (regen, kept, regen + kept))
print("assets.js size: %.1f MB" % (os.path.getsize(os.path.join(ROOT, "assets.js")) / 1048576.0))
