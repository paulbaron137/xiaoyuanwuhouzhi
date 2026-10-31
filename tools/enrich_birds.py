# -*- coding: utf-8 -*-
"""用数据库 species_catalog 的描述/别名充实 SEED_SPECIES 鸟类，替换进 gameV5/index.html。"""
import re, io, json
from xml.etree import ElementTree as ET
import zipfile

DB = r"C:\Users\30891\Desktop\校园物志侯\database\10.29V0.2\species_catalog.xlsx"
HTML = r"C:\Users\30891\Desktop\校园物志侯\gameV5\index.html"

# 解析 DB
z = zipfile.ZipFile(DB); NS='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
ss=[]
for si in ET.fromstring(z.read('xl/sharedStrings.xml')).iter('{%s}si'%NS):
    ss.append(''.join(t.text or '' for t in si.iter('{%s}t'%NS)))
rows=[]
for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).iter('{%s}row'%NS):
    cells=[]
    for c in row.iter('{%s}c'%NS):
        t=c.get('t'); v=c.find('{%s}v'%NS); val=v.text if v is not None else ''
        if t=='s' and val!='': val=ss[int(val)] if int(val)<len(ss) else val
        cells.append(val)
    rows.append(cells)
# 字段: 0 id,2 name,3 alias,4 latin,5 english,6 family,12 desc,13 common
birds={}
for r in rows[2:]:
    if len(r)<14 or r[1]!='1': continue
    birds[int(r[0])]={'name':r[2],'alias':r[3],'latin':r[4],'english':r[5],'family':r[6],'desc':r[12],'common':(r[13]=='1')}

# 现有 habitat/phenology（DB这两列为空，沿用现有）
HAB = {1:'林缘、灌丛',2:'松林、阔叶林、公园',3:'林地、公园',4:'开阔低地、草坪',5:'水边、道路',6:'河岸、浅滩',7:'湖岸、河道',8:'花园、村庄',9:'草地、灌丛',10:'稀疏树木区',11:'旷野、城镇花园',12:'开阔林地、林园',13:'农田、果园',14:'森林、灌丛'}
PHE = {1:'留鸟，全年可见',2:'留鸟，全年可见',3:'留鸟，全年可见',4:'留鸟，全年可见',5:'留鸟及候鸟',6:'留鸟及候鸟',7:'留鸟，全年可见',8:'留鸟，全年可见',9:'留鸟，全年可见',10:'留鸟，全年可见',11:'留鸟，全年可见',12:'留鸟，全年可见',13:'留鸟，迁徙成大群',14:'冬候鸟'}

def q(s):  # JS 单引号字符串
    return "'"+s.replace("\\","\\\\").replace("'","\\'")+"'"

lines=[]
for i in range(1,15):
    b=birds[i]
    lines.append("  { id:'bird_%d', type:'bird', name:%s, alias:%s, latin:%s, english:%s, family:%s, habitat:%s, phenology:%s, desc:%s, common:%s }," % (
        i, q(b['name']), q(b['alias']), q(b['latin']), q(b['english']), q(b['family']), q(HAB[i]), q(PHE[i]), q(b['desc']), 'true' if b['common'] else 'false'))
new_birds="\n".join(lines)

html=io.open(HTML,encoding='utf-8').read()
# 替换 bird_1..bird_14 这一段（从 { id:'bird_1' 到 { id:'flower_rose' 之前）
pat = re.compile(r"(const SEED_SPECIES = \[\s*\n)(.*?)(\n\s*\{ id:'flower_rose')", re.S)
m = pat.search(html)
if not m:
    print("未找到 SEED_SPECIES 鸟段"); raise SystemExit(1)
html = pat.sub(lambda mm: mm.group(1)+new_birds+"\n"+mm.group(3), html, count=1)
io.open(HTML,'w',encoding='utf-8').write(html)
print(f"已用数据库充实 {len(birds)} 只鸟的描述")
