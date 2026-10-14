# -*- coding: utf-8 -*-
"""
Generator for Japan Deep Travel Guide v2 (v2.html)
Features:
- 100% API-independent, self-contained SVG Cartographic Engine of Japan
- Tri-state adaptive layout (Swiss-Japanese Grid, Noto Serif SC, JetBrains Mono)
- 3 Classic Routes based on 2026 Argon specifications
- Dual-mode transport reactive switch (Mode A Public Transit vs Mode B Legal Self-Driving)
- Interactive D3-style elevation profile and timeline brush
- Reactive budget sandbox comparing Public Transit vs Self-Drive
- Visa submission itinerary exporter table
- Strictly zero emoji, 100% clean SVG icons
"""
import json
import math

# Load raw GeoJSON of Japan
with open('japan-travel-guide/japan_raw.geojson', 'r', encoding='utf-8') as f:
    raw_geo = json.load(f)

# Calibrated projection parameters
MAP_W = 1000
MAP_H = 750
MIN_LNG = 129.0
MAX_LNG = 143.5
MIN_LAT = 31.0
MAX_LAT = 42.8

def project(lng, lat):
    """Calibrated Mercator projection for Japan mainland & major islands"""
    x = (lng - MIN_LNG) / (MAX_LNG - MIN_LNG) * MAP_W
    lat_rad = math.radians(lat)
    merc_y = math.log(math.tan(math.pi / 4 + lat_rad / 2))
    min_merc = math.log(math.tan(math.pi / 4 + math.radians(MIN_LAT) / 2))
    max_merc = math.log(math.tan(math.pi / 4 + math.radians(MAX_LAT) / 2))
    y = (max_merc - merc_y) / (max_merc - min_merc) * MAP_H
    return round(x, 1), round(y, 1)

# Extract and simplify polygons for Japan
polygons = []
for p in raw_geo['geometry']['coordinates']:
    ring = p[0]
    if len(ring) >= 12: # Major islands and significant features
        pts = [project(pt[0], pt[1]) for pt in ring]
        simplified = [pts[0]]
        for pt in pts[1:]:
            if abs(pt[0] - simplified[-1][0]) > 0.7 or abs(pt[1] - simplified[-1][1]) > 0.7:
                simplified.append(pt)
        if len(simplified) >= 4:
            d = 'M ' + ' L '.join(f'{x},{y}' for x, y in simplified) + ' Z'
            polygons.append(d)

print(f"Total simplified SVG land polygons: {len(polygons)}")

