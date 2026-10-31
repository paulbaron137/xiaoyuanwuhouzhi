# -*- coding: utf-8 -*-
"""gameV7：恢复 10 种有真实图的植物 + PLANT_ICON + 植物标签 + 查图逻辑。"""
import io

P = r"C:\Users\30891\Desktop\校园物志侯\gameV7\index.html"
html = io.open(P, encoding="utf-8").read()

plants = [
    ('flower_rongshu','榕树','Ficus microcarpa','Chinese Banyan','桑科','校园绿地','常绿，气根发达','常绿大乔木，树冠广展，气根垂地成林，是南方校园的标志性景观树。'),
    ('flower_ginkgo','银杏','Ginkgo biloba','Ginkgo','银杏科','校园绿地','入秋转金黄','扇形叶片，入秋转金黄，冬日落叶。'),
    ('flower_camphor','香樟','Cinnamomum camphora','Camphor Tree','樟科','主干道两侧','常绿，果熟季吸引鸟类','常绿乔木，校园主干道两侧的林荫。香樟果成熟时白头鹎会光顾。'),
    ('flower_osmanthus','桂花','Osmanthus fragrans','Sweet Olive','木犀科','校园绿地','秋季盛花','秋季满园飘香，花讯期香气最浓。'),
    ('flower_duying','杜英','Elaeocarpus decipiens','Elaeocarpus','杜英科','校园绿地','花期5-6月','常绿乔木，叶片经冬不凋，初夏开白色小花，花瓣细裂如流苏。'),
    ('flower_privet','女贞','Ligustrum lucidum','Glossy Privet','木犀科','行道、绿地','花期6-7月','常绿乔木，夏日开满树白色小花，果实紫黑色，是优良的行道与庭荫树。'),
    ('flower_soapberry','无患子','Sapindus mukorossi','Soapberry','无患子科','校园绿地','入秋叶色金黄','落叶乔木，秋季叶色金黄，果皮可搓出泡沫，古时用作天然肥皂，故称无患子。'),
    ('flower_pondcypress','池杉','Taxodium ascendens','Pond Cypress','杉科','水边、湿地','入秋叶色红褐','落叶乔木，耐水湿，常植于水边，秋季叶色由绿转红褐，树形挺拔优美。'),
    ('flower_goldenrain','栾树','Koelreuteria paniculata','Goldenrain Tree','无患子科','行道、绿地','夏秋开花结果','落叶乔木，夏末开金黄小花，秋结红灯笼状蒴果，花果同赏。'),
    ('flower_willow','垂柳','Salix babylonica','Weeping Willow','杨柳科','水边、湖畔','早春发芽','落叶乔木，枝条细长下垂，喜水边，早春最早发芽，是湖畔的经典景致。'),
]

def q(s): return "'"+s.replace("\\","\\\\").replace("'","\\'")+"'"

lines=[]
for pid,name,latin,english,family,hab,phe,desc in plants:
    lines.append("  { id:'%s', type:'flower', name:%s, alias:'', latin:%s, english:%s, family:%s, habitat:%s, phenology:%s, desc:%s, common:true }," % (pid,q(name),q(latin),q(english),q(family),q(hab),q(phe),q(desc)))
plant_block = "\n".join(lines)

# 1) 在 bird_38 行后插入植物
anchor = "  { id:'bird_38',"
idx = html.index(anchor)
# 找到该行末尾
line_end = html.index("\n", idx)
html = html[:line_end+1] + plant_block + "\n" + html[line_end+1:]

# 2) PLANT_ICON 加在 SPECIES_ICON 后
plant_icon = "const PLANT_ICON = { " + ", ".join("%s:'plant_%s'"%(pid,pid.replace('flower_','')) for pid,_,_,_,_,_,_,_ in plants) + " };"
html = html.replace("const SPECIES_ICON = {", plant_icon + "\nconst SPECIES_ICON = {", 1)

# 3) 查图逻辑恢复 PLANT_ICON
html = html.replace("const icon=SPECIES_ICON[s.id];", "const icon=SPECIES_ICON[s.id] || PLANT_ICON[s.id];")
html = html.replace("    const icon=SPECIES_ICON[s.id];", "    const icon=SPECIES_ICON[s.id] || PLANT_ICON[s.id];")

# 4) 图鉴标签加「植物物候」
tab = '<div class="tab active" data-f="bird">🐦 鸟类</div>'
plant_tab = '<div class="tab" data-f="flower">🌿 植物物候</div>'
html = html.replace(tab, tab + "\n        " + plant_tab, 1)

io.open(P, "w", encoding="utf-8").write(html)
print("已恢复 %d 种植物" % len(plants))