# Complete Route Data Structure according to 2026 Argon Spec
routes_spec = {
    "route-1": {
        "id": "route-1",
        "title": "本州脊梁与千年古道：中山道、北陆工艺、纪伊熊野纵贯线",
        "shortTitle": "本州脊梁与千年古道",
        "durationDays": 18,
        "entryAirport": "中部国际 (NGO)",
        "exitAirport": "关西国际 (KIX)",
        "themeColor": "#264653",
        "accentColor": "#2a9d8f",
        "totalDistanceKm": 880,
        "trailWalkingKm": 32,
        "bestSeason": "4–6月（新绿雪墙）、10–11月（阶梯红叶）",
        "winterNote": "冬季（1-2月）：信越山岳与北陆进入豪雪期，地狱谷野猿泡汤、兼六园雪吊及五箇山雪景极美。上高地冬季闭山封路，自动换乘为松本城与安昙野冬线。",
        "autumnNote": "早秋（9-10月）：日本阿尔卑斯山脉（上高地、立山）与信州高原秋意盎然，大正池倒映红枫，气候干爽，古道徒步体感绝佳。",
        "stops": [
            {"day": 1, "name": "名古屋 / 犬山城", "lng": 136.9066, "lat": 35.1815, "elev": 55, "type": "transit", "desc": "旅程起点，现存最古老天守犬山城与如庵茶室。"},
            {"day": 2, "name": "美浓和纸之乡", "lng": 136.9100, "lat": 35.5450, "elev": 95, "type": "culture", "desc": "江户卯建防火山墙商贾街区与长良川铁道。"},
            {"day": 3, "name": "木曾路·马笼宿", "lng": 137.5661, "lat": 35.5262, "elev": 600, "type": "trail", "desc": "中山道石板路起点，行李托运轻装徒步。"},
            {"day": 4, "name": "妻笼宿 → 奈良井宿", "lng": 137.8124, "lat": 35.9669, "elev": 940, "type": "trail", "desc": "海拔最高木曾宿场町，千轩见世物产。"},
            {"day": 5, "name": "松本城 (国宝天守)", "lng": 137.9720, "lat": 36.2380, "elev": 590, "type": "culture", "desc": "五重六层黑白木造天守与日本民俗学博物馆。"},
            {"day": 6, "name": "安昙野 / 上高地", "lng": 137.6333, "lat": 36.2486, "elev": 1505, "type": "nature", "desc": "阿尔卑斯圣地，大正池至河童桥原生林徒步。"},
            {"day": 7, "name": "奥飞驒温泉乡", "lng": 137.5333, "lat": 36.2167, "elev": 1100, "type": "onsen", "desc": "翻越北阿尔卑斯山脉，天然野溪秘汤露天风吕。"},
            {"day": 8, "name": "飞驒古川", "lng": 137.1878, "lat": 36.2365, "elev": 510, "type": "culture", "desc": "避开高山人潮，白壁土藏与濑户川清流锦鲤。"},
            {"day": 9, "name": "五箇山合掌集落", "lng": 136.9066, "lat": 36.2566, "elev": 380, "type": "heritage", "desc": "世界文化遗产相仓合掌造，清净原生态体验。"},
            {"day": 10, "name": "金泽 (百万石工艺)", "lng": 136.6562, "lat": 36.5613, "elev": 25, "type": "culture", "desc": "铃木大拙馆、长町武家屋敷、兼六园。"},
            {"day": 11, "name": "越前福井·永平寺", "lng": 136.3556, "lat": 36.0560, "elev": 180, "type": "culture", "desc": "曹洞宗大本山永平寺七堂伽蓝深山古杉。"},
            {"day": 12, "name": "琵琶湖西岸 / 比叡山", "lng": 135.8400, "lat": 35.2500, "elev": 848, "type": "culture", "desc": "湖中鸟居白须神社与天台宗根本中堂延历寺。"},
            {"day": 13, "name": "飞鸟·明日香村", "lng": 135.8167, "lat": 34.4667, "elev": 110, "type": "culture", "desc": "日本律令国家发源地，石舞台古坟e-Bike骑行。"},
            {"day": 14, "name": "吉野山修验道", "lng": 135.8583, "lat": 34.3686, "elev": 455, "type": "heritage", "desc": "金峯山寺藏王堂，中千本山岳信仰秘境。"},
            {"day": 15, "name": "熊野古道·中边路", "lng": 135.7739, "lat": 33.8406, "elev": 310, "type": "trail", "desc": "发心门王子至熊野本宫大社7km森林古道。"},
            {"day": 16, "name": "汤之峰温泉 (壶汤)", "lng": 135.7578, "lat": 33.8319, "elev": 150, "type": "onsen", "desc": "1800年历史世界遗产入浴天然小石汤。"},
            {"day": 17, "name": "那智大社与那智瀑布", "lng": 135.8906, "lat": 33.6744, "elev": 330, "type": "heritage", "desc": "落差133米飞泷神社神体瀑布与熊野那智大社。"},
            {"day": 18, "name": "纪伊田边 ➔ 关西机场", "lng": 135.2441, "lat": 34.4347, "elev": 15, "type": "transit", "desc": "特急黑潮号沿纪伊海岸北上直抵关西机场返程。"}
        ],
        "daysDetail": [
            {
                "day": 1,
                "title": "名古屋入境 ➔ 犬山城下町 ➔ 美浓",
                "elev": "55m → 95m",
                "story": "自名古屋中部机场落地后，避开市区大商场，直接北上尾张与美浓边界。探访日本现存最古老木造天守之一的犬山城，并在有乐苑参拜国宝茶室如庵。傍晚抵达美浓和纸之乡。",
                "modeA": {"line": "名铁犬山线 + 长良川铁道观光列车", "pass": "不适用全国券，刷Suica单买", "cost": "1,420円", "tip": "美浓太田站换乘长良川铁道时注意单节柴油车发车时刻。"},
                "modeB": {"route": "中部国际空港 ➔ 东海北陆道美浓IC", "dist": "78 km", "time": "1小时15分", "toll": "2,450円 (ETC)", "mapCode": "38 654 219*22", "difficulty": "★☆☆☆☆", "park": "美浓传统建造物群免费第1停车场"},
                "dining": {"name": "うなぎ 登河 (犬山店)", "specialty": "备长炭炙烤名古屋一本鳗鱼饭", "score": "3.58", "cost": "3,400円"},
                "stay": {"economy": "美浓 旅籠八代 (古民家改建宿)", "comfort": "NIPPONIA 美浓 商家町 (百年纸商和邸)"}
            },
            {
                "day": 2,
                "title": "美浓和纸老街 ➔ 长良川上游",
                "elev": "95m → 120m",
                "story": "考察美浓市本住町保存完好的江户时期“卯建（Udatsu）”防火山墙建筑群。探访美浓和纸工艺馆，了解手工纸抄造传统。",
                "modeA": {"line": "长良川铁道 慢车", "pass": "一日自由乘车券", "cost": "1,200円", "tip": "车窗可俯瞰清澈的长良川香鱼游弋。"},
                "modeB": {"route": "国道156号沿长良川北上", "dist": "35 km", "time": "45分", "toll": "0円", "mapCode": "194 332 501*11", "difficulty": "★☆☆☆☆", "park": "美浓市政厅公营停车场"},
                "dining": {"name": "美浓桥畔 香鱼茶屋", "specialty": "长良川天然炭火烤活香鱼定食", "score": "3.48", "cost": "2,200円"},
                "stay": {"economy": "美浓市 纸町町家客栈", "comfort": "长良川温泉 十八楼"}
            },
            {
                "day": 3,
                "title": "木曾路古道徒步：马笼宿 ➔ 妻笼宿",
                "elev": "600m → 420m",
                "story": "进入江户五街道之“中山道·木曾路”。从马笼宿出发，8:30前在观光案内所办理行李托运（1,000日元/件寄至妻笼），轻装翻越马笼峠，沿石板林荫古道缓坡下行8公里至妻笼宿。",
                "modeA": {"line": "JR中央本线（中津川站转北惠那巴士）", "pass": "刷IC卡", "cost": "980円", "tip": "南木曾前往妻笼的路线巴士班次稀疏，务必对好时刻。"},
                "modeB": {"route": "国道19号 ➔ 妻笼宿公共停车场", "dist": "52 km", "time": "1小时10分", "toll": "0円", "mapCode": "398 524 112*44", "difficulty": "★★☆☆☆", "park": "妻笼宿第3公营停车场 (500円/天)，乘早班接驳车至马笼徒步走回"},
                "dining": {"name": "音吉 (妻笼宿)", "specialty": "木曾五平饼 & 手打十割荞麦面", "score": "3.52", "cost": "1,350円"},
                "stay": {"economy": "妻笼宿 阪本屋旅笼 (传统木造榻榻米)", "comfort": "富贵之森温泉酒店 (深山露天柏木风吕)"}
            },
            {
                "day": 4,
                "title": "妻笼宿 ➔ 奈良井宿 (海拔最高宿场)",
                "elev": "420m → 940m",
                "story": "前往海拔940米的中山道最高宿场“奈良井宿”，长达一公里的千轩见世木造建筑保存原貌，探访漆器匠人街平泽。",
                "modeA": {"line": "JR中央本线 普通列车 (南木曾 ➔ 奈良井)", "pass": "JR乘车券", "cost": "1,170円", "tip": "每1-2小时仅一班车，建议搭乘10:14班次。"},
                "modeB": {"route": "国道19号 木曾高速街道北上", "dist": "62 km", "time": "1小时20分", "toll": "0円", "mapCode": "402 781 229*05", "difficulty": "★★☆☆☆", "park": "奈良井宿权现桥免费停车场 (步行入老街2分)"},
                "dining": {"name": "越后屋 (Echigoya)", "specialty": "投汁荞麦面 (Toji Soba) 与山菜天妇罗", "score": "3.54", "cost": "1,600円"},
                "stay": {"economy": "奈良井宿 民艺旅馆 深山", "comfort": "BYAKU Narai (百年酒藏改建精品名宿)"}
            },
            {
                "day": 5,
                "title": "奈良井 ➔ 松本城 (国宝木造天守)",
                "elev": "940m → 590m",
                "story": "抵达阿尔卑斯山麓重镇松本，参拜日本现存最古老的五重六层黑白木造天守松本城，探访松本市美术馆草间弥生常设展。",
                "modeA": {"line": "JR中央本线 快速 (约45分)", "pass": "刷Suica", "cost": "590円", "tip": "松本站内出站口有大件行李寄物柜。"},
                "modeB": {"route": "国道19号 直达松本市", "dist": "34 km", "time": "50分", "toll": "0円", "mapCode": "75 851 120*11", "difficulty": "★☆☆☆☆", "park": "松本城大手门立体停车场"},
                "dining": {"name": "松本野麦 荞麦处", "specialty": "极细现打九一手打荞麦", "score": "3.66", "cost": "1,500円"},
                "stay": {"economy": "Dormy Inn 松本 (天然温泉+夜鸣拉面)", "comfort": "松本丸之内酒店 (近代洋风历史建筑)"}
            },
            {
                "day": 6,
                "title": "松本 ➔ 上高地原生林 (秋) / 安昙野 (冬)",
                "elev": "590m → 1505m",
                "story": "早秋时段换乘环保接驳车进入日本阿尔卑斯圣地“上高地”，大正池徒步至河童桥与明神池，白桦树与梓川清流如翡翠；冬季封山期游览安昙野大王山葵农场与北阿尔卑斯展望路线。",
                "modeA": {"line": "松本电铁上高地线 + 登山接驳巴士", "pass": "上高地往返乘车券", "cost": "4,700円", "tip": "上高地全面禁止私家车，公共交通最快直达。"},
                "modeB": {"route": "自驾至泽渡 (Sawatari) 停车场换乘专线巴士", "dist": "38 km", "time": "50分", "toll": "0円", "mapCode": "605 085 241*33", "difficulty": "★★★☆☆", "park": "泽渡公共停车场 (700円/天)"},
                "dining": {"name": "上高地帝国饭店 咖啡厅", "specialty": "信州林檎派 (苹果派) 与手冲咖啡", "score": "3.59", "cost": "1,800円"},
                "stay": {"economy": "白船庄 新平汤温泉民宿", "comfort": "上高地大正池酒店 / 帝国饭店"}
            },
            {
                "day": 7,
                "title": "上高地 ➔ 安房峠 ➔ 奥飞驒温泉乡",
                "elev": "1505m → 1100m",
                "story": "穿过安房峠隧道翻越本州屋脊进入飞驒国，入住拥有日本最大露天露天风吕群的奥飞驒温泉乡（新穗高温泉或平汤温泉）。",
                "modeA": {"line": "浓飞巴士 (上高地/平汤 ➔ 新穗高)", "pass": "浓飞阿尔卑斯广域券", "cost": "1,850円", "tip": "注意末班巴士通常在17:00前。"},
                "modeB": {"route": "国道158号 ➔ 安房峠道路 (高海拔隧道)", "dist": "32 km", "time": "40分", "toll": "790円", "mapCode": "569 008 412*11", "difficulty": "★★★☆☆", "park": "各温泉旅馆专属免费停车位"},
                "dining": {"name": "平汤温泉 食事处 禄次", "specialty": "飞驒牛朴叶味噌烧定食", "score": "3.51", "cost": "2,400円"},
                "stay": {"economy": "平汤温泉 旅庄 露天之汤", "comfort": "佳留萱山庄 (日本最大秘汤清流露天风吕)"}
            },
            {
                "day": 8,
                "title": "奥飞驒 ➔ 飞驒古川 (避开高山人潮)",
                "elev": "1100m → 510m",
                "story": "避开游客拥挤的飞驒高山老街，前往幽静的飞驒古川。沿濑户川白壁土藏群漫步，近千尾彩色锦鲤在渠中巡游，造访木匠会馆。",
                "modeA": {"line": "浓飞特急巴士 ➔ JR高山本线 (古川站)", "pass": "广域通票", "cost": "1,450円", "tip": "古川站案内所可免费租借语音导览。"},
                "modeB": {"route": "国道471号 ➔ 国道41号", "dist": "48 km", "time": "1小时", "toll": "0円", "mapCode": "191 548 772*88", "difficulty": "★★☆☆☆", "park": "飞驒市役所前免费观光停车场"},
                "dining": {"name": "味处 古川", "specialty": "朴叶味噌牛排 & 蓬莱纯米酒", "score": "3.50", "cost": "2,200円"},
                "stay": {"economy": "古川 八三馆町家旅馆", "comfort": "季古里 飞驒古川山庄"}
            },
            {
                "day": 9,
                "title": "飞驒古川 ➔ 世界遗产五箇山合掌造",
                "elev": "510m → 380m",
                "story": "前往世界文化遗产五箇山（相仓或菅沼集落）。比白川乡清静数倍，保留浓郁山村农家气息，造访五箇山和纸工坊。",
                "modeA": {"line": "世界遗产观光巴士 (高山 ➔ 白川乡 ➔ 五箇山相仓)", "pass": "五箇山区间票", "cost": "2,600円", "tip": "相仓口站下车需徒步约5分钟入村。"},
                "modeB": {"route": "东海北陆道 ➔ 五箇山IC", "dist": "56 km", "time": "55分", "toll": "1,680円", "mapCode": "549 018 335*00", "difficulty": "★★☆☆☆", "park": "相仓合掌集落保存协力金停车场 (500円)"},
                "dining": {"name": "茶房 まつや (相仓)", "specialty": "五箇山硬豆腐刺身 & 岩鱼盐烤", "score": "3.47", "cost": "1,500円"},
                "stay": {"economy": "相仓合掌造民宿 勇助 (一泊二食)", "comfort": "五箇山温泉 赤尾馆"}
            },
            {
                "day": 10,
                "title": "五箇山 ➔ 金泽 (加贺百万石美学)",
                "elev": "380m → 25m",
                "story": "出山脉抵日本海工艺重都金泽。游览日本三大名园之首兼六园、金泽21世纪美术馆、长町武家屋敷与极富禅意的铃木大拙馆。",
                "modeA": {"line": "加越能巴士 ➔ 北陆新干线/爱之风铁道抵金泽", "pass": "北陆拱形券或买单程", "cost": "1,980円", "tip": "金泽站东口购买城下町周游一日券 (800円)。"},
                "modeB": {"route": "东海北陆道转北陆自动车道 金泽森本IC", "dist": "64 km", "time": "1小时", "toll": "1,890円", "mapCode": "41 528 200*44", "difficulty": "★☆☆☆☆", "park": "兼六坂市营地下停车场"},
                "dining": {"name": "金泽 近江町市场 寿司 歴々", "specialty": "喉黑鱼 (Nodoguro) 炙烤握寿司 & 白虾", "score": "3.64", "cost": "3,800円"},
                "stay": {"economy": "Dormy Inn 金泽 (天然温泉加贺之汤)", "comfort": "三井花园酒店 金泽白巧"}
            },
            {
                "day": 11,
                "title": "金泽 ➔ 福井曹洞宗大本山永平寺",
                "elev": "25m → 180m",
                "story": "南下福井深山，参拜道元禅师770年前开创的曹洞宗大本山永平寺，在伞松阁天井画与七堂伽蓝中感受深邃禅宗净土。下午探访越前和纸之里。",
                "modeA": {"line": "北陆新干线至福井站 ➔ 京福特快巴士直达永平寺", "pass": "周游券覆盖铁道段", "cost": "1,850円", "tip": "寺内木地板需脱鞋慢行，殿堂肃穆。"},
                "modeB": {"route": "北陆道 福井北IC ➔ 中部纵贯道 永平寺参道IC", "dist": "72 km", "time": "1小时05分", "toll": "2,100円", "mapCode": "63 681 405*22", "difficulty": "★☆☆☆☆", "park": "永平寺门前公营参道停车场"},
                "dining": {"name": "永平寺 门前 井之上 荞麦", "specialty": "越前带辛味白萝卜泥荞麦面 (Oroshi Soba)", "score": "3.52", "cost": "1,200円"},
                "stay": {"economy": "芦原温泉 清风庄 (北陆名汤)", "comfort": "永平寺 亲禅之宿 柏树关 (宿坊体验与精进料理)"}
            },
            {
                "day": 12,
                "title": "福井 ➔ 琵琶湖西岸 (白须神社·比叡山)",
                "elev": "180m → 848m",
                "story": "沿琵琶湖西岸南下，远眺水中鸟居白须神社；乘叡山缆车登上“日本佛教母山”比叡山延历寺，考察东塔国宝根本中堂。",
                "modeA": {"line": "JR湖西线 新快速 (近江今津 ➔ 坂本比叡山口)", "pass": "关西广域或JR乘车券", "cost": "1,340円", "tip": "坂本站有日本最长坂道比叡山缆车。"},
                "modeB": {"route": "国道161号 琵琶湖西纵贯道路", "dist": "95 km", "time": "1小时40分", "toll": "0円", "mapCode": "270 285 410*00", "difficulty": "★★☆☆☆", "park": "比叡山延历寺东塔山顶停车场"},
                "dining": {"name": "比叡山 延历寺会馆 望湖亭", "specialty": "近江比叡汤叶精进料理", "score": "3.49", "cost": "2,500円"},
                "stay": {"economy": "大津 琵琶湖万枫酒店", "comfort": "延历寺会馆 (宿坊，清晨参加根本中堂早课)"}
            },
            {
                "day": 13,
                "title": "飞鸟·明日香村 (日本律令文明起点)",
                "elev": "848m → 110m",
                "story": "进入奈良盆地南端古代大和朝廷核心明日香村。在观光案内所租借e-Bike，骑行于梯田间探访石舞台巨石古坟、飞鸟寺大佛及高松冢古坟壁画馆。",
                "modeA": {"line": "近铁吉野线 (飞鸟站)", "pass": "刷IC卡", "cost": "890円", "tip": "飞鸟站前即是租赁e-Bike中心 (1,500円/天)。"},
                "modeB": {"route": "京奈和自动车道 ➔ 橿原高田IC", "dist": "68 km", "time": "1小时15分", "toll": "1,200円", "mapCode": "36 295 108*77", "difficulty": "★☆☆☆☆", "park": "石舞台古坟公营停车场 (免费)"},
                "dining": {"name": "kotodama (ことだま)", "specialty": "明日香村本地时令无农药野菜定食", "score": "3.55", "cost": "1,750円"},
                "stay": {"economy": "明日香村 农家民宿 (Tatami Stay)", "comfort": "橿原皇家大酒店 (露天天然大浴场)"}
            },
            {
                "day": 14,
                "title": "明日香 ➔ 修验道圣地吉野山",
                "elev": "110m → 455m",
                "story": "深入纪伊山地北缘修验道总本山吉野山。参拜金峯山寺藏王堂（国宝大木造建筑），走访吉水神社（南朝皇居与弁庆隐匿地），俯瞰中千本山岳。",
                "modeA": {"line": "近铁吉野特急 (约25分)", "pass": "近铁特急券", "cost": "780円", "tip": "吉野站有日本现存最古老吉野山缆车接驳。"},
                "modeB": {"route": "国道169号 ➔ 吉野山景观道路", "dist": "22 km", "time": "35分", "toll": "0円", "mapCode": "36 122 890*11", "difficulty": "★★★☆☆", "park": "吉野山中千本公营停车场 (非樱花季免费)"},
                "dining": {"name": "八十吉 (吉野山)", "specialty": "吉野葛切 (Kuzukiri) & 柿叶寿司", "score": "3.56", "cost": "1,400円"},
                "stay": {"economy": "吉野山 景胜之宿 芳云馆", "comfort": "竹林院 群芳园 (千利休庭园宿)"}
            },
            {
                "day": 15,
                "title": "吉野 ➔ 熊野古道中边路徒步",
                "elev": "455m → 310m",
                "story": "跨越十津川深谷纵贯纪伊山脉抵达熊野古道世界遗产核心段。从“发心门王子”开始，在古杉与苔藓覆盖的石板参道徒步7公里至熊野本宫大社。",
                "modeA": {"line": "奈良交通八木新宫线 (日本最长路面巴士，体验段)", "pass": "巴士分段买票", "cost": "3,400円", "tip": "本宫大社前观光中心可盖熊野古道巡礼印章。"},
                "modeB": {"route": "国道168号 (纵贯十津川峡谷，桥隧已贯通)", "dist": "88 km", "time": "2小时15分", "toll": "0円", "mapCode": "478 221 004*22", "difficulty": "★★★☆☆", "park": "熊野本宫大社河原免费大停车场"},
                "dining": {"name": "茶房 珍重庵 本宫店", "specialty": "熊野名物 茶粥定食 & 温泉蛋荞麦", "score": "3.48", "cost": "1,200円"},
                "stay": {"economy": "汤之峰温泉 温泉民宿 峰", "comfort": "渡濑温泉 笹百合 (西日本最大大露天风吕)"}
            },
            {
                "day": 16,
                "title": "熊野本宫 ➔ 汤之峰温泉 (世界遗产壶汤)",
                "elev": "310m → 150m",
                "story": "深入开汤1800年的汤之峰温泉。体验世界唯一可入浴的世界文化遗产“壶汤（Tsuboyu，每天泉水变色七次）”，在温泉街公用小溪煮温泉蛋与番薯。",
                "modeA": {"line": "熊野御坊南海巴士 (本宫 ➔ 汤之峰 10分)", "pass": "刷IC卡", "cost": "320円", "tip": "壶汤在公营番所领号排队，限每次30分钟。"},
                "modeB": {"route": "县道241号 (仅3公里)", "dist": "3.5 km", "time": "8分", "toll": "0円", "mapCode": "478 193 881*00", "difficulty": "★★☆☆☆", "park": "汤之峰公营停车场 (免费)"},
                "dining": {"name": "汤之峰 温泉食堂", "specialty": "本地岩鱼盐烧 & 鹿肉刺身", "score": "3.46", "cost": "1,800円"},
                "stay": {"economy": "汤之峰 伊势屋 (古朴温泉宿)", "comfort": "汤之峰温泉 吾妻屋 (江户文人墨客投宿名宿)"}
            },
            {
                "day": 17,
                "title": "熊野速玉大社 ➔ 那智大社 ➔ 那智瀑布",
                "elev": "150m → 330m",
                "story": "参拜新宫熊野速玉大社与神宝馆；沿大门坂石阶古道漫步至熊野那智大社及青岸渡寺三重塔，远眺落差133米、日本第一水量的神体那智瀑布。",
                "modeA": {"line": "熊野交通巴士 (新宫 ➔ 胜浦 ➔ 那智山)", "pass": "熊野三山巴士2日券", "cost": "1,500円", "tip": "大门坂夫妇杉处可租借平安时代平安衣装体验。"},
                "modeB": {"route": "国道42号 那智胜浦道路", "dist": "46 km", "time": "1小时", "toll": "0円", "mapCode": "324 825 610*44", "difficulty": "★★☆☆☆", "park": "那智山防灾广场景观停车场 (800円)"},
                "dining": {"name": "那智胜浦 桂城 (Katsuragi)", "specialty": "纪伊胜浦港生鲜蓝鳍金枪鱼三色丼", "score": "3.62", "cost": "2,400円"},
                "stay": {"economy": "胜浦温泉 浦岛酒店 (洞窟海浪忘归洞风吕)", "comfort": "碧之岛 中之岛酒店 (私人游船登岛露天名宿)"}
            },
            {
                "day": 18,
                "title": "纪伊胜浦 ➔ 关西国际机场 (KIX) 离境",
                "elev": "330m → 15m",
                "story": "告别黑潮拍击的纪伊半岛，搭乘特急列车沿太平洋与纪伊水道海岸线北上，直接抵达关西国际机场办理出境归国。",
                "modeA": {"line": "JR 特急 Kuroshio (黑潮号) 直达日根野转关空", "pass": "关西广域铁路周游券", "cost": "6,100円", "tip": "黑潮号车窗左侧为壮丽太平洋海景，右侧为纪伊山地。"},
                "modeB": {"route": "阪和自动车道 ➔ 关西空港联络桥还车", "dist": "178 km", "time": "2小时30分", "toll": "4,320円 (ETC)", "mapCode": "802 001 552*33", "difficulty": "★☆☆☆☆", "park": "关西机场第1航站楼租车归还点"},
                "dining": {"name": "关西机场 鹤桥风月", "specialty": "关西风味豚玉御好烧 & 炒面", "score": "3.42", "cost": "1,500円"},
                "stay": {"economy": "返程航班", "comfort": "关西机场 日航酒店 (早班机备选)"}
            }
        ]
    },
    "route-2": {
        "id": "route-2",
        "title": "山阴神话海岸与濑户内海群岛：出云古国、石见银山、四国遍路与岛波海道",
        "shortTitle": "山阴神话与濑户内群岛",
        "durationDays": 17,
        "entryAirport": "冈山 (OKJ) / 关西 (KIX)",
        "exitAirport": "关西国际 (KIX)",
        "themeColor": "#BC4749",
        "accentColor": "#e76f51",
        "totalDistanceKm": 940,
        "trailWalkingKm": 28,
        "bestSeason": "3–6月（温和花季）、9–12月（海风宜人、冬季松叶蟹）",
        "winterNote": "冬季（1-2月）：气候温和少雪，山阴海岸（境港、松江、鸟取）迎来顶级松叶蟹解禁，出云大社冬云缭绕极具神圣庄严；濑户内海降水极少，阳光晴朗。",
        "autumnNote": "早秋（9-10月）：气候干爽舒适，避开夏季暴晒，最适合在岛波海道跨海大桥（生口岛、大三岛）进行绝景骑行，石见银山与吹屋红墙老街秋色浓郁。",
        "stops": [
            {"day": 1, "name": "仓敷美观地区", "lng": 133.7712, "lat": 34.5968, "elev": 20, "type": "heritage", "desc": "白壁土藏群、大原美术馆与民艺馆。"},
            {"day": 2, "name": "备中松山城 / 吹屋", "lng": 133.6219, "lat": 34.8086, "elev": 430, "type": "culture", "desc": "现存唯一山城天守与弁柄红墙矿山老街。"},
            {"day": 3, "name": "水都松江 / 宍道湖", "lng": 133.0505, "lat": 35.4723, "elev": 15, "type": "culture", "desc": "国宝松江城护城河游览船、宍道湖日落百景。"},
            {"day": 4, "name": "足立美术馆 (第一庭园)", "lng": 133.2250, "lat": 35.3780, "elev": 65, "type": "culture", "desc": "蝉联20余年日本第一枯山水横轴庭园。"},
            {"day": 5, "name": "神话之国·出云大社", "lng": 132.7550, "lat": 35.3670, "elev": 28, "type": "heritage", "desc": "全日本最大注连绳神乐殿、日御碕灯塔海崖。"},
            {"day": 6, "name": "世界遗产·石见银山", "lng": 132.4411, "lat": 35.1128, "elev": 210, "type": "heritage", "desc": "16世纪世界银矿遗址，龙源寺间步坑道。"},
            {"day": 7, "name": "温泉津温泉 (运银古港)", "lng": 132.3500, "lat": 35.0944, "elev": 35, "type": "onsen", "desc": "原貌保留温泉小镇、龙御前神社夜神乐。"},
            {"day": 8, "name": "津和野 (山阴小京都)", "lng": 131.7733, "lat": 34.4686, "elev": 160, "type": "culture", "desc": "殿町锦鲤水渠与太皷谷稻成千本鸟居。"},
            {"day": 9, "name": "长州藩·萩市城下町", "lng": 131.3991, "lat": 34.4103, "elev": 10, "type": "heritage", "desc": "明治维新摇篮、松下村塾与武家土墙夏柑树。"},
            {"day": 10, "name": "竹原 ➔ 坂道之城尾道", "lng": 133.2048, "lat": 34.4091, "elev": 45, "type": "culture", "desc": "千光寺文学坡道、远眺濑户内水道。"},
            {"day": 11, "name": "岛波海道跨海骑行", "lng": 133.0800, "lat": 34.3000, "elev": 80, "type": "nature", "desc": "连接本州与四国的大桥群，生口岛与大三岛。"},
            {"day": 12, "name": "大三岛大山祇神社", "lng": 133.0069, "lat": 34.2483, "elev": 35, "type": "heritage", "desc": "日本国宝刀剑甲胄宝库、伊东丰雄建筑馆。"},
            {"day": 13, "name": "松山·道后温泉本馆", "lng": 132.7867, "lat": 33.8522, "elev": 40, "type": "onsen", "desc": "三千年古汤木造三层楼阁与内子町木蜡老街。"},
            {"day": 14, "name": "四国喀斯特 (天狗高原)", "lng": 132.9500, "lat": 33.4833, "elev": 1400, "type": "nature", "desc": "云端石灰岩高山草原景观大道。"},
            {"day": 15, "name": "日本三大秘境·祖谷溪", "lng": 133.8167, "lat": 33.8667, "elev": 450, "type": "nature", "desc": "奥祖谷二重藤蔓编织古桥与落合集落古民家。"},
            {"day": 16, "name": "琴平·金刀比罗宫", "lng": 133.8153, "lat": 34.1856, "elev": 521, "type": "heritage", "desc": "1368阶神道朝圣道，海上守护神信仰。"},
            {"day": 17, "name": "丰岛/直岛 ➔ 关西返程", "lng": 135.2441, "lat": 34.4347, "elev": 15, "type": "transit", "desc": "丰岛美术馆水滴建筑，经濑户大桥返回关西机场。"}
        ],
        "daysDetail": [
            {
                "day": 1,
                "title": "关西/冈山抵港 ➔ 仓敷美观地区",
                "elev": "15m → 20m",
                "story": "自冈山或关西空港乘新干线直达仓敷。漫步仓敷川畔柳树白壁土藏群，参观日本首家西洋美术馆大原美术馆（收藏莫奈《睡莲》与格列柯名作）。",
                "modeA": {"line": "山阳新干线 + JR山阳本线", "pass": "山阳山阴7日周游券", "cost": "覆盖", "tip": "仓敷站步行至美观地区约10分钟。"},
                "modeB": {"route": "冈山空港 ➔ 山阳自动车道 仓敷IC", "dist": "24 km", "time": "30分", "toll": "750円", "mapCode": "19 632 018*55", "difficulty": "★☆☆☆☆", "park": "仓敷市营中央停车场"},
                "dining": {"name": "有邻庵 (仓敷)", "specialty": "幸福布丁 & 冈山生鸡蛋拌饭", "score": "3.54", "cost": "1,300円"},
                "stay": {"economy": "Dormy Inn 仓敷 (天然温泉阿知之汤)", "comfort": "仓敷常备宿 鹤形 (三百年商贾町家名宿)"}
            },
            {
                "day": 2,
                "title": "备中高梁山城 ➔ 吹屋红墙矿山町",
                "elev": "20m → 430m",
                "story": "北上探访日本现存天守中海拔最高的山城——备中松山城（秋冬清晨可见云海浮城）；午后深入全日本唯一由氧化铁红（弁柄）统一红墙石州瓦的吹屋故乡村。",
                "modeA": {"line": "JR伯备线特急Yakumo至备中高梁 ➔ 拼车观光计程车", "pass": "JR段覆盖", "cost": "2,200円 (计程车)", "tip": "备中高梁站可预约登山接驳车。"},
                "modeB": {"route": "冈山道贺阳IC ➔ 国道180号穿行吉备高原", "dist": "68 km", "time": "1小时25分", "toll": "1,100円", "mapCode": "329 881 245*11", "difficulty": "★★☆☆☆", "park": "吹屋千枚驻车场 (免费)"},
                "dining": {"name": "藤森食堂 (吹屋)", "specialty": "弁柄咖喱饭 & 冈山桃太郎地鸡荞麦", "score": "3.46", "cost": "1,100円"},
                "stay": {"economy": "高梁市 备中高梁车站酒店", "comfort": "吹屋古民家住宿 乐家"}
            },
            {
                "day": 3,
                "title": "水都松江城下町 ➔ 宍道湖日落",
                "elev": "430m → 15m",
                "story": "乘车翻越中国山地抵达面向日本海的松江。参观日本现存十二天守之一的国宝松江城，搭乘小型木造小舟巡游护城河；傍晚在岛根县立美术馆水畔欣赏宍道湖落日百景。",
                "modeA": {"line": "JR特急八云号 (Yakumo) 贯穿山地抵松江", "pass": "山阳山阴Pass覆盖", "cost": "覆盖", "tip": "松江堀川游览船有冬日被炉加热装置。"},
                "modeB": {"route": "米子道 ➔ 山阴自动车道 松江中央IC", "dist": "95 km", "time": "1小时35分", "toll": "2,350円", "mapCode": "163 294 510*33", "difficulty": "★☆☆☆☆", "park": "松江城大手前停车场"},
                "dining": {"name": "川京 (松江老铺)", "specialty": "宍道湖七珍料理 (大和蚬、白鱼、鲈鱼)", "score": "3.68", "cost": "3,800円"},
                "stay": {"economy": "松本野松江 Dormy Inn", "comfort": "玉造温泉 佳翠苑皆美 (日本古老美肌名汤)"}
            },
            {
                "day": 4,
                "title": "安来足立美术馆 (活生生的画卷)",
                "elev": "15m → 65m",
                "story": "参观连续二十余年被美国庭园杂志评为日本第一的足立美术馆。五万坪借景枯山水、苔庭、池庭透过落地玻璃框如同徐徐展开的横轴山水画。",
                "modeA": {"line": "JR山阴本线至安来站 ➔ 免费专用接驳巴士 (20分)", "pass": "JR段覆盖", "cost": "0円", "tip": "凭外国护照购票享专属优惠。"},
                "modeB": {"route": "山阴道 安来IC ➔ 县道45号", "dist": "28 km", "time": "35分", "toll": "580円", "mapCode": "252 642 108*77", "difficulty": "★☆☆☆☆", "park": "足立美术馆400位免费专用停车场"},
                "dining": {"name": "足立美术馆 茶室 大观庵", "specialty": "抹茶佐足立特制和菓子", "score": "3.55", "cost": "1,200円"},
                "stay": {"economy": "皆生温泉 芙蓉别馆", "comfort": "皆生温泉 游月 (全客房配海景露天风吕)"}
            },
            {
                "day": 5,
                "title": "古代神话起源：出云大社与日御碕",
                "elev": "65m → 28m",
                "story": "进入全日本八百万神明十月聚集的神话之国出云。参拜出云大社（主祭大国主大神，神乐殿悬挂重达5.2吨全日本最大注连绳），走访日御碕白色石造灯塔。",
                "modeA": {"line": "一畑电铁 (松江湖畔 ➔ 出云大社前站)", "pass": "买一日券或刷IC", "cost": "820円", "tip": "一畑电车是日本保存最完好的怀旧老电车之一。"},
                "modeB": {"route": "国道431号沿宍道湖与日本海行驶", "dist": "44 km", "time": "50分", "toll": "0円", "mapCode": "306 484 219*00", "difficulty": "★★☆☆☆", "park": "出云大社御本殿公营免费停车场"},
                "dining": {"name": "荒木屋 (出云最古老荞麦店)", "specialty": "三段割子荞麦面 (Warigo Soba)", "score": "3.63", "cost": "1,450円"},
                "stay": {"economy": "出云 月夜之兔 (全馆榻榻米商务温泉)", "comfort": "出云 佳云 (高格调和风温泉旅馆)"}
            },
            {
                "day": 6,
                "title": "世界文化遗产：石见银山 (大森町)",
                "elev": "28m → 210m",
                "story": "探访16-17世纪曾产出全球三分之一白银的世界文化遗产石见银山。租借e-Bike骑行于静谧的大森町老街，步入常年恒温12度的“龙源寺间步”古代采掘坑道。",
                "modeA": {"line": "JR山阴本线至大田市站 ➔ 石见交通路线巴士", "pass": "JR段覆盖", "cost": "680円 (巴士)", "tip": "景区核心区完全禁行私家车，骑车最自在。"},
                "modeB": {"route": "山阴道 大田IC ➔ 银山世界遗产中心换乘处", "dist": "52 km", "time": "1小时", "toll": "0円", "mapCode": "416 325 801*33", "difficulty": "★★☆☆☆", "park": "世界遗产中心免费停车场"},
                "dining": {"name": "群言堂 咖啡厅 (Gungendo)", "specialty": "里山酵素玄米时令野菜午间定食", "score": "3.58", "cost": "1,800円"},
                "stay": {"economy": "大森町 古民家宿 暮らす宿", "comfort": "他乡阿部家 (由石见银山文化复兴者主理的名宿)"}
            },
            {
                "day": 7,
                "title": "石见银山运银港 ➔ 温泉津温泉",
                "elev": "210m → 35m",
                "story": "抵达曾是运银出海港口的温泉津温泉。全镇列入重要传统建造物群，街道狭窄保留大正昭和木造旅馆风貌，在元汤体验强酸性药效泉，晚间观赏热血的石见神乐表演。",
                "modeA": {"line": "JR山阴本线 普通车至温泉津站 ➔ 徒步15分", "pass": "JR段覆盖", "cost": "420円", "tip": "龙御前神社周六晚间有传统神乐常态公演。"},
                "modeB": {"route": "国道9号沿日本海海岸西南下", "dist": "22 km", "time": "30分", "toll": "0円", "mapCode": "416 112 559*88", "difficulty": "★☆☆☆☆", "park": "温泉津港口公营免费停车场"},
                "dining": {"name": "温泉津 港食堂", "specialty": "日本海白身鱼煮付 & 鲜鱿鱼刺身", "score": "3.49", "cost": "1,600円"},
                "stay": {"economy": "温泉津 辉云庄 (温泉旅馆)", "comfort": "能登屋 旅馆 (大正时代木造建筑名宿)"}
            },
            {
                "day": 8,
                "title": "山阴小京都津和野 ➔ 萩市城下町",
                "elev": "35m → 10m",
                "story": "穿行中国山地抵津和野，漫步殿町千条锦鲤游弋的清渠；傍晚西抵面向日本海的长州藩大本营萩市，探访明治维新摇篮。",
                "modeA": {"line": "JR山阴本线 ➔ JR山口线 ➔ 特急巴士抵萩", "pass": "部分段覆盖", "cost": "2,100円", "tip": "萩市内最适宜在观光所租借自行车骑游。"},
                "modeB": {"route": "国道9号 ➔ 县道11号跨越山岭", "dist": "85 km", "time": "1小时40分", "toll": "0円", "mapCode": "379 248 110*00", "difficulty": "★★☆☆☆", "park": "萩城下町中央停车场 (310円)"},
                "dining": {"name": "津和野 沙罗之木 割烹", "specialty": "津和野角寿司 & 鲇鱼御饭", "score": "3.51", "cost": "1,500円"},
                "stay": {"economy": "萩市 芳和庄 (纯和风古民家)", "comfort": "萩 一本木之馆 萩温泉"}
            },
            {
                "day": 9,
                "title": "长州长门风云：松下村塾与武家白壁",
                "elev": "10m → 15m",
                "story": "游览吉田松阴讲学的松下村塾、木户孝允故居及高杉晋作诞生之地；在夏蜜柑果树探出白壁土墙的街巷慢行，品尝萩市见兰牛。",
                "modeA": {"line": "萩市内观光循环巴士 (Maru Bus)", "pass": "一日券", "cost": "500円", "tip": "两条环线涵盖所有维新史迹。"},
                "modeB": {"route": "萩市内自驾 ➔ 青海岛景观道", "dist": "32 km", "time": "45分", "toll": "0円", "mapCode": "379 339 501*44", "difficulty": "★☆☆☆☆", "park": "松阴神社免费大停车场"},
                "dining": {"name": "见兰牛 烧肉 绿 (Midori)", "specialty": "日本原种见岛牛后裔见兰牛极上烧肉", "score": "3.66", "cost": "3,800円"},
                "stay": {"economy": "萩之汤 萩皇家智能酒店", "comfort": "长门汤本温泉 大谷山庄 (国宾级名宿)"}
            },
            {
                "day": 10,
                "title": "安艺竹原 ➔ 坡道文学之城尾道",
                "elev": "15m → 45m",
                "story": "横穿本州抵达濑户内海。短暂停靠安艺小京都竹原老街，下午抵尾道。拾级而上千光寺山，俯瞰错落水道与停泊货轮，漫步猫之细道。",
                "modeA": {"line": "山阳新干线 ➔ JR山阳本线至尾道站", "pass": "Pass覆盖", "cost": "覆盖", "tip": "千光寺公园有索道缆车单程至山顶。"},
                "modeB": {"route": "山阳自动车道 尾道IC", "dist": "110 km", "time": "1小时30分", "toll": "2,850円", "mapCode": "48 248 102*33", "difficulty": "★☆☆☆☆", "park": "尾道站前地下停车场"},
                "dining": {"name": "朱华园 系谱：尾道拉面 喰海", "specialty": "濑户内小鱼酱油背脂尾道拉面", "score": "3.59", "cost": "850円"},
                "stay": {"economy": "尾道 Anago no Nedoko (町家旅舍)", "comfort": "ONOMICHI U2 (骑行概念海景精品酒店)"}
            },
            {
                "day": 11,
                "title": "岛波海道跨海骑行：生口岛与大三岛",
                "elev": "45m → 80m",
                "story": "踏上世界闻名的跨海自行车道“岛波海道”。租借专业公路车或e-Bike，骑过因岛大桥、生口桥抵生口岛，探访耕三寺与未来心之丘大理石庭园。",
                "modeA": {"line": "尾道港轮渡 + 岛波海道公共单车/巴士", "pass": "单车租金 (2,000円/天)", "cost": "2,500円", "tip": "沿途岛屿均设跨岛还车点，累了可随时改搭巴士。"},
                "modeB": {"route": "西濑户自动车道 (岛波海道跨海大桥群)", "dist": "45 km", "time": "50分", "toll": "1,980円 (ETC)", "mapCode": "133 118 402*11", "difficulty": "★★☆☆☆", "park": "各岛公路服务区与桥头观景点免费停车"},
                "dining": {"name": "生口岛 料理 汐待亭", "specialty": "濑户内海柠檬猪肉定食 & 鲜榨纯柠檬汁", "score": "3.52", "cost": "1,650円"},
                "stay": {"economy": "生口岛 濑户田民宿", "comfort": "Azumi Setoda (三井财阀古宅改建顶级名宿)"}
            },
            {
                "day": 12,
                "title": "大三岛大山祇神社 ➔ 今治跨入四国",
                "elev": "80m → 35m",
                "story": "前往爱媛县大三岛，参拜供奉日本总镇守的大山祇神社（其宝物馆收藏全日本八成列为国宝的古代武将甲胄与日本刀，包括源义经的铠甲）。跨来岛海峡大桥抵四国。",
                "modeA": {"line": "岛波特急巴士 (大三岛 ➔ 今治站)", "pass": "巴士单买", "cost": "1,150円", "tip": "来岛海峡大桥是世界第一座三连吊桥。"},
                "modeB": {"route": "西濑户道 来岛海峡SA展望台 ➔ 今治", "dist": "38 km", "time": "40分", "toll": "1,750円", "mapCode": "194 008 223*00", "difficulty": "★☆☆☆☆", "park": "大山祇神社专用免费停车场"},
                "dining": {"name": "今治 烤鸡皮 鸟林", "specialty": "今治铁板无签烤鸡皮 (Kawataki)", "score": "3.61", "cost": "2,200円"},
                "stay": {"economy": "今治 国际酒店", "comfort": "道后温泉 茶玻瑠 (露天风吕)"}
            },
            {
                "day": 13,
                "title": "松山道后温泉本馆 ➔ 木蜡内子町",
                "elev": "35m → 40m",
                "story": "体验三千年历史的木造神之汤道后温泉本馆；南下探访因木蜡贸易富庶的内子町，参观大正时代纯木造歌舞伎剧场内子座。",
                "modeA": {"line": "伊予铁道少爷列车 + JR予赞线特急宇和海号", "pass": "四国Pass覆盖", "cost": "覆盖", "tip": "内子站前租借自行车漫步八日市古街。"},
                "modeB": {"route": "松山自动车道 内子五十崎IC", "dist": "45 km", "time": "45分", "toll": "1,340円", "mapCode": "194 772 018*99", "difficulty": "★☆☆☆☆", "park": "内子町八日市游客停车场"},
                "dining": {"name": "下芳我邸 荞麦", "specialty": "木蜡富商豪宅内享用野草天妇罗荞麦", "score": "3.56", "cost": "1,600円"},
                "stay": {"economy": "内子町 织物古民家宿", "comfort": "道后温泉 ふなや (Funaya 390年天皇御宿老铺)"}
            },
            {
                "day": 14,
                "title": "翻越四国喀斯特 (天狗高原云端草原)",
                "elev": "40m → 1400m",
                "story": "沿四国天路攀升至海拔1400米的四国喀斯特高原。在绿草如茵的高原与白色石灰岩石林间远眺太平洋与濑户内海双重全景。",
                "modeA": {"line": "JR土赞线须崎站 ➔ 预订高原接驳计程车", "pass": "JR段覆盖", "cost": "4,000円 (拼车)", "tip": "非自驾者建议在松山参加当地一日散策团。"},
                "modeB": {"route": "国道440号 ➔ 县道383号 四国喀斯特景观道", "dist": "72 km", "time": "1小时45分", "toll": "0円", "mapCode": "723 381 200*55", "difficulty": "★★★★☆", "park": "天狗庄高原观景停车场 (免费)"},
                "dining": {"name": "星空之东风 (Hoshifuru) 高原餐厅", "specialty": "土佐褐毛和牛高原汉堡排定食", "score": "3.48", "cost": "1,600円"},
                "stay": {"economy": "高原星空露营木屋", "comfort": "高原之宿 天狗庄 (云海观星名所)"}
            },
            {
                "day": 15,
                "title": "深入日本三大秘境：祖谷溪与蔓藤桥",
                "elev": "1400m → 450m",
                "story": "穿行四国屋脊峡谷抵达平家落人避难秘境祖谷溪。走过用野生软枣猕猴桃藤蔓编制的“祖谷蔓桥（Iya Kazurabashi）”，探访悬崖上的小便小僧雕像。",
                "modeA": {"line": "JR土赞线特急 (阿波池田站转四国交通巴士)", "pass": "四国Pass覆盖铁道", "cost": "1,200円 (巴士)", "tip": "巴士穿行于狭窄险峻的祖谷溪深壑。"},
                "modeB": {"route": "国道32号转县道32号祖谷街道", "dist": "62 km", "time": "1小时30分", "toll": "0円", "mapCode": "357 398 012*44", "difficulty": "★★★★☆", "park": "祖谷蔓桥市营停车场 (500円)"},
                "dining": {"name": "蔓桥梦舞台 食堂", "specialty": "祖谷荞麦 (太切短荞麦) & 祖谷油豆腐烤串", "score": "3.50", "cost": "1,100円"},
                "stay": {"economy": "祖谷落合集落 古民家旅宿 桃源乡", "comfort": "祖谷温泉 秘境之宿 (乘专用缆车下降至谷底露天风吕)"}
            },
            {
                "day": 16,
                "title": "琴平金刀比罗宫 (1368阶神道朝圣)",
                "elev": "450m → 521m",
                "story": "北出四国峡谷抵达香川县琴平。参拜日本全国金刀比罗神社总本宫，拾级攀登785级至御本宫、1368级至奥社，远眺赞岐平原富士山形赞岐富士。",
                "modeA": {"line": "JR土赞线 特急南风号 ➔ 琴平站", "pass": "Pass覆盖", "cost": "覆盖", "tip": "参道起点有租借竹杖服务 (通常免费或100円)。"},
                "modeB": {"route": "高松自动车道 善通寺IC ➔ 琴平", "dist": "48 km", "time": "50分", "toll": "1,120円", "mapCode": "77 352 108*11", "difficulty": "★☆☆☆☆", "park": "琴平参道公营大型停车场 (500円)"},
                "dining": {"name": "琴平 虎屋 赞岐乌冬", "specialty": "手打生酱油乌冬配半熟天妇罗蛋", "score": "3.64", "cost": "650円"},
                "stay": {"economy": "琴平 樱之抄 (琴平温泉)", "comfort": "琴平 琴参阁 (讃岐飞天之馆)"}
            },
            {
                "day": 17,
                "title": "丰岛水滴美术馆 ➔ 濑户大桥 ➔ 关西离境",
                "elev": "521m → 15m",
                "story": "自高松港乘高速船登艺术之岛“丰岛”，探访内藤礼与西泽立卫设计的丰岛美术馆（纯白混凝土水滴建筑，风与泉水在此呼吸）；傍晚经濑户大桥跨海返回大阪关西机场。",
                "modeA": {"line": "丰岛轮渡 + JR濑户大桥线快速Marine Liner + 新干线", "pass": "周游券覆盖铁道段", "cost": "1,350円 (轮渡)", "tip": "丰岛美术馆需提前在官方预约入馆时段。"},
                "modeB": {"route": "高松港还车转公共交通，或驾车经濑户中央道返关西", "dist": "185 km", "time": "2小时30分", "toll": "4,850円 (ETC)", "mapCode": "802 001 552*33", "difficulty": "★☆☆☆☆", "park": "关西机场还车点"},
                "dining": {"name": "丰岛 岛厨 (Shima Kitchen)", "specialty": "丰岛本地渔获与蔬菜合奏定食", "score": "3.57", "cost": "1,980円"},
                "stay": {"economy": "归国航班", "comfort": "关西机场 酒店 (备选)"}
            }
        ]
    },
    "route-3": {
        "id": "route-3",
        "title": "奥羽山脉与北国秘汤：东北陆奥潮风步道、出羽三山与绳文遗址巡礼",
        "shortTitle": "奥羽秘汤与绳文森林",
        "durationDays": 16,
        "entryAirport": "仙台 (SDJ) / 东京 (HND/NRT)",
        "exitAirport": "东京羽田/成田 (HND/NRT)",
        "themeColor": "#386641",
        "accentColor": "#606c38",
        "totalDistanceKm": 820,
        "trailWalkingKm": 38,
        "bestSeason": "5–10月（避暑红叶、溪流徒步）、1–2月（豪雪秘汤树冰仅荐电车）",
        "winterNote": "冬季（1-2月）：极致银白雪国！藏王连峰树冰奇观、银山温泉大正浪漫夜景、乳头温泉乡鹤之汤雪中天然温泉风吕。气温常在-5°C以下，严禁无经验自驾雪道，全推新干线+巴士。",
        "autumnNote": "早秋（9-10月）：本州最早红叶盛宴！八甲田山高山草甸、十和田湖与奥入濑溪流在10月层林尽染，角馆黑板木墙映衬金黄与枫红，气候清凉干燥，徒步极佳。",
        "stops": [
            {"day": 1, "name": "仙台 / 盐釜水产市场", "lng": 140.8694, "lat": 38.2682, "elev": 35, "type": "food", "desc": "杜之都炭烤牛舌、盐釜海鲜仲卸市场自选丼。"},
            {"day": 2, "name": "世界遗产·平泉中尊寺", "lng": 141.1130, "lat": 38.9950, "elev": 90, "type": "heritage", "desc": "奥州藤原氏金色堂与毛越寺净土庭园。"},
            {"day": 3, "name": "民间传说故乡·远野", "lng": 141.5333, "lat": 39.3333, "elev": 280, "type": "culture", "desc": "《远野物语》河童传说与南部曲屋农家。"},
            {"day": 4, "name": "三陆复兴公园·净土之滨", "lng": 141.9806, "lat": 39.6500, "elev": 10, "type": "nature", "desc": "锯齿状海岸锯齿岩与白色流纹岩海湾。"},
            {"day": 5, "name": "陆奥潮风步道·八户", "lng": 141.5200, "lat": 40.5300, "elev": 45, "type": "trail", "desc": "种差海岸天然海滨草甸漫步与馆鼻岸壁早市。"},
            {"day": 6, "name": "十和田湖与奥入濑溪流", "lng": 140.9427, "lat": 40.5489, "elev": 400, "type": "nature", "desc": "14公里清流原生林徒步，瀑布云集长卷。"},
            {"day": 7, "name": "八甲田山 ➔ 酸汤温泉", "lng": 140.8497, "lat": 40.6544, "elev": 920, "type": "onsen", "desc": "三百年木造千人混浴白浊硫磺秘汤（设女性专属时段）。"},
            {"day": 8, "name": "青森县立美术馆 / 弘前", "lng": 140.7400, "lat": 40.8244, "elev": 25, "type": "culture", "desc": "奈良美智《青森犬》、弘前城现存天守。"},
            {"day": 9, "name": "五千年三内丸山绳文遗址", "lng": 140.6972, "lat": 40.8106, "elev": 40, "type": "heritage", "desc": "世界文化遗产绳文时代巨型木构立柱聚落。"},
            {"day": 10, "name": "五能线 ➔ 白神山地十二湖", "lng": 140.0500, "lat": 40.5500, "elev": 180, "type": "nature", "desc": "Resort白神号海景列车与深蓝青池原生林。"},
            {"day": 11, "name": "陆奥小京都·角馆", "lng": 140.5606, "lat": 39.5960, "elev": 65, "type": "heritage", "desc": "江户时代青柳家石黑家武家屋敷通。"},
            {"day": 12, "name": "田泽湖 ➔ 乳头温泉乡", "lng": 140.7891, "lat": 39.7997, "elev": 680, "type": "onsen", "desc": "日本最深高山湖与300年茅草秘汤鹤之汤七汤巡礼。"},
            {"day": 13, "name": "乳头温泉乡 (汤巡帖秘汤)", "lng": 140.8100, "lat": 39.8100, "elev": 720, "type": "onsen", "desc": "妙乃汤金汤银汤、大釜温泉、黑汤深度休整。"},
            {"day": 14, "name": "出羽三山：羽黑山石阶参道", "lng": 139.9700, "lat": 38.7050, "elev": 414, "type": "trail", "desc": "2446级石阶古杉道、国宝五重塔、修验道斋馆。"},
            {"day": 15, "name": "宝珠山立石寺 (山寺)", "lng": 140.4350, "lat": 38.3117, "elev": 360, "type": "heritage", "desc": "松尾芭蕉奥之细道名句诞生地，悬崖五大堂。"},
            {"day": 16, "name": "山形新干线直达东京返程", "lng": 139.7671, "lat": 35.6812, "elev": 20, "type": "transit", "desc": "翼号新干线穿行奥羽盆地直达东京站离境。"}
        ],
        "daysDetail": [
            {
                "day": 1,
                "title": "仙台机场入境 ➔ 盐釜市场 ➔ 仙台市",
                "elev": "5m → 35m",
                "story": "抵达东北都会仙台。乘仙石线至盐釜水产仲卸市场，购买400日元米饭套餐，在各滩位选购刚靠岸的天然本鲔鱼与赤贝制作自选海鲜丼；傍晚在仙台站品尝炭烤厚切牛舌。",
                "modeA": {"line": "JR仙石线 + 仙台机场Access线", "pass": "JR东日本东北Pass 5日券", "cost": "Pass覆盖", "tip": "仙台站JR东日本旅客服务中心激活通票。"},
                "modeB": {"route": "仙台机场提车 ➔ 三陆自动车道 盐釜IC", "dist": "34 km", "time": "40分", "toll": "720円", "mapCode": "110 502 331*22", "difficulty": "★☆☆☆☆", "park": "盐釜海鲜市场免费专用停车场"},
                "dining": {"name": "仙台 司 (Tsukasa) 牛舌西口名店", "specialty": "熟成炭烤厚切牛舌定食配麦饭牛尾汤", "score": "3.69", "cost": "2,400円"},
                "stay": {"economy": "Dormy Inn 仙台站前 (天然温泉萩之汤)", "comfort": "仙台威斯汀酒店 (俯瞰杜之都天际线)"}
            },
            {
                "day": 2,
                "title": "日本三景松岛 ➔ 世界遗产平泉中尊寺",
                "elev": "35m → 90m",
                "story": "晨游日本三景松岛瑞严寺；午后乘新干线北上岩手县平泉，探访平安时代末期奥州藤原氏构筑的佛教理想国——中尊寺金色堂（通体金箔覆盖国宝建筑）与毛越寺净土庭园。",
                "modeA": {"line": "东北新干线 (仙台 ➔ 一之关转东北本线至平泉)", "pass": "东北Pass覆盖", "cost": "覆盖", "tip": "平泉站提供“巡回巴士RunRun”串联所有世遗古迹。"},
                "modeB": {"route": "东北自动车道 平泉前泽IC", "dist": "88 km", "time": "1小时10分", "toll": "2,350円", "mapCode": "142 225 118*44", "difficulty": "★☆☆☆☆", "park": "中尊寺第一公营停车场 (500円)"},
                "dining": {"name": "平泉 芭蕉馆", "specialty": "平泉盛进碗子荞麦面 (Wanko Soba 12碗配山菜)", "score": "3.55", "cost": "1,850円"},
                "stay": {"economy": "平泉 温泉古民居 净土之里", "comfort": "花卷温泉 佳松园 (岩手顶级纯和风名宿)"}
            },
            {
                "day": 3,
                "title": "民间传说摇篮：远野盆地曲屋",
                "elev": "90m → 280m",
                "story": "深入日本民俗学之父柳田国男《远野物语》诞生地远野盆地。租借e-Bike游览马与人同住的“南部曲屋（L型农家建筑）”，探寻常坚寺后的河童渊清溪与五百罗汉岩刻。",
                "modeA": {"line": "JR釜石线 (花卷 ➔ 远野站)", "pass": "东北Pass覆盖", "cost": "覆盖", "tip": "釜石线为宫泽贤治《银河铁道之夜》的原型铁道。"},
                "modeB": {"route": "釜石自动车道 远野IC", "dist": "54 km", "time": "50分", "toll": "0円 (免费区间)", "mapCode": "298 441 229*00", "difficulty": "★☆☆☆☆", "park": "远野传承园免费停车场"},
                "dining": {"name": "远野 烤羊肉 元祖 白川", "specialty": "远野名物 成吉思汗烤生羊肉 (Jingisukan)", "score": "3.62", "cost": "2,100円"},
                "stay": {"economy": "远野 民宿 多佳代", "comfort": "远野 语之宿 (Kataribe之宿，听老妇讲述古老民间传说)"}
            },
            {
                "day": 4,
                "title": "三陆复兴国立公园：宫古净土之滨",
                "elev": "280m → 10m",
                "story": "穿行北上山地抵太平洋三陆海岸。探访宫古市净土之滨，白色流纹岩巨石与青松、蔚蓝海水构成天然日式净土画卷；登临北山崎200米锯齿状悬崖。",
                "modeA": {"line": "JR山田线至宫古 ➔ 三陆铁道Rias海岸观光线", "pass": "Pass覆盖部分", "cost": "1,100円", "tip": "三陆铁道是日本海岸景观列车典范。"},
                "modeB": {"route": "国道106号 (宫古盛冈横断道路) ➔ 三陆沿岸道路", "dist": "72 km", "time": "1小时15分", "toll": "0円 (国家免费高速段)", "mapCode": "286 238 411*77", "difficulty": "★★☆☆☆", "park": "净土之滨第1游客停车场"},
                "dining": {"name": "净土之滨 休息屋", "specialty": "三陆重茂半岛天然瓶装生海胆丼 (季节限定)", "score": "3.58", "cost": "3,200円"},
                "stay": {"economy": "宫古 净土之滨公园酒店", "comfort": "北山崎 绝壁海景旅宿"}
            },
            {
                "day": 5,
                "title": "陆奥潮风步道 ➔ 八户海鲜早市",
                "elev": "10m → 45m",
                "story": "徒步“陆奥潮风步道（Michinoku Coastal Trail）”最负盛名的种差海岸天然草坪段；下午抵达海港八户，在三六横丁居酒屋街品尝地酒与八户仙贝汁火锅。",
                "modeA": {"line": "JR八户线 (沿海行驶各站停车)", "pass": "东北Pass覆盖", "cost": "覆盖", "tip": "种差海岸站出站即可直达海滨草甸步道。"},
                "modeB": {"route": "三陆沿岸道路一路向北", "dist": "68 km", "time": "1小时", "toll": "0円", "mapCode": "84 002 119*55", "difficulty": "★☆☆☆☆", "park": "种差海岸免费游客信息中心停车场"},
                "dining": {"name": "八户 屋台村 三六横丁 (Miroku Yokocho)", "specialty": "八户前冲鲭鱼盐烤 & 仙贝汁土鸡火锅", "score": "3.56", "cost": "2,800円"},
                "stay": {"economy": "Dormy Inn 八户 (天然温泉)", "comfort": "八户 星野 青森屋 (东北祭典与睡魔文化名宿)"}
            },
            {
                "day": 6,
                "title": "奥入濑溪流 14km 徒步 ➔ 十和田湖",
                "elev": "45m → 400m",
                "story": "深入东北自然皇冠奥入濑溪流。从烧山徒步至子之口（全程14公里，亦可随巴士分段），穿梭于苔藓岩石、茂密山毛榉树冠与千变万化的瀑布群之间；傍晚宿十和田湖畔。",
                "modeA": {"line": "JR东北巴士 (八户站 ➔ 奥入濑溪流 ➔ 十和田湖)", "pass": "凭东北Pass免费乘坐", "cost": "覆盖", "tip": "巴士沿途每隔1-2公里设站，随走随上极其便利。"},
                "modeB": {"route": "国道102号沿奥入濑溪流慢速行驶", "dist": "46 km", "time": "1小时10分", "toll": "0円", "mapCode": "612 360 401*22", "difficulty": "★★☆☆☆", "park": "石户休息所停车场 (徒步起点)"},
                "dining": {"name": "奥入濑 苔藓咖啡厅", "specialty": "奥入濑山泉手冲咖啡 & 苔藓抹茶甜点", "score": "3.50", "cost": "1,200円"},
                "stay": {"economy": "十和田湖畔 旅宿 湖畔亭", "comfort": "星野集团 奥入濑溪流酒店 (溪流露天风吕)"}
            },
            {
                "day": 7,
                "title": "八甲田山 ➔ 三百年秘汤酸汤温泉",
                "elev": "400m → 920m",
                "story": "登八甲田山高山湿地；入住拥有三百年历史、列入国民保养温泉地第1号的“酸汤温泉（Sukayu Onsen）”。体验面积达160坪全罗汉柏木造的“千人风吕”强酸性白浊硫磺古汤。",
                "modeA": {"line": "JR东北巴士 (十和田湖 ➔ 酸汤温泉 ➔ 青森站)", "pass": "东北Pass免费乘坐", "cost": "覆盖", "tip": "千人风吕为混浴，但清晨与晚间固定设女性专属时段。"},
                "modeB": {"route": "国道103号 八甲田环状景观道", "dist": "32 km", "time": "45分", "toll": "0円", "mapCode": "704 532 108*00", "difficulty": "★★★☆☆", "park": "酸汤温泉专用大型停车场 (免费)"},
                "dining": {"name": "酸汤温泉 鬼面庵", "specialty": "酸汤名物 现打生荞麦面 & 温泉生姜关东煮", "score": "3.54", "cost": "1,100円"},
                "stay": {"economy": "酸汤温泉 汤治部 (自炊部朴素榻榻米)", "comfort": "酸汤温泉 本馆旅馆部 (一泊二食山菜膳)"}
            },
            {
                "day": 8,
                "title": "酸汤 ➔ 青森县立美术馆 ➔ 弘前",
                "elev": "920m → 25m",
                "story": "下山至青森市。造访与三内丸山遗址相融的白色壕沟建筑——青森县立美术馆（瞻仰奈良美智高达8.5米的巨型雕塑《青森犬》）；午后抵津轻藩城下町弘前。",
                "modeA": {"line": "JR巴士至青森站 ➔ JR奥羽本线至弘前", "pass": "东北Pass覆盖", "cost": "覆盖", "tip": "青森站旁古川市场可体验Nokkedon自选手撕丼。"},
                "modeB": {"route": "国道103号北下至青森 ➔ 国道7号至弘前", "dist": "48 km", "time": "1小时10分", "toll": "0円", "mapCode": "99 551 200*33", "difficulty": "★☆☆☆☆", "park": "弘前公园市营地下停车场"},
                "dining": {"name": "弘前 藤田纪念庭园 大正浪漫吃茶室", "specialty": "津轻本地苹果派品评套餐 (三款对比)", "score": "3.63", "cost": "1,400円"},
                "stay": {"economy": "Dormy Inn 弘前 (天然温泉苹果风吕)", "comfort": "弘前 露天之宿 石场旅馆 (津轻文化古宿)"}
            },
            {
                "day": 9,
                "title": "五千年绳文聚落：三内丸山遗址",
                "elev": "25m → 40m",
                "story": "探访世界文化遗产“北海道及北东北绳文遗址群”核心——三内丸山遗址。近距离观摩距今5000年的六根巨型栗木立柱建筑、大型半地穴式竖穴住居与精巧漆器骨角器。",
                "modeA": {"line": "弘南巴士 (弘前 ➔ 青森三内丸山)", "pass": "买单程票", "cost": "780円", "tip": "遗址附设“绳文Jomon时游馆”提供免费中文讲解器。"},
                "modeB": {"route": "浪冈IC ➔ 东北自动车道 青森IC", "dist": "35 km", "time": "40分", "toll": "850円", "mapCode": "99 521 884*11", "difficulty": "★☆☆☆☆", "park": "三内丸山遗址超大免费停车场"},
                "dining": {"name": "绳文餐厅 五花堂", "specialty": "绳文风味古代黑米饭 & 栗子猪肉汁定食", "score": "3.47", "cost": "1,350円"},
                "stay": {"economy": "弘前 艺术酒店", "comfort": "南田温泉 苹果乐园 (全馆苹果芳香名汤)"}
            },
            {
                "day": 10,
                "title": "五能线海景列车 ➔ 白神山地青池",
                "elev": "40m → 180m",
                "story": "乘坐全景观光列车“Resort白神号”，列车在津轻三味线现场演奏声中紧贴日本海波涛飞驰。在十二湖站下车，徒步进入世界自然遗产白神山地山毛榉原生林，探访宛如蓝墨水倾注的神奇“青池”。",
                "modeA": {"line": "JR五能线观光列车 Resort白神号 (需提前预订指定席)", "pass": "东北Pass免费覆盖指定席", "cost": "覆盖", "tip": "A侧座位全程直面绝美日本海！"},
                "modeB": {"route": "国道101号 黄金崎日落大道", "dist": "78 km", "time": "1小时40分", "toll": "0円", "mapCode": "795 221 008*33", "difficulty": "★★☆☆☆", "park": "十二湖养鱼场森林停车场 (400円)"},
                "dining": {"name": "十二湖 八峰物产馆", "specialty": "深浦名物 活烤枪乌贼 & 幻之鱼白神岩鱼", "score": "3.52", "cost": "1,600円"},
                "stay": {"economy": "深浦 黄金崎不老不死温泉 (海边极近铁锈红露天风吕)", "comfort": "秋田能代 纯和风旅宿"}
            },
            {
                "day": 11,
                "title": "陆奥小京都：角馆武家屋敷群",
                "elev": "180m → 65m",
                "story": "进入秋田县仙北地区。漫步“陆奥小京都”角馆，长达数公里的黑板土墙参道两侧林立着青柳家、石黑家、河原田家等江户高阶武士宅邸，探访桦细工（野山樱树皮工艺）工坊。",
                "modeA": {"line": "秋田新干线 小町号 (Komachi)", "pass": "东北Pass覆盖", "cost": "覆盖", "tip": "角馆站步行至武家屋敷约15分钟。"},
                "modeB": {"route": "秋田自动车道 大曲IC ➔ 国道105号", "dist": "62 km", "time": "1小时", "toll": "1,200円", "mapCode": "280 318 501*22", "difficulty": "★☆☆☆☆", "park": "角馆樱皮馆公营停车场 (500円)"},
                "dining": {"name": "角馆 樱之里 (Sakuranosato)", "specialty": "秋田比内地鸡特上亲子丼 & 稻庭手延乌冬", "score": "3.67", "cost": "1,850円"},
                "stay": {"economy": "角馆 町家客栈 宿屋", "comfort": "角馆 山庄 侘樱 (隐于栗林的茅草顶名宿)"}
            },
            {
                "day": 12,
                "title": "田泽湖 ➔ 乳头温泉乡 (鹤之汤)",
                "elev": "65m → 680m",
                "story": "环游日本最深湖泊田泽湖（深达423米，呈现神秘琉璃深蓝）；午后驶入八幡平国立公园腹地“乳头温泉乡”，入住拥有350年历史的“鹤之汤温泉”。体验茅草本阵与警备森严的天然混浴露天白汤。",
                "modeA": {"line": "羽后交通田泽湖环游巴士 ➔ 鹤之汤专用接驳车", "pass": "巴士分段买票", "cost": "1,400円", "tip": "鹤之汤古民家房型极度紧俏，需提前半年预订。"},
                "modeB": {"route": "国道341号 ➔ 乳头山麓林道", "dist": "28 km", "time": "40分", "toll": "0円", "mapCode": "729 448 012*99", "difficulty": "★★★☆☆", "park": "鹤之汤茅草门前免费停车场"},
                "dining": {"name": "鹤之汤 围炉里会席", "specialty": "炭火围炉里烤岩鱼 & 秋田名物山药丸子山菜锅", "score": "3.72", "cost": "一泊二食含"},
                "stay": {"economy": "乳头温泉乡 鹤之汤 二号馆 (榻榻米)", "comfort": "鹤之汤 本阵 (百年文化财茅草屋顶房间)"}
            },
            {
                "day": 13,
                "title": "乳头七汤巡礼 (金汤·银汤·黑汤)",
                "elev": "680m → 720m",
                "story": "持有住客专属的“汤巡帖（Yumeguri-cho）”，搭乘温泉乡巡回小巴穿梭于森林中的其余六汤：妙乃汤的溪流金色瀑布汤、大釜温泉的木造旧校舍汤与黑汤温泉的泥浆地热地狱。",
                "modeA": {"line": "乳头温泉乡 汤巡号接驳小巴", "pass": "汤巡帖 (2,000円含所有七汤入浴与巴士)", "cost": "2,000円", "tip": "一天内可尽情对比不同酸碱度与矿物泉质。"},
                "modeB": {"route": "各汤之间距离仅1-2公里，可驾车亦可林道徒步", "dist": "6 km", "time": "20分", "toll": "0円", "mapCode": "729 475 221*00", "difficulty": "★★☆☆☆", "park": "各秘汤旅馆专属车位"},
                "dining": {"name": "妙乃汤 餐厅", "specialty": "秋田名物米棒锅 (Kiritanpo Nabe)", "score": "3.58", "cost": "1,900円"},
                "stay": {"economy": "乳头温泉 休暇村 乳头温泉乡", "comfort": "妙乃汤 (现代和风现代治愈系名宿)"}
            },
            {
                "day": 14,
                "title": "修验道信仰圣地：出羽三山羽黑山",
                "elev": "720m → 414m",
                "story": "西南行至山形县庄内平原。参拜日本修验道圣地出羽三山之羽黑山。徒步登临拥有350年树龄巨杉林立的2446级石阶参道，瞻仰国宝羽黑山五重塔（东北最古老木塔）；在山顶三神合祭殿感受山岳信仰。",
                "modeA": {"line": "JR羽越本线至鹤冈站 ➔ 庄内交通羽黑山专线巴士", "pass": "JR段覆盖", "cost": "840円 (巴士)", "tip": "随身携带熊铃，山间杉林极为幽静古朴。"},
                "modeB": {"route": "日本海东北自动车道 庄内空港IC ➔ 羽黑山有料道路", "dist": "115 km", "time": "1小时50分", "toll": "1,450円", "mapCode": "352 238 001*44", "difficulty": "★★☆☆☆", "park": "羽黑山顶大鸟居公营免费停车场"},
                "dining": {"name": "羽黑山 斋馆 (Saikan)", "specialty": "出羽修验道正统精进料理 (胡麻豆腐与山菜月山笋)", "score": "3.66", "cost": "2,800円 (需预约)"},
                "stay": {"economy": "羽黑山 宿坊 宿坊大圣坊", "comfort": "汤野滨温泉 龟屋 (日本海落日露天风吕)"}
            },
            {
                "day": 15,
                "title": "宝珠山立石寺 (松尾芭蕉山寺)",
                "elev": "414m → 360m",
                "story": "乘车进入山形盆地。攀登千级石阶至松尾芭蕉写下“闲寂深潜岩石中，蝉声似水渗禅心”名句的宝珠山立石寺（山寺）。登上悬空于断崖之上的五大堂，极目远眺四山合围与田园峡谷。",
                "modeA": {"line": "JR仙山线 (山形 ➔ 山寺站 约20分)", "pass": "东北Pass覆盖", "cost": "覆盖", "tip": "山寺站出站徒步5分钟即抵登山口。"},
                "modeB": {"route": "山形自动车道 山形北IC ➔ 县道19号", "dist": "64 km", "time": "1小时10分", "toll": "1,200円", "mapCode": "62 508 120*11", "difficulty": "★☆☆☆☆", "park": "山寺登山口民间停车场 (500円)"},
                "dining": {"name": "山寺 对面石 荞麦", "specialty": "板荞麦 (Itasoba) & 山形名物炖芋头 (Imoni)", "score": "3.59", "cost": "1,500円"},
                "stay": {"economy": "山形站前 大和Roynet酒店", "comfort": "天童温泉 泷之汤 (山形名汤)"}
            },
            {
                "day": 16,
                "title": "山形 ➔ 山形新干线 ➔ 东京返程离境",
                "elev": "360m → 20m",
                "story": "在山形站品尝米泽牛便当，搭乘翼号（Tsubasa）山形新干线穿行于奥羽群山之间，直达东京站，换乘成田特急或东京单轨电车前往机场离境归国。",
                "modeA": {"line": "山形新干线 Tsubasa (约2小时45分直达东京)", "pass": "东北Pass覆盖", "cost": "覆盖", "tip": "车窗可最后回望藏王连峰雄浑山体。"},
                "modeB": {"route": "山形站异地还车转乘新干线，或经东北道自驾返东京", "dist": "360 km", "time": "4小时30分", "toll": "7,850円 (ETC)", "mapCode": "1 154 200*11", "difficulty": "★☆☆☆☆", "park": "东京站八重洲地下停车场还车"},
                "dining": {"name": "山形站 米泽牛 黄木 车站便当", "specialty": "极上米泽牛丝与牛排双拼铁道便当", "score": "3.61", "cost": "1,980円"},
                "stay": {"economy": "东京羽田/成田 归国航班", "comfort": "东京站大饭店 (The Tokyo Station Hotel 备选)"}
            }
        ]
    }
}

print(f"Routes spec compiled: {len(routes_spec)} routes.")

# Save compiled bundle for inspection or standalone use
with open('japan-travel-guide/routes_v2_spec.json', 'w', encoding='utf-8') as f:
    json.dump({
        "polygons": polygons,
        "routes": routes_spec
    }, f, ensure_ascii=False, indent=2)

print("routes_v2_spec.json written successfully.")
