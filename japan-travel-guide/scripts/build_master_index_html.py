# -*- coding: utf-8 -*-
"""
Builder script for japan-travel-guide/index.html (2026 Master Flagship).
Comprehensive Flagship Portal:
- Data Source: JAPAN_TRAVEL_GUIDE_2026_MASTER.md
- UI Architecture: v3.html baseline (43/57 split, D3 elevation probe, Leaflet)
- Visual Language & Components: v2.html (Noto fonts, Navy/Washi, route-meta-grid, seasonal-box)
- Header: Compact 50px fixed single-row with Top Route Drawer (17 routes, 4 categories)
- Zero Emojis: 100% SVG inline icons
"""

import json
import os
import re

OUTPUT_FILE = "japan-travel-guide/index.html"

# 1. Load routes from JSON
with open("japan-travel-guide/data/v4_routes.json", "r", encoding="utf-8") as f:
    v4_routes = json.load(f)
with open("japan-travel-guide/data/v3_routes.json", "r", encoding="utf-8") as f:
    v3_routes = json.load(f)
with open("japan-travel-guide/data/v2_routes.json", "r", encoding="utf-8") as f:
    v2_routes = json.load(f)
with open("japan-travel-guide/data/v2_extras.json", "r", encoding="utf-8") as f:
    v2_extras = json.load(f)

# 2. Extract Transit Table from MASTER.md
with open("japan-travel-guide/docs/guides/JAPAN_TRAVEL_GUIDE_2026_MASTER.md", "r", encoding="utf-8") as f:
    master_md = f.read()

m_table = re.search(r'(\| 序号 \| 区间走廊[\s\S]*?\n\n)', master_md)
transit_rows = []
if m_table:
    lines = m_table.group(1).strip().splitlines()
    header = [c.strip() for c in lines[0].split('|')[1:-1]]
    for l in lines[2:]:
        cols = [c.strip() for c in l.split('|')[1:-1]]
        if len(cols) == len(header):
            transit_rows.append(cols)

# Assemble Master ROUTES_DATA
ROUTES = {}

# 1. Framework
ROUTES["fa"] = {
    "id": "fa",
    "cat": "framework",
    "tag": "FRAMEWORK A · 18 DAYS · KANSAI, CHUBU & TOKYO",
    "title": "框架 A：本州黄金经典环线（关西 + 中部 + 东京）",
    "shortName": "关西中部东京黄金大环线",
    "badge": "框架 A · 18日落地黄金大环线",
    "desc": "关西机场(KIX)进 / 东京羽田(HND)出 · 首次赴日最稳妥选择。串联大阪城郭与市井美食、京都庭园与疏水、奈良东大寺、神户港湾、名古屋城、东京三大国家级博物馆群、镰仓江之电与箱根名汤。",
    "color": "#264653",
    "daysText": "18 日 / 17 晚",
    "maxElev": "940 m (箱根芦之湖/大涌谷)",
    "trailKm": "82.5 km (全线城市与名胜徒步)",
    "baseCostRMB": 15800,
    "pass": "SmartEX 早特早鸟折扣 (点对点单买) + 关西地区周游券",
    "transit": "东海道新干线 + JR特急 Haruka/Azusa + 阪急/京阪私铁",
    "ports": "关西机场 (KIX) 入境 → 东京羽田/成田离境 (单向不走回头路)",
    "bestMonths": [2, 3, 4, 5, 9, 10, 11],
    "winterAdvice": {
        "title": "1–2月 太平洋侧晴朗干燥与雪见名汤",
        "text": "本州太平洋沿岸冬季降雨少、空气通透，富士山远眺清晰度达到全年最高（超80%）；箱根芦之湖温泉一泊二食温暖治愈；京都与名古屋冬季游人较春秋大幅减少，名刹深幽。"
    },
    "autumnAdvice": {
        "title": "9–10月 初秋气候温润与城郭历史巡礼",
        "text": "9–10月关西与东京平原红叶尚未见顷（红叶普遍在11月中下旬），但气温20–25℃极其宜人；二条城、名古屋城本丸御殿金箔障壁画在秋阳下极尽灿烂，合羽桥刀匠与宇治抹茶正值佳期。"
    },
    "nodes": v4_routes["fa"]["nodes"]
}

ROUTES["fb"] = {
    "id": "fb",
    "cat": "framework",
    "tag": "FRAMEWORK B · 18 DAYS · NATURE & CONTEMPORARY ART",
    "title": "框架 B：自然与当代艺术生态（关西 + 濑户内 + 四国）",
    "shortName": "关西濑户内四国艺术生态",
    "badge": "框架 B · 18日当代艺术与海岛",
    "desc": "关西机场进出，或经高松/广岛机场 · 文艺与建筑爱好者的慢速海岛之旅。串联仓敷美观大原美术馆、直岛地中美术馆、丰岛水滴美术馆、小豆岛橄榄林、高松栗林公园、道后温泉古木楼阁与岛波海道跨海骑行。",
    "color": "#BC4749",
    "daysText": "18 日 / 17 晚",
    "maxElev": "480 m (四国屋岛/千光寺山)",
    "trailKm": "64.0 km (含岛波海道跨海骑行)",
    "baseCostRMB": 16500,
    "pass": "JR 关西&广岛铁路周游券 (5日) + 四国铁路周游券",
    "transit": "山阳新干线 + 快速 Marine Liner + 岛波海道巴士 + 四国汽船",
    "ports": "关西机场 (KIX) 进出，或经高松/广岛国际机场",
    "bestMonths": [3, 4, 5, 6, 9, 10, 11],
    "winterAdvice": {
        "title": "1–2月 濑户内海温和气候与道后暖汤",
        "text": "濑户内海四面环山，气候如地中海般温润少雨；避开夏季酷暑排队，直岛地中美术馆安藤忠雄光影沉静庄严；道后温泉本馆古木楼阁泡汤舒畅无比。"
    },
    "autumnAdvice": {
        "title": "9–10月 艺术跳岛黄金季与岛波跨海骑行",
        "text": "秋风习习，直岛草间弥生红南瓜与丰岛美术馆水滴在秋光中极具张力；租借公路车或 E-Bike 横跨岛波海道跨海大桥，俯瞰濑户内海翡翠色平静海面。"
    },
    "nodes": v4_routes["fb"]["nodes"]
}

ROUTES["fc"] = {
    "id": "fc",
    "cat": "framework",
    "tag": "FRAMEWORK C · 15 DAYS · KANTO DEPTH, MOUNTAINS & LAKES",
    "title": "框架 C：关东纵深与山岳湖泊（东京深度 + 箱根/日光/富士）",
    "shortName": "东京日光箱根富士关东纵深",
    "badge": "框架 C · 15日关东世界遗产与名岳",
    "desc": "东京(HND/NRT)同场进出 · 关东山海与江户遗产高效巡礼。串联东京三大国家级博物馆群、日光东照宫世界遗产雕刻极致、中禅寺湖、镰仓江之电古都海岸、箱根大涌谷名汤与富士五湖逆富士绝景。",
    "color": "#386641",
    "daysText": "15 日 / 14 晚",
    "maxElev": "1,269 m (奥日光中禅寺湖畔)",
    "trailKm": "58.0 km (山岳与步道徒步)",
    "baseCostRMB": 14200,
    "pass": "东武日光周游券 (NIKKO PASS) + 小田急箱根周游券 + 富士山周游券",
    "transit": "东武特急 Spacia X + 小田急浪漫特快 + JR中央线特急 Azusa",
    "ports": "东京羽田 (HND) 或成田 (NRT) 国际机场同场进出",
    "bestMonths": [2, 3, 4, 5, 9, 10, 11],
    "winterAdvice": {
        "title": "1–2月 富士山清晰倒影与奥日光冰瀑",
        "text": "冬季关东干燥无云，河口湖'逆富士'倒影几率超过 80%；奥日光华严瀑布形成晶莹剔透之巨型冰瀑；箱根露天风吕热气蒸腾，眺望雪山。"
    },
    "autumnAdvice": {
        "title": "9–10月 奥日光高海拔彩林与湘南海岸",
        "text": "10月中旬奥日光汤之湖与战场之原率先迎来金黄落叶松与红叶；镰仓江之电沿湘南海岸行驶，夕阳下的相模湾海天一色，富士山暮色剪影迷人。"
    },
    "nodes": v4_routes["fc"]["nodes"]
}

# 2. Classics
ROUTES["r1_gt"] = {
    "id": "r1_gt",
    "cat": "classic",
    "tag": "ROUTE 01 · GOLDEN TRIANGLE · TOKYO, NAGOYA, KYOTO & OSAKA",
    "title": "东海道黄金三角经典走廊：东京都市文明、尾张名古屋工业历史、关西古都名刹与宇治茶乡环线",
    "shortName": "东海道黄金三角走廊",
    "badge": "经典 01 · 东海道黄金三角 (18日)",
    "desc": "东京(HND/NRT)进 / 大阪关西(KIX)出 · 贯通日本政治经济文化最核心大动脉。串联东京三大国家级博物馆群与江户下町刀匠、镰仓江之电古都海岸、战国尾张名城与热田神宫、JR东海磁浮铁道馆、京都千年名刹与宇治茶乡、大和奈良大佛与大阪水都商贾美食。",
    "color": "#264653",
    "daysText": "18 日 / 17 晚",
    "maxElev": "115 m (犬山城木曾川崖顶)",
    "trailKm": "52.0 km (名胜步道)",
    "baseCostRMB": 17800,
    "pass": "SmartEX 早特早鸟折扣 (点对点单买) + 地铁一日券",
    "transit": "东海道新干线 Nozomi + 名铁特急 + 近铁特急 + JR奈良线快速",
    "ports": "东京羽田/成田入境 → 大阪关西出境 (单向不走回头路)",
    "bestMonths": [3, 4, 5, 9, 10, 11],
    "winterAdvice": {
        "title": "1–2月 冬日晴空古都名刹与尾张暖锅",
        "text": "本州太平洋沿岸冬季降水稀少，阳光灿烂，步行舒适度极高；京都南禅寺热汤豆腐、名古屋蓬莱轩热鳗鱼饭三吃暖胃解乏；避开春秋季百万大军拥挤。"
    },
    "autumnAdvice": {
        "title": "9–10月 秋高气爽城郭历史与茶道巡礼",
        "text": "9–10月气候温和适宜日均2万步漫步；探访热田神宫信长塀、名古屋城本丸御殿、宇治平等院凤凰堂及抹茶名家，感受日本核心三大都会圈的古今共振。"
    },
    "nodes": [
        {
            "day": "D1–D3",
            "name": "东京：上野国立博物馆群、合羽桥道具街与江户下町文化",
            "pref": "东京都 (台东区/墨田区)",
            "lat": 35.7188, "lng": 139.7765, "elev": 24, "distKm": 0,
            "exp": "【江户艺术与职人工艺】羽田/成田入境。漫步谷中银座下町古巷；参访上野【东京国立博物馆】（本馆考古与法隆寺宝物馆，日本最高规格文化宝库）；前往合羽桥道具街探访拥有百年历史的手工锻造料理刀坊；暮色中游览两国江户东京历史区与浅草寺。",
            "public": {
                "line": "京成Skyliner / 成田特急N'EX直达市区 + 都营大江户线 / JR山手线",
                "costJPY": 3200,
                "alert": "在JR车站用 Apple Wallet 绑定充值 Suica 或在售票机购买 Welcome Suica；东博建议预留至少 3 小时。"
            },
            "drive": {
                "line": "首都高速都心环线(C1) → 上野线 → 上野公园地下停车场",
                "costJPY": 1950,
                "mapCode": "738 884*77",
                "alert": "东京市区道路复杂极度拥堵且停车费昂贵（约 600-800 JPY/小时），强烈建议使用公共交通。"
            },
            "food": "浅草 驹形前川 炭火烤鳗鱼重 & 合羽桥老铺 手打荞麦面",
            "tabelog": "3.68",
            "stay": "Dormy Inn Premium 涩谷神宫前 / 谷根千设计町家民宿 (人均 9,500 JPY)",
            "airbnb": "谷根千昭和排屋改建和风独栋，步行至东博 15 分钟，带日式厨房与静谧小庭院"
        },
        {
            "day": "D4–D5",
            "name": "镰仓与江之岛：圆觉寺枯山水、高德院大佛与江之电海岸线",
            "pref": "神奈川县 (镰仓市/藤泽市)",
            "lat": 35.3191, "lng": 139.5467, "elev": 18, "distKm": 54,
            "exp": "【武家政权发祥与湘南海岸】自东京搭乘横须贺线南下镰仓。参访北镰仓临济宗大本山【圆觉寺】与【建长寺】禅宗枯山水；参拜高德院青铜大佛；搭乘百年【江之电】沿湘南海岸穿行至长谷与镰仓高校前，远眺相模湾落日与富士山剪影。",
            "public": {
                "line": "JR 横须贺线 (东京/品川 → 镰仓约55分) + 江之岛电铁 (全线通票 800 JPY)",
                "costJPY": 1820,
                "alert": "江之电长谷站至镰仓高校前为热门路段，建议早晨 8:30 前搭乘避开拍照人潮。"
            },
            "drive": {
                "line": "首都高速湾岸线 → 横滨横须贺道路 → 朝比奈IC → 镰仓街道",
                "costJPY": 2600,
                "mapCode": "187 340 181*44",
                "alert": "镰仓由比之滨与长谷周边道路极狭窄且周末易封路，外地车牌停车极其困难。"
            },
            "food": "镰仓小町通 吻仔鱼双色盖饭 (Shirasu-don) & 抹茶冰淇淋",
            "tabelog": "3.55",
            "stay": "镰仓王子大饭店 (相模湾海景) / 由比之滨和风古民家 Airbnb (人均 11,000 JPY)",
            "airbnb": "由比之滨独栋海滨木屋，步行 3 分钟即达沙滩，可观赏相模湾落日"
        },
        {
            "day": "D6–D7",
            "name": "尾张名古屋：战国名城本丸御殿、热田神宫草薙剑与磁浮·铁道馆",
            "pref": "爱知县 (名古屋市)",
            "lat": 35.1856, "lng": 136.8991, "elev": 35, "distKm": 360,
            "exp": "【天下统一霸业与现代工业之心】乘东海道新干线 Nozomi 号直达名古屋。登临名古屋城，深度考察 2018 年完成原寸复原的战国巅峰【本丸御殿】（狩野派金箔障壁画金碧辉煌）；参拜日本三大神宫之一【热田神宫】（供奉三神器之草薙神剑，瞻仰织田信长桶狭间战前祈愿修筑的信长塀）；下午参观【磁浮·铁道馆】（JR东海技术殿堂，陈列自蒸汽机车到 L0 系超导磁浮列车等 39 辆真实车辆）。",
            "public": {
                "line": "东海道新干线 Nozomi (品川 → 名古屋 1小时36分) + 名古屋市营地下铁",
                "costJPY": 11300,
                "alert": "新干线大件行李（161-250cm）务必提前通过 SmartEX 免费预约最后一排专属行李席。"
            },
            "drive": {
                "line": "东名高速道路 → 名古屋高速都心环线 → 锦桥出口",
                "costJPY": 8900,
                "mapCode": "4 348 301*22",
                "alert": "名古屋百万人大都市交通流量极大，市中心名站与荣商圈推荐停放大厦立体车库。"
            },
            "food": "热田神宫蓬莱轩 本店 独家鳗鱼饭三吃 (Hitsumabushi) & 风来坊手羽先",
            "tabelog": "3.78",
            "stay": "名古屋万豪酒店 / 大须商圈高层现代公寓 Airbnb (人均 8,500 JPY)",
            "airbnb": "荣商业区外围现代高层 Mansion 2LDK 公寓，开放式全功能厨房，带独立双卫浴"
        },
        {
            "day": "D8",
            "name": "国宝犬山城：现存最古木造天守、如庵茶室与木曾川峭壁",
            "pref": "爱知县 (犬山市)",
            "lat": 35.3883, "lng": 136.9392, "elev": 115, "distKm": 385,
            "exp": "【白帝木造遗制与茶道清修】搭名铁特急前往犬山。攀登日本现存十二天守中最古老的【犬山城】（天文六年建造木造四重六阶天守，立于木曾川险峻绝壁之上）；漫步名铁有乐苑，参访织田信长之弟织田有乐斋所建国宝三大茶室之一【如庵】；漫步城下町品尝酱油焦香五平饼。",
            "public": {
                "line": "名铁犬山线 特急 / 快速急行 (名铁名古屋 → 犬山游园站 26分)",
                "costJPY": 600,
                "alert": "在犬山游园站下车沿木曾川步行 12 分钟至天守，风景远胜犬山站直达。"
            },
            "drive": {
                "line": "名古屋高速小牧线 → 国道41号 → 犬山城下町专用停车场",
                "costJPY": 1200,
                "mapCode": "98 316 422*15",
                "alert": "城下町周末禁止机动车驶入，请将车辆停靠在木曾川沿岸营运停车场。"
            },
            "food": "犬山城下町 炭烤五平饼 & 鲇鱼盐烤定食",
            "tabelog": "3.52",
            "stay": "英迪格酒店 犬山有乐苑 / 犬山都酒店 (人均 9,800 JPY)",
            "airbnb": "木曾川畔古民家民宿，推窗即眺望犬山城天守夜景与江水流淌"
        },
        {
            "day": "D9–D11",
            "name": "千年王城京都：清水寺音羽舞台、二条城鹂鸣地板与岚山天龙寺",
            "pref": "京都府 (京都市)",
            "lat": 35.0116, "lng": 135.7681, "elev": 52, "distKm": 510,
            "exp": "【平安王城与禅宗美学巅峰】新干线 34 分钟直达京都。清晨探访【清水寺】悬空音羽舞台与二年坂青石街；考察德川家康筑造的【二条城】（二之丸御殿走廊鹂鸣防刺客地板与大政奉还现场）；前往洛西岚山跨越渡月桥，步入世界遗产【天龙寺】曹源池回游式庭园，深入常寂光寺与嵯峨野野宫竹林。",
            "public": {
                "line": "东海道新干线 Nozomi (名古屋 → 京都 34分) + 京都市营地下铁/市巴士",
                "costJPY": 5910,
                "alert": "京都巴士严格后门上车刷IC卡或取整理券，前门下车付费；车未停稳切勿走动！"
            },
            "drive": {
                "line": "名神高速道路 (小牧IC → 京都东IC 约1小时20分)",
                "costJPY": 3480,
                "mapCode": "7 618 204*33",
                "alert": "京都历史核心区严禁自驾，路狭车多且单行道密布，市中心停车费极高。"
            },
            "food": "南禅寺 顺正 传统汤豆腐会席 & 祇园 鲭姿寿司",
            "tabelog": "3.72",
            "stay": "西阵百年京町家独栋整租 Airbnb / 三井花园饭店京都站前 (人均 12,000 JPY)",
            "airbnb": "西阵纺织区 100 年历史独栋京町家整租，配桧木大浴缸、枯山水私人坪庭与急须茶室"
        },
        {
            "day": "D12",
            "name": "宇治：世界遗产平等院凤凰堂净土佛国与抹茶茶道体验",
            "pref": "京都府 (宇治市)",
            "lat": 34.8893, "lng": 135.8078, "elev": 28, "distKm": 530,
            "exp": "【净土佛国与茶之极意】清晨搭 JR 奈良线直抵伏见稻荷大社（清晨 7 点避开人潮漫步千本鸟居）；随后南下宇治，参访十元硬币背面图案实体【平等院凤凰堂】（平安时代藤原赖通建造的西方极乐世界木造化身，临阿字池倒影绝美）；探访丸久小山园或中村藤吉宇治本店，亲历手工点抹茶与茶道礼仪。",
            "public": {
                "line": "JR 奈良线 区间快速 (京都站 → 宇治站 17分 单程仅需 240 JPY)",
                "costJPY": 480,
                "alert": "伏见稻荷站与宇治站车次每小时多达 6 班，直接刷 Suica/ICOCA 即可进出站。"
            },
            "drive": {
                "line": "京滋绕道 (宇治西IC) → 宇治川沿岸市营停车场",
                "costJPY": 800,
                "mapCode": "11 125 301*77",
                "alert": "宇治平等院表参道属于行人专用街区，车辆须停在宇治川对岸公营停车场。"
            },
            "food": "中村藤吉 宇治本店 生茶生巧克力果冻抹茶竹筒甜品 & 宇治抹茶茶麦面",
            "tabelog": "3.74",
            "stay": "花敷水馆 / 宇治川畔设计民宿 (人均 8,500 JPY)",
            "airbnb": "宇治川沿岸和风双层木屋，步行 5 分钟到平等院表参道，夜听宇治川流水淙淙"
        },
        {
            "day": "D13–D14",
            "name": "大和古代原点奈良：东大寺卢舍那大佛与斑鸠法隆寺",
            "pref": "奈良县 (奈良市/生驹郡)",
            "lat": 34.6851, "lng": 135.8048, "elev": 75, "distKm": 565,
            "exp": "【飞鸟古风与南都大寺】自宇治南下古都奈良。探访奈良公园神鹿群落与【春日大社】朱红回廊；参拜【东大寺】（世界最大木造古建筑大佛殿，高 15m 的青铜卢舍那大佛令人肃穆）；前往斑鸠之里参访【法隆寺】（圣德太子建于公元 607 年，世界现存最古老木造建筑群与玉虫厨子国宝）。",
            "public": {
                "line": "JR 奈良线 / 近铁奈良线特急 + 奈良交通斑鸠巴士一日券",
                "costJPY": 1500,
                "alert": "近铁奈良站距离奈良公园步行仅 3 分钟；法隆寺推荐搭 JR 大和路线至法隆寺站转巴士。"
            },
            "drive": {
                "line": "京奈和自动车道 → 国道24号 → 奈良公园高畑停车场",
                "costJPY": 1100,
                "mapCode": "11 354 102*00",
                "alert": "奈良公园附近野生鹿常走上行车道，驾车务必极其谨慎低速慢行。"
            },
            "food": "奈良町 志津香 釜饭 (釜めし) & 柿叶寿司 (Kaki-no-ha sushi)",
            "tabelog": "3.66",
            "stay": "奈良万叶若草旅馆 / 奈良町武家排屋整租 Airbnb (人均 9,000 JPY)",
            "airbnb": "奈良町百年町家整租，保留古式灶台与榻榻米天井，出门即是格子门手作街"
        },
        {
            "day": "D15–D18",
            "name": "大阪水都：大阪城天守石垣、难波道顿堀美食与关西机场离境",
            "pref": "大阪府 (大阪市/泉佐野市)",
            "lat": 34.6873, "lng": 135.5262, "elev": 15, "distKm": 580,
            "exp": "【商贾浪速之魂与跨国枢纽】近铁快速 36 分钟抵大阪难波。考察【大阪城】丰臣秀吉巨型石垣与极乐桥；参访中之岛近代红砖公会堂与大阪中之岛美术馆；漫步心斋桥、道顿堀与木津水产市场；梅田蓝天大厦空中庭园眺望大阪湾；经难波搭乘南海特急 Rapi:t 或天王寺搭乘 JR 特急 Haruka 号直奔关西机场(KIX)出境。",
            "public": {
                "line": "近铁难波·奈良线快速急行 + 南海特急 Rapi:t (难波 → 关西机场 38分)",
                "costJPY": 2150,
                "alert": "出境前完成退税与免税核销；提前出示 Visit Japan Web 海关单一码；关西机场免税店预留至少 2 小时。"
            },
            "drive": {
                "line": "阪神高速1号环状线 → 阪神高速4号湾岸线至关西国际机场",
                "costJPY": 2400,
                "mapCode": "1 285 410*55",
                "alert": "关西机场为人工岛跨海大桥，过桥费单程约 940 JPY；机场航站楼支持异地还车。"
            },
            "food": "难波木津市场 现开海胆金枪鱼双色海鲜丼 & 通天阁 元祖炸串达摩",
            "tabelog": "3.71",
            "stay": "大阪南海瑞士酒店 (难波站上盖) / 难波高层现代公寓 Airbnb (人均 9,800 JPY)",
            "airbnb": "难波南侧现代化 Mansion 高级公寓，直达关西机场电车，配烘干一体洗衣机与大阳台"
        }
    ]
}

ROUTES["r1_v3"] = {
    "id": "r1_v3",
    "cat": "classic",
    "tag": "ROUTE 02 · TOKYO CULTURE, HOKUSAI UKIYO-E & HOKURIKU CRAFTS",
    "title": "本州脊梁与大师溯源：东京博物馆群、浮世绘《富岳三十六景》、信越北陆加贺物语与关西名刹纵贯线",
    "shortName": "富岳三十六景·北陆信越加贺",
    "badge": "经典 02 · 葛饰北斋与信越加贺 (18日)",
    "desc": "东京(HND/NRT)进 / 大阪关西(KIX)出 · 溯源浮世绘大师葛饰北斋《富岳三十六景》灵感线，串联东京国立博物馆与墨田北斋馆、信州小布施晚年肉笔画圣地、国宝松本城天守、阿尔卑斯上高地、五箇山合掌造、加贺百万石工艺与关西千年名刹。",
    "color": "#3D5A80",
    "daysText": "18 日 / 17 晚",
    "maxElev": "1,505 m (上高地梓川)",
    "trailKm": "42.0 km",
    "baseCostRMB": 19800,
    "pass": "北陆拱形铁路周游券 (7日) + Alpico 上高地联票",
    "transit": "北陆新干线 + 特急 Azusa + 特急雷鸟号 + 浓飞巴士",
    "ports": "东京成田/羽田进 → 大阪关西出",
    "bestMonths": [4, 5, 6, 9, 10, 11],
    "winterAdvice": {
        "title": "1–2月 豪雪合掌造与加贺兼六园雪吊挂",
        "text": "金泽兼六园雪吊挂防雪景观绝美非凡；五箇山相仓合掌造雪屋宛如童话世界；松本城黑色天守覆雪庄严；北陆加能蟹（红楚蟹）正值肥美季节。"
    },
    "autumnAdvice": {
        "title": "9–10月 信州小布施栗香与北阿尔卑斯彩林",
        "text": "9月下旬小布施新栗采收，栗子糯米饭香气扑鼻；上高地梓川清流与涸泽圈谷高山草甸染红；轻井泽落叶松与云场池秋景如诗如画。"
    },
    "nodes": v3_routes["r1"]["nodes"]
}

ROUTES["r1_v2"] = {
    "id": "r1_v2",
    "cat": "classic",
    "tag": "ROUTE 03 · CENTRAL ALPS, HOKURIKU & KUMANO KODO",
    "title": "本州脊梁与千年古道：中山道宿场、北陆工艺、纪伊半岛熊野古道纵贯线",
    "shortName": "中山道宿场·熊野古道纵贯线",
    "badge": "经典 03 · 中山道与熊野古道 (18日)",
    "desc": "名古屋(NGO)进 / 大阪关西(KIX)出 · 避开常规京阪人潮，纵贯木曾路森林石板古道、飞驒五箇山合掌聚落、加贺百万石金泽、大和飞鸟古京与纪伊山脉神佛圣地熊野古道中边路。",
    "color": "#1B4332",
    "daysText": "18 日 / 17 晚",
    "maxElev": "1,505 m (上高地梓川)",
    "trailKm": "38.5 km",
    "baseCostRMB": 19480,
    "pass": "北陆拱形铁路周游券 + 浓飞巴士 + JR 关西广域周游券",
    "transit": "特急 Shinano + 北陆新干线 + 特急 Kuroshio + 路线巴士",
    "ports": "名古屋/东京进 → 大阪关西出",
    "bestMonths": [4, 5, 6, 10, 11],
    "winterAdvice": v2_extras["r1"]["winterAdvice"],
    "autumnAdvice": v2_extras["r1"]["autumnAdvice"],
    "nodes": v2_routes["r1"]["nodes"]
}

ROUTES["r2_v3"] = {
    "id": "r2_v3",
    "cat": "classic",
    "tag": "ROUTE 04 · SAN-IN MYTH COAST, SHIMANAMI & SHIKOKU",
    "title": "山阴神话海岸与濑户内海群岛：出云古国、石见银山、岛波海道与四国秘境环线",
    "shortName": "山阴出云神话·濑户内群岛",
    "badge": "经典 04 · 山阴神话与四国环线 (17日)",
    "desc": "冈山进 / 高松或大阪出 · 横跨日本海侧出云大社神话古国、世界遗产石见银山矿山、津和野小京都，穿越岛波海道跨海桥梁系统，探访夏目漱石道后温泉与赞岐金刀比罗宫。",
    "color": "#BC4749",
    "daysText": "17 日 / 16 晚",
    "maxElev": "430 m (吹屋铜山/金刀比罗宫)",
    "trailKm": "32.0 km",
    "baseCostRMB": 18200,
    "pass": "JR 山阳&山阴铁路周游券 (7日) + 四国铁路周游券",
    "transit": "山阳新干线 + JR特急 Yakumo + 岛波海道高速巴士 + 琴电",
    "ports": "冈山或广岛进 → 高松或大阪关西出",
    "bestMonths": [4, 5, 9, 10, 11],
    "winterAdvice": v2_extras["r2"]["winterAdvice"],
    "autumnAdvice": v2_extras["r2"]["autumnAdvice"],
    "nodes": v3_routes["r2"]["nodes"]
}

ROUTES["r3_v3"] = {
    "id": "r3_v3",
    "cat": "classic",
    "tag": "ROUTE 05 · OU MOUNTAINS, SANRIKU COAST & TOHOKU ONSEN",
    "title": "奥羽山脉与北国秘汤：三陆潮风步道、奥入濑溪流、白神山地与出羽三山巡礼",
    "shortName": "东北奥羽·三陆潮风与秘汤",
    "badge": "经典 05 · 奥羽山脉与北国秘汤 (16日)",
    "desc": "仙台或东京进 / 新青森或秋田出 · 纵穿陆奥东北六县的原始山毛榉林、太平洋三陆海岸绝壁、奥入濑溪流、世界遗产白神山地青池、八甲田酸汤温泉与乳头温泉乡鹤之汤白浊名汤。",
    "color": "#386641",
    "daysText": "16 日 / 15 晚",
    "maxElev": "920 m (八甲田山酸汤温泉)",
    "trailKm": "46.0 km",
    "baseCostRMB": 19600,
    "pass": "JR 东日本铁路周游券 (东北地区5日券)",
    "transit": "东北/秋田新干线 + JR五能线 Resort 白神号 + 路线巴士",
    "ports": "仙台或东京进 → 青森或秋田离境",
    "bestMonths": [5, 6, 9, 10, 11],
    "winterAdvice": v2_extras["r3"]["winterAdvice"],
    "autumnAdvice": v2_extras["r3"]["autumnAdvice"],
    "nodes": v3_routes["r3"]["nodes"]
}

# 3. Themes
ROUTES["t1"] = {
    "id": "t1",
    "cat": "theme",
    "tag": "THEME 01 · KYOTO GARDENS & TRADITIONAL CRAFTS",
    "title": "路线 1：京都「庭园与传统工艺」深度（5 日，造园 + 染织/陶艺）",
    "shortName": "京都庭园与传统工艺",
    "badge": "专题 01 · 京都造园与工艺深度",
    "desc": "京都集散 · 深入洛北文人诗仙堂、大德寺孤篷庵枯山水、西阵百年手拉织机工坊、五条坂清水烧手作窑坊与桂离宫借景最高境界。",
    "color": "#264653",
    "daysText": "5 日 / 4 晚",
    "maxElev": "180 m (诗仙堂洛北山麓)",
    "trailKm": "22.0 km",
    "baseCostRMB": 6800,
    "pass": "京都市营地下铁·巴士一日券 + 关西私铁 IC 卡",
    "transit": "京都市营地下铁 + 阪急电车 + 京福岚电",
    "ports": "京都站综合枢纽集散",
    "bestMonths": [3, 4, 5, 9, 10, 11],
    "winterAdvice": {
        "title": "1–2月 枯山水雪景与汤豆腐暖心",
        "text": "大德寺与龙安寺枯山水石庭在轻雪覆盖下禅意更为深邃；冬日南禅寺顺正热汤豆腐清香温润；西阵町屋手织机穿梭之声清幽可闻。"
    },
    "autumnAdvice": {
        "title": "9–10月 初秋青苔与工艺手作巡访",
        "text": "9–10月避开深秋红叶百万大军拥堵；诗仙堂与大德寺庭园青苔依然鲜活翠绿，五条坂陶艺家作品展与西阵染织作坊体验清静自如。"
    },
    "nodes": v4_routes["r1"]["nodes"]
}

ROUTES["t2"] = {
    "id": "t2",
    "cat": "theme",
    "tag": "THEME 02 · SETO INLAND SEA ART ISLANDS & SHIKOKU",
    "title": "路线 2：濑户内艺术岛 + 四国海岛（5 日，当代艺术 + 岛民生活）",
    "shortName": "濑户内艺术三岛跳岛",
    "badge": "专题 02 · 濑户内当代艺术与海岛",
    "desc": "高松/宇野进出 · 直岛地中美术馆安藤忠雄清水混凝土、李禹焕美术馆、丰岛美术馆水滴凝结回响、小豆岛寒霞溪与高松手打赞岐乌冬面馆。",
    "color": "#BC4749",
    "daysText": "5 日 / 4 晚",
    "maxElev": "290 m (小豆岛寒霞溪)",
    "trailKm": "18.5 km",
    "baseCostRMB": 6500,
    "pass": "四国汽船渡轮票 + 小豆岛 Olive 巴士通票",
    "transit": "四国汽船高速船/客轮 + 租借 E-Bike 单车",
    "ports": "高松港 / 宇野港集散",
    "bestMonths": [3, 4, 5, 9, 10, 11],
    "winterAdvice": {
        "title": "1–2月 濑户内温和冬阳与静谧展馆",
        "text": "海岛冬季干燥温和，地中美术馆莫奈睡莲展厅完全无需排队，安藤忠雄的自然天井光线在冬日极尽深沉柔和。"
    },
    "autumnAdvice": {
        "title": "9–10月 艺术跳岛黄金天候与海风漫步",
        "text": "秋风习习，丰岛岛厨房品尝岛民新鲜海产蔬菜料理，小豆岛橄榄成熟泛绿，骑行在蔚蓝海岸线体感极佳。"
    },
    "nodes": v4_routes["r2"]["nodes"]
}

ROUTES["t3"] = {
    "id": "t3",
    "cat": "theme",
    "tag": "THEME 03 · TOKYO CRAFTS, GARDENS & MODERN ARCHITECTURE",
    "title": "路线 3：东京「下町工艺 + 庭园 + 近代建筑」（5 日，设计 + 江户庭园）",
    "shortName": "东京下町工艺与近代建筑",
    "badge": "专题 03 · 东京手作职人与大名庭园",
    "desc": "东京集散 · 深入合羽桥手工料理刀锻造铺、墨田区江户切子刻花玻璃工坊、旧芝离宫与滨离宫海水引流庭园、六义园和歌筑山与柯布西耶国立西洋美术馆。",
    "color": "#386641",
    "daysText": "5 日 / 4 晚",
    "maxElev": "40 m (六义园筑山藤代峠)",
    "trailKm": "26.0 km",
    "baseCostRMB": 6200,
    "pass": "Tokyo Subway Ticket 72小时券 (1,500 JPY)",
    "transit": "都营大江户线 + 东京 Metro + 都电荒川线",
    "ports": "东京都会区内循环",
    "bestMonths": [1, 2, 3, 4, 5, 9, 10, 11, 12],
    "winterAdvice": {
        "title": "1–2月 清冽冬空与下町老铺锅物",
        "text": "东京冬季晴空万里，远眺晴空塔极为锐利；合羽桥道具街与神保町古书店暖意融融；浅草驹形泥鳅锅与军鸡火锅暖胃。"
    },
    "autumnAdvice": {
        "title": "9–10月 秋高气爽与庭园夜间灯光秀",
        "text": "六义园秋季水景秀丽，藏前文创街区咖啡烘焙香气浓郁；上野国立西洋美术馆常设展与柯布西耶柱廊光影极具观赏性。"
    },
    "nodes": v4_routes["r3"]["nodes"]
}

ROUTES["t4"] = {
    "id": "t4",
    "cat": "theme",
    "tag": "THEME 04 · SEA OF JAPAN GASTRONOMY, CASTLES & CRAFTS",
    "title": "路线 4：日本海侧「美食与工艺」（北陆 + 冈山，6 日，和菓子 + 金属工艺 + 城郭）",
    "shortName": "北陆金泽·冈山美食工艺",
    "badge": "专题 04 · 日本海侧美食与城郭工艺",
    "desc": "冈山/金泽进出 · 黑色乌城冈山城与后乐园、备前烧千年柴烧窑、加贺百万石金泽兼六园、长町武家土墙街、能登半岛近江町海鲜丼与富山玻璃美术馆。",
    "color": "#D97706",
    "daysText": "6 日 / 5 晚",
    "maxElev": "60 m (金泽城本丸高台)",
    "trailKm": "24.0 km",
    "baseCostRMB": 7800,
    "pass": "JR 关西&北陆地区铁路周游券 (7日)",
    "transit": "山阳新干线 + 特急雷鸟号 + 北陆新干线",
    "ports": "冈山或金泽进出",
    "bestMonths": [3, 4, 5, 9, 10, 11],
    "winterAdvice": {
        "title": "1–2月 北陆加能蟹解禁与兼六园雪景",
        "text": "冬季为金泽近江町市场加能蟹（红楚蟹）与寒鰤鱼最鲜美时节；兼六园雪吊挂防雪绳索如琴弦交织，美不胜收。"
    },
    "autumnAdvice": {
        "title": "9–10月 备前陶艺烧造与金箔手工体验",
        "text": "10月中旬冈山备前烧祭热闹非凡，金泽东茶屋街手贴金箔体验趣味浓郁；富山湾白虾刺身清甜滑嫩。"
    },
    "nodes": v4_routes["r4"]["nodes"]
}

ROUTES["t5"] = {
    "id": "t5",
    "cat": "theme",
    "tag": "THEME 05 · KYUSHU VOLCANOES, ONSEN & HISTORIC PORTS",
    "title": "路线 5：九州「火山与历史」（5 日，温泉 + 原爆记忆 + 铁路文化）",
    "shortName": "九州火山地热观光铁道",
    "badge": "专题 05 · 九州活火山与特色观光铁道",
    "desc": "福冈博多进出 · 别府八大地狱蒸气喷涌、由布院金鳞湖晨雾与艺术小铺、阿苏世界级破火山口与草千里、加藤清正熊本城坚固石垣与长崎稻佐山千万夜景。",
    "color": "#BC4749",
    "daysText": "5 日 / 4 晚",
    "maxElev": "1,140 m (阿苏中岳草千里高台)",
    "trailKm": "21.0 km",
    "baseCostRMB": 6900,
    "pass": "JR 全/北九州铁路周游券 (5日券 14,000 JPY)",
    "transit": "特急 Sonic + 九州新干线 + 特急由布院之森",
    "ports": "福冈博多国际空港枢纽",
    "bestMonths": [3, 4, 5, 10, 11, 12],
    "winterAdvice": {
        "title": "1–2月 地热温泉蒸腾与由布院晨雾",
        "text": "冬日别府地狱蒸气喷涌壮观非凡，由布院露天温泉水气蒸腾宛如仙境；阿苏火山草千里或有薄雪覆草，风光别致。"
    },
    "autumnAdvice": {
        "title": "9–10月 秋高气爽草千里与长崎海风",
        "text": "阿苏破火山口秋草金黄，乘观光列车穿行火山口体感极佳；长崎稻佐山秋日能见度极高，立体山谷夜景光彩耀眼。"
    },
    "nodes": v4_routes["r5"]["nodes"]
}

ROUTES["t6"] = {
    "id": "t6",
    "cat": "theme",
    "tag": "THEME 06 · HOKKAIDO WINTER RAILWAYS & WILDERNESS",
    "title": "路线 6：北海道「铁道与雪季」（7 日，雪祭 + 温泉 + 全道铁道）",
    "shortName": "北海道道东铁道雪季",
    "badge": "专题 06 · 北海道极寒流冰与丹顶鹤",
    "desc": "札幌/钏路进出 · 札幌大通公园雪祭冰雕、特急大空号穿越日高山脉、SL冬之湿原号蒸气机车、鹤居村雪原丹顶鹤起舞、神秘不冻摩周湖与网走破冰船冲破流冰。",
    "color": "#1E3A8A",
    "daysText": "7 日 / 6 晚",
    "maxElev": "351 m (摩周湖第一展望台)",
    "trailKm": "15.0 km",
    "baseCostRMB": 9800,
    "pass": "JR 北海道铁路周游券 (5日或7日)",
    "transit": "特急 Ozora + SL冬之湿原号 + 网走极光号破冰船",
    "ports": "札幌新千岁或钏路国际机场",
    "bestMonths": [1, 2, 6, 7, 8],
    "winterAdvice": {
        "title": "1–2月 极寒流冰高峰与野生丹顶鹤漫步",
        "text": "全日本冬季极景巅峰。网走鄂霍次克海流冰覆盖率最高；鹤居村野外丹顶鹤雪中交颈起舞；必须配备专业雪地防滑靴与防风雪羽绒服。"
    },
    "autumnAdvice": {
        "title": "9–10月 道东原始湿原金黄与秋鲑回流",
        "text": "钏路湿原在初秋泛起苍茫金黄，阿寒湖畔冷杉落叶松红黄相间；屈斜路湖与摩周湖湛蓝深邃，秋鲑与海胆正值产季。"
    },
    "nodes": v4_routes["r6"]["nodes"]
}

# 4. Literature (3 Long Routes from v2.html + 3 Micro-Tours from v4.html)
ROUTES["ml1"] = {
    "id": "ml1",
    "cat": "literature",
    "tag": "LITERATURE 04 · HARUKI MURAKAMI · HOKKAIDO WILDERNESS & SHEEP",
    "title": v2_routes["r4"]["title"],
    "shortName": v2_extras["r4"].get("shortName", "村上春树·北海道寻羊冒险"),
    "badge": v2_extras["r4"].get("badge", "村上文学 · 18日北国荒原"),
    "desc": v2_routes["r4"]["desc"],
    "color": v2_routes["r4"].get("color", "#3D5A80"),
    "daysText": "18 日 / 17 晚",
    "maxElev": "680 m (美深町仁宇布高地)",
    "trailKm": "95.0 km (全线高地农场与极北海岸)",
    "baseCostRMB": 17800,
    "pass": v2_extras["r4"]["pass"],
    "transit": v2_extras["r4"]["transit"],
    "ports": v2_extras["r4"]["ports"],
    "bestMonths": [1, 2, 7, 8, 9, 10],
    "winterAdvice": v2_extras["r4"]["winterAdvice"],
    "autumnAdvice": v2_extras["r4"]["autumnAdvice"],
    "nodes": v2_routes["r4"]["nodes"]
}

ROUTES["ml2"] = {
    "id": "ml2",
    "cat": "literature",
    "tag": "LITERATURE 05 · HARUKI MURAKAMI · SHIKOKU KAFKA & HANSHIN",
    "title": v2_routes["r5"]["title"],
    "shortName": v2_extras["r5"].get("shortName", "村上春树·四国海边卡夫卡"),
    "badge": v2_extras["r5"].get("badge", "村上文学 · 16日少年海滩"),
    "desc": v2_routes["r5"]["desc"],
    "color": v2_routes["r5"].get("color", "#1B4332"),
    "daysText": "16 日 / 15 晚",
    "maxElev": "720 m (梼原町森林迷宫与云之上)",
    "trailKm": "68.0 km (全线海岸林道与避难所探寻)",
    "baseCostRMB": 15200,
    "pass": v2_extras["r5"]["pass"],
    "transit": v2_extras["r5"]["transit"],
    "ports": v2_extras["r5"]["ports"],
    "bestMonths": [3, 4, 5, 9, 10, 11],
    "winterAdvice": v2_extras["r5"]["winterAdvice"],
    "autumnAdvice": v2_extras["r5"]["autumnAdvice"],
    "nodes": v2_routes["r5"]["nodes"]
}

ROUTES["ml3"] = {
    "id": "ml3",
    "cat": "literature",
    "tag": "LITERATURE 06 · HARUKI MURAKAMI · TOKYO, HAKONE & IZU",
    "title": v2_routes["r6"]["title"],
    "shortName": v2_extras["r6"].get("shortName", "村上春树·东京1Q84箱根"),
    "badge": v2_extras["r6"].get("badge", "村上文学 · 15日山海慢行"),
    "desc": v2_routes["r6"]["desc"],
    "color": v2_routes["r6"].get("color", "#6D4C41"),
    "daysText": "15 日 / 14 晚",
    "maxElev": "865 m (箱根仙石原·桃源台画室山谷)",
    "trailKm": "58.0 km (都会漫步与伊豆苔藓古道)",
    "baseCostRMB": 14600,
    "pass": v2_extras["r6"]["pass"],
    "transit": v2_extras["r6"]["transit"],
    "ports": v2_extras["r6"]["ports"],
    "bestMonths": [1, 2, 3, 4, 5, 9, 10, 11, 12],
    "winterAdvice": v2_extras["r6"]["winterAdvice"],
    "autumnAdvice": v2_extras["r6"]["autumnAdvice"],
    "nodes": v2_routes["r6"]["nodes"]
}

ROUTES["m1"] = {
    "id": "m1",
    "cat": "literature",
    "tag": "LITERATURE 01 · HARUKI MURAKAMI · TOKYO JAZZ & YOUTH",
    "title": "路线 M1：东京村上春树 2–3 日（文学东京·1960年代爵士吧与早稻田）",
    "shortName": "村上春树·东京爵士黑胶",
    "badge": "文学 01 · 青春与爵士黑胶",
    "desc": "早稻田大学国际文学馆（村上春树图书馆）、千驮谷神宫球场外野席（下定决心写小说之地）、国分寺 Peter Cat 爵士酒吧旧址与南青山纪伊国屋书店。",
    "color": "#264653",
    "daysText": "3 日 / 2 晚",
    "maxElev": "35 m (早稻田文学馆台地)",
    "trailKm": "14.5 km",
    "baseCostRMB": 3800,
    "pass": "东京 Metro 24小时券 + Suica IC卡",
    "transit": "东京地下铁 + JR中央·总武线",
    "ports": "东京都心",
    "bestMonths": [1, 2, 3, 4, 5, 9, 10, 11, 12],
    "winterAdvice": {
        "title": "冬日早稻田落木与爵士喫茶香气",
        "text": "冬日东京空气清冽，漫步早稻田大学和敬塾宿舍小径；在新宿 Disk Union 翻找爵士二手黑胶，点一杯热咖啡享受慢调文学时光。"
    },
    "autumnAdvice": {
        "title": "早秋神宫外苑慢跑与神保町古书祭",
        "text": "循着《当我谈跑步时我谈些什么》在外苑银杏大道慢跑；10月下旬神保町古书街露天书市淘选绝版文库本。"
    },
    "nodes": v4_routes["m1"]["nodes"]
}

ROUTES["m2"] = {
    "id": "m2",
    "cat": "literature",
    "tag": "LITERATURE 02 · 1Q84 TWIN MOONS · TOKYO WEST & SANGENJAYA",
    "title": "路线 M2：村上春树 2 日（从《1Q84》首都高避难梯到高圆寺双月滑梯）",
    "shortName": "村上春树·1Q84双月东京",
    "badge": "文学 02 · 现实与非现实交界",
    "desc": "三轩茶屋首都高速 3 号线紧急避难阶梯（青豆脱鞋走入 1Q84 世界之地）、世田谷太子堂老街居酒屋、高圆寺中央公园滑梯（天吾仰望双月之地）与下北泽古着唱片街。",
    "color": "#4A5568",
    "daysText": "2 日 / 1 晚",
    "maxElev": "42 m (世田谷高台)",
    "trailKm": "11.0 km",
    "baseCostRMB": 2600,
    "pass": "东急电铁一日通票 + JR东日本 IC卡",
    "transit": "东急田园都市线 + 世田谷线路面电车",
    "ports": "东京西部",
    "bestMonths": [1, 2, 3, 4, 5, 9, 10, 11, 12],
    "winterAdvice": {
        "title": "冬夜双月寒空与世田谷怀旧胡同",
        "text": "冬夜三轩茶屋三角地带暖意融融，高圆寺中央公园夜空中星月分明；在静谧居民区感受都会隐匿者的独特心境。"
    },
    "autumnAdvice": {
        "title": "秋日午后漫步下北泽与高圆寺",
        "text": "秋风拂过世田谷老式路面电车，下北泽独立小剧场与二手书店林立，体验最地道的东京西郊文艺青年日常。"
    },
    "nodes": v4_routes["m2"]["nodes"]
}

ROUTES["m3"] = {
    "id": "m3",
    "cat": "literature",
    "tag": "LITERATURE 03 · KAFKA ON THE SHORE · SHIKOKU ODYSSEY",
    "title": "路线 M3：四国村上春树 4 日（《海边的卡夫卡》高知流浪与赞岐乌冬巡礼）",
    "shortName": "村上春树·海边的卡夫卡",
    "badge": "文学 03 · 隐喻迷宫与少年海滩",
    "desc": "冈山跨濑户大桥至四国高松港、丸龟市猪熊弦一郎现代美术馆（甲村纪念图书馆原型）、琴平手打赞岐乌冬名铺、大步危深山林道避难所与高知太平洋海岸桂滨。",
    "color": "#1B4332",
    "daysText": "4 日 / 3 晚",
    "maxElev": "380 m (四国深山吉野川峡谷)",
    "trailKm": "16.0 km",
    "baseCostRMB": 4900,
    "pass": "四国铁路周游券 (3日券) + 琴平电铁",
    "transit": "快速 Marine Liner + 特急南风号 + 土佐电",
    "ports": "高松进 → 高知出",
    "bestMonths": [3, 4, 5, 9, 10, 11],
    "winterAdvice": {
        "title": "冬日太平洋暖阳与赞岐热乌冬",
        "text": "四国南岸太平洋温暖无雪，高松热腾腾的釜玉乌冬面麦香扑鼻；在丸龟安静的图书馆阅读佐伯女士的乐谱。"
    },
    "autumnAdvice": {
        "title": "秋高气爽与大步危深山峡谷红叶",
        "text": "吉野川大步危峡谷在秋日染上五彩斑斓，高知桂滨波涛浩荡；品尝当季肥美的稻草炙烤鲣鱼。"
    },
    "nodes": v4_routes["m3"]["nodes"]
}

# Convert ROUTES to JSON string
ROUTES_JSON = json.dumps(ROUTES, ensure_ascii=False)

# Build Transit Table Rows HTML
transit_tr_html = []
for r in transit_rows:
    seq = r[0].replace('*', '')
    corridor = r[1]
    stations = r[2]
    train = r[3]
    duration = r[4]
    fare = r[5]
    booking = r[6]
    tips = r[7]
    transit_tr_html.append(f"""
      <tr>
        <td class="mono" style="font-weight:700;color:var(--slate-500);text-align:center;">{seq}</td>
        <td style="font-weight:700;color:var(--navy-900);">{corridor}</td>
        <td style="font-size:0.72rem;">{stations}</td>
        <td style="color:var(--indigo);font-weight:600;">{train}</td>
        <td class="mono">{duration}</td>
        <td class="mono" style="color:var(--vermilion);font-weight:600;">{fare}</td>
        <td style="font-size:0.7rem;">{booking}</td>
        <td style="font-size:0.7rem;color:var(--slate-500);">{tips}</td>
      </tr>
    """)
TRANSIT_TABLE_ROWS = "".join(transit_tr_html)

# Build Drawer Cards HTML
drawer_cards_html = []
for r_key, r_obj in ROUTES.items():
    cat = r_obj["cat"]
    title = r_obj["title"]
    short_name = r_obj.get("shortName", title)
    days_text = r_obj.get("daysText", "")
    km = r_obj.get("trailKm", "")
    desc = r_obj.get("desc", "")
    color = r_obj.get("color", "#264653")
    cat_name = {
        "framework": "落地主干",
        "classic": "经典大长线",
        "theme": "专题深度",
        "literature": "村上文学"
    }.get(cat, "路线")

    drawer_cards_html.append(f"""
      <div class="drawer-card" data-cat="{cat}" data-key="{r_key}" onclick="selectRouteFromDrawer('{r_key}')">
        <div class="d-card-top">
          <span class="d-card-cat" style="color:{color};">
            <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:{color};margin-right:4px;"></span>
            {cat_name}
          </span>
          <span class="d-card-days">{days_text}</span>
        </div>
        <div class="d-card-title">{short_name}</div>
        <div class="d-card-desc">{desc}</div>
      </div>
    """)
DRAWER_CARDS = "".join(drawer_cards_html)

# Write output file
print("Writing", OUTPUT_FILE)

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>日本深度自游全景导览 · 2026 典藏主控版</title>
  <meta name="description" content="基于日本外务省、JNTO、JR官方数据编制的15–20日深度自由行空间导览系统。整合东海道黄金三角走廊、信越北陆古道、出云神话、东北秘汤与村上春树文学寻踪。">

  <!-- External Libraries -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
  <script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>

  <style>
    :root {{
      --washi: #f8fafc;
      --washi-card: #ffffff;
      --washi-subtle: #f1f5f9;
      --navy-900: #0b1329;
      --navy-800: #13203f;
      --navy-700: #1e3158;
      --navy-100: #e2e8f0;
      --slate-800: #1e293b;
      --slate-700: #334155;
      --slate-600: #475569;
      --slate-500: #64748b;
      --slate-400: #94a3b8;
      --slate-300: #cbd5e1;
      --slate-200: #e2e8f0;
      --slate-100: #f1f5f9;
      --vermilion: #dc2626;
      --vermilion-soft: #fef2f2;
      --vermilion-border: #fecaca;
      --pine: #0d9488;
      --pine-soft: #f0fdfa;
      --pine-border: #99f6e4;
      --indigo: #2563eb;
      --indigo-soft: #eff6ff;
      --indigo-border: #bfdbfe;
      --amber: #d97706;
      --amber-soft: #fffbeb;
      --amber-border: #fde68a;
      --active-color: #264653;
      --font-serif: "Noto Serif SC", "Source Han Serif SC", STSong, "Yu Mincho", serif;
      --font-sans: "Noto Sans SC", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      --font-mono: "JetBrains Mono", "SFMono-Regular", Consolas, Menlo, monospace;
      --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
      --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.08), 0 2px 4px -2px rgb(0 0 0 / 0.05);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.08);
    }}

    body.theme-night {{
      --washi: #0b1329;
      --washi-card: #13203f;
      --washi-subtle: #1e293b;
      --navy-900: #f8fafc;
      --navy-800: #e2e8f0;
      --navy-700: #cbd5e1;
      --navy-100: #1e3158;
      --slate-800: #f8fafc;
      --slate-700: #e2e8f0;
      --slate-600: #cbd5e1;
      --slate-500: #94a3b8;
      --slate-400: #64748b;
      --slate-300: #334155;
      --slate-200: rgba(255, 255, 255, 0.12);
      --slate-100: #1e293b;
      --vermilion-soft: #2a1215;
      --vermilion-border: #5c1d24;
      --pine-soft: #092623;
      --pine-border: #134e48;
      --indigo-soft: #112240;
      --indigo-border: #1d4ed8;
      --amber-soft: #2d1f05;
      --amber-border: #78350f;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ height: 100%; width: 100%; overflow: hidden; background: var(--washi); color: var(--slate-800); font-family: var(--font-sans); -webkit-font-smoothing: antialiased; }}

    .icon {{ width: 14px; height: 14px; stroke-width: 2; stroke: currentColor; fill: none; stroke-linecap: round; stroke-linejoin: round; vertical-align: middle; display: inline-block; }}
    .icon-lg {{ width: 18px; height: 18px; }}
    .mono {{ font-family: var(--font-mono); font-feature-settings: "tnum"; }}

    /* 1. GLOBAL HEADER (50px Fixed) */
    .global-header {{
      position: fixed; top: 0; left: 0; right: 0; height: 50px; z-index: 1000;
      background: var(--washi-card); border-bottom: 1px solid var(--slate-200);
      display: flex; align-items: center; justify-content: space-between; padding: 0 1rem;
      box-shadow: var(--shadow-sm); user-select: none;
    }}
    .brand-group {{ display: flex; align-items: center; gap: 8px; flex-shrink: 0; }}
    .brand-seal {{
      width: 24px; height: 24px; background: var(--vermilion); color: #fff;
      display: flex; align-items: center; justify-content: center;
      font-family: var(--font-serif); font-size: 13px; font-weight: 700; border-radius: 4px;
    }}
    .brand-text-block {{ display: flex; align-items: baseline; gap: 6px; }}
    .brand-title {{ font-family: var(--font-serif); font-size: 0.95rem; font-weight: 700; color: var(--navy-900); letter-spacing: 0.02em; }}
    .brand-badge {{
      font-size: 0.65rem; font-family: var(--font-mono); font-weight: 700;
      background: var(--pine-soft); color: var(--pine); border: 1px solid var(--pine-border);
      padding: 1px 5px; border-radius: 9999px; text-transform: uppercase;
    }}

    .header-center {{ display: flex; align-items: center; gap: 10px; }}

    .route-drawer-btn {{
      display: flex; align-items: center; gap: 7px;
      background: var(--washi-subtle); border: 1px solid var(--slate-300); border-radius: 6px;
      padding: 5px 11px; cursor: pointer; transition: all 0.15s ease;
      color: var(--slate-800); font-size: 0.8rem; font-weight: 600; font-family: var(--font-sans);
    }}
    .route-drawer-btn:hover {{ border-color: var(--active-color); background: var(--washi-card); }}
    .route-drawer-dot {{ width: 8px; height: 8px; border-radius: 50%; display: inline-block; flex-shrink: 0; }}
    .icon-chevron {{ width: 12px; height: 12px; color: var(--slate-400); transition: transform 0.2s ease; }}
    .route-drawer-btn.open .icon-chevron {{ transform: rotate(180deg); }}

    .mode-switch-capsule {{
      display: flex; background: var(--washi-subtle); border: 1px solid var(--slate-300);
      border-radius: 6px; padding: 2px;
    }}
    .mode-btn {{
      display: flex; align-items: center; gap: 5px; border: none; background: transparent;
      padding: 3px 8px; font-size: 0.72rem; font-weight: 500; color: var(--slate-600);
      border-radius: 4px; cursor: pointer; transition: all 0.15s ease; font-family: var(--font-sans);
    }}
    .mode-btn.active {{
      background: var(--washi-card); color: var(--navy-900); font-weight: 700;
      box-shadow: 0 1px 2px rgba(0,0,0,0.06);
    }}

    .header-right {{ display: flex; align-items: center; gap: 8px; }}
    .util-group, .engine-group {{ display: flex; align-items: center; gap: 4px; }}
    .divider-vertical {{ width: 1px; height: 18px; background: var(--slate-200); margin: 0 4px; }}

    .btn-util {{
      display: flex; align-items: center; gap: 4px; background: transparent;
      border: 1px solid transparent; border-radius: 5px; padding: 4px 7px;
      font-size: 0.74rem; font-weight: 500; color: var(--slate-600); cursor: pointer; transition: all 0.15s;
    }}
    .btn-util:hover {{ background: var(--washi-subtle); border-color: var(--slate-300); color: var(--navy-900); }}

    .btn-icon {{
      display: flex; align-items: center; justify-content: center; width: 28px; height: 28px;
      background: transparent; border: 1px solid transparent; border-radius: 5px;
      color: var(--slate-600); cursor: pointer; transition: all 0.15s;
    }}
    .btn-icon:hover {{ background: var(--washi-subtle); border-color: var(--slate-300); color: var(--navy-900); }}

    .tile-dropdown {{
      background: var(--washi-subtle); border: 1px solid var(--slate-300); border-radius: 5px;
      padding: 3px 6px; font-size: 0.72rem; color: var(--slate-700); cursor: pointer; outline: none;
      font-family: var(--font-sans);
    }}
    .btn-version-pill {{
      background: var(--indigo-soft); border: 1px solid var(--indigo-border); color: var(--indigo);
      font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; cursor: pointer;
    }}

    /* 2. TOP ROUTE DRAWER */
    .route-drawer-backdrop {{
      position: fixed; top: 50px; left: 0; right: 0; bottom: 0; z-index: 998;
      background: rgba(11, 19, 41, 0.45); backdrop-filter: blur(2px);
      display: none; opacity: 0; transition: opacity 0.2s ease;
    }}
    .route-drawer-backdrop.show {{ display: block; opacity: 1; }}

    .route-drawer {{
      position: fixed; top: 50px; left: 0; right: 0; z-index: 999;
      background: var(--washi-card); border-bottom: 2px solid var(--slate-300);
      box-shadow: 0 12px 28px rgba(0,0,0,0.15); max-height: calc(85vh - 50px);
      overflow-y: auto; transform: translateY(-105%); transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      padding: 1.25rem 2rem;
    }}
    .route-drawer.open {{ transform: translateY(0); }}

    .route-drawer-header {{
      display: flex; align-items: center; justify-content: space-between;
      border-bottom: 1px solid var(--slate-200); padding-bottom: 0.75rem; margin-bottom: 1rem;
    }}
    .drawer-cat-tabs {{ display: flex; gap: 6px; flex-wrap: wrap; }}
    .drawer-tab {{
      background: var(--washi-subtle); border: 1px solid var(--slate-300); border-radius: 5px;
      padding: 4px 10px; font-size: 0.76rem; font-weight: 600; color: var(--slate-600);
      cursor: pointer; transition: all 0.15s ease;
    }}
    .drawer-tab.active {{ background: var(--active-color); border-color: var(--active-color); color: #fff; }}
    .drawer-close-btn {{
      background: transparent; border: none; cursor: pointer; color: var(--slate-400); padding: 4px;
      border-radius: 4px; display: flex; align-items: center;
    }}
    .drawer-close-btn:hover {{ color: var(--slate-700); background: var(--washi-subtle); }}

    .route-drawer-grid {{
      display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 10px;
    }}
    .drawer-card {{
      background: var(--washi); border: 1px solid var(--slate-200); border-radius: 7px;
      padding: 10px 12px; cursor: pointer; transition: all 0.15s ease; position: relative;
    }}
    .drawer-card:hover {{
      border-color: var(--active-color); background: var(--washi-card);
      transform: translateY(-2px); box-shadow: var(--shadow-sm);
    }}
    .drawer-card.active {{
      border-color: var(--active-color); background: var(--washi-card);
      border-left: 4px solid var(--active-color);
    }}
    .d-card-top {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px; }}
    .d-card-cat {{ font-size: 0.65rem; font-weight: 700; color: var(--slate-500); text-transform: uppercase; font-family: var(--font-mono); }}
    .d-card-days {{ font-size: 0.72rem; font-family: var(--font-mono); font-weight: 600; color: var(--slate-600); }}
    .d-card-title {{ font-family: var(--font-serif); font-size: 0.85rem; font-weight: 700; color: var(--navy-900); margin-bottom: 4px; line-height: 1.35; }}
    .d-card-desc {{ font-size: 0.72rem; color: var(--slate-500); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}

    /* 3. MAIN APP SHELL (43% : 57%) */
    .app-shell {{
      position: absolute; top: 50px; left: 0; right: 0; bottom: 0;
      display: grid; grid-template-columns: 43% 57%; overflow: hidden;
    }}

    /* Left Narrative Column */
    .narrative-col {{
      height: 100%; overflow-y: auto; padding: 1.25rem 1.5rem;
      border-right: 1px solid var(--slate-200); background: var(--washi);
    }}

    /* Route Hero */
    .route-hero {{
      background: var(--washi-card); border: 1px solid var(--slate-200);
      border-radius: 8px; padding: 1.15rem 1.25rem; margin-bottom: 1rem;
      box-shadow: var(--shadow-sm);
    }}
    .hero-top-row {{ display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }}
    .route-cat-badge {{
      font-size: 0.68rem; font-weight: 700; font-family: var(--font-mono);
      background: var(--indigo-soft); color: var(--indigo); border: 1px solid var(--indigo-border);
      padding: 1px 7px; border-radius: 9999px;
    }}
    .route-tag {{ font-size: 0.68rem; font-weight: 600; font-family: var(--font-mono); color: var(--slate-400); letter-spacing: 0.05em; }}
    .route-name {{ font-family: var(--font-serif); font-size: 1.15rem; font-weight: 700; color: var(--navy-900); line-height: 1.4; margin-bottom: 8px; }}
    .route-desc {{ font-size: 0.8rem; color: var(--slate-600); line-height: 1.55; }}

    /* Route Meta Grid (Replacing kpi-grid) */
    .route-meta-grid {{
      display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; margin-bottom: 1rem;
    }}
    .meta-item {{
      background: var(--washi-card); border: 1px solid var(--slate-200);
      border-radius: 7px; padding: 8px 10px; display: flex; flex-direction: column; gap: 3px;
      box-shadow: var(--shadow-sm); min-width: 0; overflow: hidden;
    }}
    .meta-label {{
      font-size: 0.7rem; color: var(--slate-500); display: flex; align-items: center; gap: 5px; font-weight: 600;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0;
    }}
    .meta-val {{
      font-size: 0.78rem; font-weight: 700; color: var(--navy-900); font-family: var(--font-sans);
      line-height: 1.35; word-break: break-word; overflow-wrap: break-word; min-width: 0;
    }}

    /* Phenology Box & Seasonal Advice Box */
    .phenology-box {{
      background: var(--washi-card); border: 1px solid var(--slate-200);
      border-radius: 7px; padding: 8px 12px; margin-bottom: 10px; box-shadow: var(--shadow-sm);
    }}
    .phenology-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }}
    .phenology-label {{ font-size: 0.72rem; font-weight: 600; color: var(--slate-600); display: flex; align-items: center; gap: 5px; }}
    .phenology-tip {{ font-size: 0.65rem; color: var(--slate-400); }}
    .month-pills {{ display: grid; grid-template-columns: repeat(12, 1fr); gap: 3px; }}
    .month-pill {{
      font-size: 0.65rem; font-family: var(--font-mono); font-weight: 600; text-align: center;
      padding: 3px 0; border-radius: 4px; background: var(--washi-subtle); color: var(--slate-400);
      transition: all 0.15s ease;
    }}
    .month-pill.active {{
      background: var(--active-color); color: #fff; font-weight: 700;
      box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }}

    .seasonal-box {{
      display: flex; gap: 10px; background: var(--pine-soft); border: 1px solid var(--pine-border);
      border-radius: 7px; padding: 10px 12px; margin-bottom: 1rem; align-items: flex-start;
    }}
    .seasonal-box svg {{ color: var(--pine); flex-shrink: 0; margin-top: 2px; }}
    .seasonal-box h4 {{ font-size: 0.8rem; font-weight: 700; color: var(--navy-900); margin-bottom: 3px; font-family: var(--font-serif); }}
    .seasonal-box p {{ font-size: 0.74rem; color: var(--slate-600); line-height: 1.45; }}

    /* Sub-Navigation Tabs */
    .panel-switcher {{
      display: flex; background: var(--washi-card); border: 1px solid var(--slate-200);
      border-radius: 7px; padding: 3px; margin-bottom: 1rem; box-shadow: var(--shadow-sm);
    }}
    .panel-tab {{
      flex: 1; border: none; background: transparent; padding: 6px 4px;
      font-size: 0.74rem; font-weight: 600; color: var(--slate-500); cursor: pointer;
      border-radius: 5px; transition: all 0.15s ease; text-align: center;
    }}
    .panel-tab.active {{ background: var(--washi-subtle); color: var(--navy-900); font-weight: 700; }}

    /* Day Itinerary Cards */
    .day-list {{ display: flex; flex-direction: column; gap: 12px; }}
    .day-card {{
      background: var(--washi-card); border: 1px solid var(--slate-200);
      border-radius: 8px; padding: 12px 14px; box-shadow: var(--shadow-sm);
      transition: all 0.2s ease; cursor: pointer; position: relative;
    }}
    .day-card:hover {{
      border-color: var(--active-color); box-shadow: var(--shadow-md); transform: translateY(-1px);
    }}
    .day-card.active {{
      border-left: 5px solid var(--active-color) !important;
      background: #fcfdfe;
      box-shadow: var(--shadow-md);
    }}
    .day-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }}
    .day-badge {{
      font-size: 0.72rem; font-family: var(--font-mono); font-weight: 700;
      background: var(--active-color); color: #fff; padding: 2px 7px; border-radius: 4px;
    }}
    .day-coords {{ font-size: 0.68rem; font-family: var(--font-mono); color: var(--slate-400); }}
    .day-name {{ font-family: var(--font-serif); font-size: 0.95rem; font-weight: 700; color: var(--navy-900); margin-bottom: 6px; }}
    .day-exp {{ font-size: 0.78rem; color: var(--slate-600); line-height: 1.5; margin-bottom: 10px; }}

    .transit-block {{
      background: var(--washi-subtle); border-radius: 6px; padding: 8px 10px; margin-bottom: 8px;
      border-left: 3px solid var(--indigo); font-size: 0.74rem;
    }}
    .transit-row {{ display: flex; justify-content: space-between; margin-bottom: 3px; font-weight: 600; color: var(--navy-900); }}
    .transit-alert {{ font-size: 0.7rem; color: var(--slate-500); line-height: 1.35; }}

    .food-stay-block {{
      display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.72rem;
      border-top: 1px solid var(--slate-100); padding-top: 8px; margin-top: 8px;
    }}
    .fs-item {{ display: flex; flex-direction: column; gap: 2px; }}
    .fs-label {{ font-weight: 700; color: var(--slate-400); font-size: 0.65rem; text-transform: uppercase; }}
    .fs-val {{ color: var(--slate-700); font-weight: 500; }}
    .tabelog-tag {{ color: var(--amber); font-weight: 700; font-family: var(--font-mono); }}

    /* Panel 2: Transit Table */
    .transit-table-wrapper {{
      background: var(--washi-card); border: 1px solid var(--slate-200);
      border-radius: 8px; padding: 12px; overflow-x: auto; font-size: 0.74rem; box-shadow: var(--shadow-sm);
    }}
    .transit-data-table {{ width: 100%; border-collapse: collapse; text-align: left; min-width: 600px; }}
    .transit-data-table th, .transit-data-table td {{ padding: 6px 8px; border-bottom: 1px solid var(--slate-200); }}
    .transit-data-table th {{ background: var(--washi-subtle); color: var(--slate-700); font-weight: 700; }}

    /* Panel 3: Stay & Airbnb */
    .stay-cards-grid {{ display: flex; flex-direction: column; gap: 10px; }}
    .stay-card {{
      background: var(--washi-card); border: 1px solid var(--slate-200);
      border-radius: 8px; padding: 12px 14px; box-shadow: var(--shadow-sm);
    }}
    .stay-card h4 {{ font-family: var(--font-serif); font-size: 0.88rem; font-weight: 700; color: var(--navy-900); margin-bottom: 4px; }}
    .stay-card p {{ font-size: 0.76rem; color: var(--slate-600); line-height: 1.45; }}

    /* Panel 4: Budget Sandbox */
    .sandbox-container {{
      background: var(--washi-card); border: 1px solid var(--slate-200);
      border-radius: 8px; padding: 14px; box-shadow: var(--shadow-sm);
    }}
    .slider-row {{ margin-bottom: 12px; }}
    .slider-header {{ display: flex; justify-content: space-between; font-size: 0.76rem; font-weight: 600; margin-bottom: 4px; color: var(--navy-900); }}
    .slider-input {{ width: 100%; height: 5px; accent-color: var(--active-color); cursor: pointer; }}
    .budget-result-display {{
      background: var(--washi-subtle); border-radius: 6px; padding: 10px 12px;
      display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px;
    }}
    .budget-val-big {{ font-size: 1.4rem; font-weight: 700; color: var(--vermilion); font-family: var(--font-mono); }}

    /* Right Viewport Column (Map & D3 Elevation) */
    .viewport-col {{
      height: 100%; display: flex; flex-direction: column; background: var(--washi-subtle);
    }}
    .map-wrapper {{ flex: 1; position: relative; width: 100%; }}
    #map-canvas {{ width: 100%; height: 100%; background: #dcd7c9; }}

    .map-overlay-top {{
      position: absolute; top: 10px; right: 10px; z-index: 500;
      display: flex; gap: 6px;
    }}
    .map-chip {{
      background: var(--washi-card); border: 1px solid var(--slate-300);
      border-radius: 6px; padding: 4px 8px; font-size: 0.72rem; box-shadow: var(--shadow-md);
      display: flex; align-items: center; gap: 5px;
    }}
    .tile-select {{ border: none; background: transparent; font-size: 0.72rem; outline: none; cursor: pointer; color: var(--slate-700); }}
    .btn-util-sm {{ background: transparent; border: none; font-size: 0.72rem; cursor: pointer; display: flex; align-items: center; gap: 4px; color: var(--slate-700); font-weight: 600; }}

    /* Elevation Dock */
    .elevation-dock {{
      height: 155px; max-height: 155px; min-height: 155px; background: var(--washi-card); border-top: 1px solid var(--slate-200);
      display: flex; flex-direction: column; padding: 8px 14px 4px; z-index: 400; box-shadow: 0 -2px 6px rgba(0,0,0,0.03);
      box-sizing: border-box; overflow: hidden; flex-shrink: 0;
    }}
    .dock-header {{
      height: 22px; min-height: 22px; max-height: 22px; line-height: 22px;
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;
      overflow: hidden; white-space: nowrap; flex-shrink: 0; box-sizing: border-box;
    }}
    .dock-title {{
      font-size: 0.72rem; font-weight: 700; color: var(--navy-900); display: flex; align-items: center; gap: 5px;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 0 1 auto; min-width: 0;
    }}
    .probe-readout {{
      font-size: 0.72rem; font-family: var(--font-mono); color: var(--active-color); font-weight: 700;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 0 0 auto; max-width: 50%;
      text-align: right; margin-left: 8px; min-width: 0;
    }}
    #elevation-svg {{ width: 100%; height: 119px; max-height: 119px; overflow: visible; display: block; flex: 1 1 auto; }}
    .visa-table {{ width: 100%; border-collapse: collapse; font-size: 0.76rem; margin-top: 8px; }}
    .visa-table th {{ background: var(--washi-subtle); border: 1px solid var(--slate-300); padding: 8px 10px; font-weight: 700; text-align: left; }}
    .visa-table td {{ border: 1px solid var(--slate-300); padding: 8px 10px; line-height: 1.45; }}

    /* Modals System */
    .modal-backdrop {{
      position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 2000;
      background: rgba(11, 19, 41, 0.6); backdrop-filter: blur(3px);
      display: none; align-items: center; justify-content: center; padding: 1.5rem;
    }}
    .modal-backdrop.show {{ display: flex; }}
    .modal-card {{
      background: var(--washi-card); border: 1px solid var(--slate-300);
      border-radius: 10px; width: 100%; max-width: 760px; max-height: 85vh;
      display: flex; flex-direction: column; box-shadow: var(--shadow-lg); overflow: hidden;
    }}
    .modal-header {{
      padding: 12px 16px; border-bottom: 1px solid var(--slate-200);
      display: flex; justify-content: space-between; align-items: center;
    }}
    .modal-title {{ font-family: var(--font-serif); font-size: 0.98rem; font-weight: 700; color: var(--navy-900); }}
    .modal-close {{ background: transparent; border: none; cursor: pointer; color: var(--slate-400); font-size: 1.2rem; }}
    .modal-body {{ padding: 14px 18px; overflow-y: auto; font-size: 0.8rem; line-height: 1.55; color: var(--slate-700); }}
    .modal-footer {{ padding: 10px 16px; border-top: 1px solid var(--slate-200); display: flex; justify-content: flex-end; }}

    @media (max-width: 900px) {{
      .app-shell {{ grid-template-columns: 1fr; grid-template-rows: 45vh 1fr; }}
      .viewport-col {{ order: 1; }}
      .narrative-col {{ order: 2; height: 100%; }}
      .header-right .btn-util span {{ display: none; }}
    }}
  </style>
</head>
<body>

  <!-- 1. GLOBAL HEADER -->
  <header class="global-header">
    <div class="brand-group">
      <div class="brand-seal">日</div>
      <div class="brand-text-block">
        <h1 class="brand-title">日本深度自游全景导览</h1>
        <span class="brand-badge">2026 MASTER</span>
      </div>
    </div>

    <div class="header-center">
      <!-- Route Drawer Trigger Button -->
      <button class="route-drawer-btn" id="btn-route-drawer" onclick="toggleRouteDrawer()">
        <span class="route-drawer-dot" id="header-route-dot" style="background:#264653"></span>
        <span class="route-drawer-label" id="header-route-label">东海道黄金三角 (18D) · 共20条路线</span>
        <svg class="icon icon-chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
      </button>

      <!-- Dual Transport Mode Capsule -->
      <div class="mode-switch-capsule">
        <button class="mode-btn active" id="mode-btn-public" onclick="setTransportMode('public')">
          <svg class="icon" viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="16" rx="2"/><path d="M4 11h16"/><path d="M12 3v8"/><path d="m8 19-2 3"/><path d="m16 19 2 3"/></svg>
          公共交通+eBike
        </button>
        <button class="mode-btn" id="mode-btn-drive" onclick="setTransportMode('drive')">
          <svg class="icon" viewBox="0 0 24 24"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
          合规自驾
        </button>
      </div>
    </div>

    <div class="header-right">
      <!-- Practical Guides Group -->
      <div class="util-group">
        <button class="btn-util" onclick="openModal('modal-rules')" title="2026 签证与自驾法律生死线">
          <svg class="icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>规制</span>
        </button>
        <button class="btn-util" onclick="openModal('modal-transit')" title="跨地交通购票、起讫参数与新干线行李">
          <svg class="icon" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
          <span>交通</span>
        </button>
        <button class="btn-util" onclick="openModal('modal-stay')" title="住宿评测、Tabelog 与 Airbnb 民泊全指南">
          <svg class="icon" viewBox="0 0 24 24"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          <span>食宿</span>
        </button>
        <button class="btn-util" onclick="openModal('modal-checklist')" title="T-60至T-1备忘清单与24h应急热线">
          <svg class="icon" viewBox="0 0 24 24"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
          <span>备忘</span>
        </button>
        <button class="btn-util" onclick="openVisaModal()" title="生成日本领事馆标准格式送签《滞在予定表》">
          <svg class="icon" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          <span>送签</span>
        </button>
      </div>

      <div class="divider-vertical"></div>

      <!-- Engine & Theme Group -->
      <div class="engine-group">
        <select class="tile-dropdown" id="tile-selector" onchange="switchBaseTile(this.value)" title="切换底图引擎">
          <option value="carto">CARTO 人文</option>
          <option value="carto_positron">CARTO 浅灰</option>
          <option value="gsi">GSI 国土院</option>
          <option value="gsi_pale">GSI 淡彩</option>
          <option value="osm">OSM 全球</option>
        </select>
        <button class="btn-icon" id="btn-theme-toggle" onclick="toggleNightTheme()" title="切换暗色山峦/和纸日间模式">
          <svg class="icon" id="theme-icon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
        <button class="btn-icon" onclick="openModal('modal-carto-key')" title="配置底图 API Key">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6"/><path d="m15.5 7.5 3 3L22 7l-3-3"/></svg>
        </button>
        <button class="btn-version-pill" onclick="openModal('modal-versions')" title="查看已构建的各网页版本矩阵">
          版本
        </button>
      </div>
    </div>
  </header>

  <!-- 2. TOP ROUTE DRAWER -->
  <div class="route-drawer-backdrop" id="route-drawer-backdrop" onclick="closeRouteDrawer()"></div>
  <div class="route-drawer" id="route-drawer">
    <div class="route-drawer-header">
      <div class="drawer-cat-tabs" id="drawer-cat-tabs">
        <button class="drawer-tab active" data-cat="all" onclick="filterDrawerCat('all')">全部路线 (20)</button>
        <button class="drawer-tab" data-cat="framework" onclick="filterDrawerCat('framework')">落地主干框架 (3)</button>
        <button class="drawer-tab" data-cat="classic" onclick="filterDrawerCat('classic')">经典与大师长线 (5)</button>
        <button class="drawer-tab" data-cat="theme" onclick="filterDrawerCat('theme')">专题深度微循环 (6)</button>
        <button class="drawer-tab" data-cat="literature" onclick="filterDrawerCat('literature')">村上文学寻踪 (6)</button>
      </div>
      <button class="drawer-close-btn" onclick="closeRouteDrawer()" title="关闭抽屉">
        <svg class="icon" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <div class="route-drawer-grid" id="route-drawer-grid">
      {DRAWER_CARDS}
    </div>
  </div>

  <!-- 3. MAIN APP SHELL -->
  <main class="app-shell">
    <!-- Left Column: Narrative & Planning Control -->
    <section class="narrative-col">
      <!-- Route Hero -->
      <div class="route-hero" id="route-hero">
        <div class="hero-top-row">
          <span class="route-cat-badge" id="hero-cat-badge">经典大长线</span>
          <span class="route-tag" id="hero-tag">ROUTE 01 · GOLDEN TRIANGLE</span>
        </div>
        <h1 class="route-name" id="hero-title">东海道黄金三角经典走廊：东京都市文明、尾张名古屋工业历史、关西古都名刹与宇治茶乡环线</h1>
        <p class="route-desc" id="hero-desc">东京(HND/NRT)进 / 大阪关西(KIX)出 · 贯通日本政治经济文化最核心大动脉。串联东京三大国家级博物馆群与江户下町刀匠、镰仓江之电古都海岸、战国尾张名城与热田神宫、JR东海磁浮铁道馆、京都千年名刹与宇治茶乡、大和奈良大佛与大阪水都商贾美食。</p>
      </div>

      <!-- Route Meta Grid (Replacing kpi-grid) -->
      <div class="route-meta-grid">
        <div class="meta-item">
          <span class="meta-label">
            <svg class="icon" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            建议总天数
          </span>
          <span class="meta-val" id="meta-days-val">18 日 / 17 晚</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">
            <svg class="icon" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
            推荐铁路通票
          </span>
          <span class="meta-val" id="meta-pass-val">SmartEX 早特早鸟折扣 (避开JR Pass)</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">
            <svg class="icon" viewBox="0 0 24 24"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
            交通组织骨干
          </span>
          <span class="meta-val" id="meta-transit-val">东海道新干线 + 地方特急 + e-Bike</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">
            <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
            起讫城市枢纽
          </span>
          <span class="meta-val" id="meta-ports-val">东京入境 / 关西离境 (不走回头路)</span>
        </div>
      </div>

      <!-- Phenology Month Pills -->
      <div class="phenology-box">
        <div class="phenology-header">
          <span class="phenology-label">
            <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
            适行物候推荐月份：
          </span>
          <span class="phenology-tip">深色高亮为该路线最佳季节</span>
        </div>
        <div class="month-pills" id="month-pills-container"></div>
      </div>

      <!-- Seasonal Advice Box -->
      <div class="seasonal-box" id="season-advice-box">
        <svg class="icon icon-lg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        <div>
          <h4 id="season-advice-title">适行季节与气候指导</h4>
          <p id="season-advice-text"></p>
        </div>
      </div>

      <!-- Sub-Navigation Tabs (4 Panels) -->
      <div class="panel-switcher">
        <button class="panel-tab active" onclick="switchSubPanel('itinerary')" id="ptab-itinerary">逐日空间轨迹与食宿</button>
        <button class="panel-tab" onclick="switchSubPanel('transit')" id="ptab-transit">跨地交通详单</button>
        <button class="panel-tab" onclick="switchSubPanel('stay')" id="ptab-stay">住宿与 Airbnb</button>
        <button class="panel-tab" onclick="switchSubPanel('budget')" id="ptab-budget">动态预算精算沙盒</button>
      </div>

      <!-- PANEL 1: ITINERARY -->
      <div id="panel-itinerary">
        <div class="day-list" id="day-list-container"></div>
      </div>

      <!-- PANEL 2: TRANSIT TABLE -->
      <div id="panel-transit" style="display:none;">
        <div class="transit-table-wrapper">
          <h3 style="font-family:var(--font-serif);font-size:0.95rem;margin-bottom:8px;color:var(--navy-900);">
            2026 核心跨地交通运行参数速查大表 (20 个区间走廊)
          </h3>
          <p style="font-size:0.72rem;color:var(--slate-500);margin-bottom:10px;">
            基于 JR 各社 2026 最新时刻运行图编制。含起讫车站名、指定席/自由席票价、耗时及换乘避坑要领。
          </p>
          <table class="transit-data-table">
            <thead>
              <tr>
                <th>序号</th>
                <th>区间走廊</th>
                <th>起讫车站名 (日文/英文)</th>
                <th>推荐交通工具与车种</th>
                <th>耗时</th>
                <th>票价 (JPY)</th>
                <th>购票与取票方式</th>
                <th>换乘要领与核心避坑</th>
              </tr>
            </thead>
            <tbody>
              {TRANSIT_TABLE_ROWS}
            </tbody>
          </table>
        </div>
      </div>

      <!-- PANEL 3: STAY & AIRBNB -->
      <div id="panel-stay" style="display:none;">
        <div class="stay-cards-grid">
          <div class="stay-card" style="border-left: 4px solid var(--vermilion);">
            <h4>日本《民泊新法》（住宅宿泊事业法）法律准绳与执照验真</h4>
            <p>
              1. <strong>合法民泊唯一识别码</strong>：房源详情必须公示『第 M + 8/9 位数字（例：第 M12345678 号）』或地方保健所简易宿所许可番号。<br>
              2. <strong>黑民宿查封取缔风险</strong>：无证黑民宿面临日本警方突击查封断水断电，订单会在入住前数天被平台强制取消，且无联网烟雾报警逃生设施。
            </p>
          </div>
          <div class="stay-card">
            <h4>京都府：百年历史「京町家（Kyomachiya）」独栋整租</h4>
            <p>
              <strong>推荐选址</strong>：东山五条、上京区西阵纺织老街、东寺南侧。<br>
              <strong>特色配置</strong>：木造纯正和室、榻榻米稻草香、信乐烧或桧木浴缸、私人枯山水坪庭（Tsuboniwa）、急须茶室。整栋每晚约 25,000–55,000 JPY。
            </p>
          </div>
          <div class="stay-card">
            <h4>东京都：下町文创平层与世田谷文艺街区公寓</h4>
            <p>
              <strong>推荐选址</strong>：谷根千（谷中根津下町木造改建平层）、世田谷三轩茶屋/下北泽（青年文艺公寓、黑胶唱片店旁）、墨田押上（晴空塔景观顶楼）。<br>
              <strong>特色配置</strong>：现代和洋折衷设计、带烘干功能的洗衣机、开放式厨房。整套每晚约 18,000–38,000 JPY。
            </p>
          </div>
          <div class="stay-card">
            <h4>爱知名古屋：荣与大须商圈现代高级 Mansion 塔楼</h4>
            <p>
              <strong>推荐选址</strong>：大须观音商圈旁、荣商业区外围白川公园周边。<br>
              <strong>特色配置</strong>：现代混凝土防震塔楼整套 2LDK，三分离干湿卫浴，适合家庭超市采购飞驒牛肉自炊。每晚约 14,000–26,000 JPY。
            </p>
          </div>
          <div class="stay-card">
            <h4>信州与飞驒高山：江户时代古民家（Kominka）复原木屋</h4>
            <p>
              <strong>推荐选址</strong>：高山上三之町外围、飞驒古川白壁水渠沿岸、木曾福岛。<br>
              <strong>特色配置</strong>：百年挑高梁柱实木住宅，客厅中心保留日式「围炉里（Irori 地炉）」与铁壶，全屋铺设地暖。每晚约 30,000–60,000 JPY。
            </p>
          </div>
          <div class="stay-card" style="border-left: 4px solid var(--amber);">
            <h4>Airbnb 入住与避坑四大铁律（违规重罚！）</h4>
            <p>
              1. <strong>严酷的垃圾分类</strong>：厨房提供 4–5 个分类桶（可燃、不可燃、塑料包装プラ、PET瓶剥皮踩扁、铝铁罐）。退房留存混装垃圾将扣除 5,000–20,000 JPY 特别清运费！<br>
              2. <strong>21:00 晚间静音公约</strong>：日本轻木住宅隔音弱，晚 9 点后严禁高声喧哗、外放音乐或室外拉动行李箱，防止邻居直接报警 110。<br>
              3. <strong>严禁直接跨城寄送行李至民宿</strong>：民泊无前台代收！应使用黑猫宅急便指定寄往附近的「大和运输直营营业所自提（センター止め）」或便利店。<br>
              4. <strong>法定身份登记</strong>：全体同行人员均须上传护照首页并完成房内平板人脸核验。
            </p>
          </div>
        </div>
      </div>

      <!-- PANEL 4: BUDGET SANDBOX -->
      <div id="panel-budget" style="display:none;">
        <div class="sandbox-container">
          <h3 style="font-family:var(--font-serif);font-size:0.95rem;margin-bottom:12px;color:var(--navy-900);">
            15–20 日自助游动态成本精算沙盒 (实时汇率: 100 JPY ≈ 4.25 RMB)
          </h3>
          <div class="slider-row">
            <div class="slider-header">
              <span>旅行总天数</span>
              <span class="mono" id="b-days-val" style="color:var(--active-color);">18 天</span>
            </div>
            <input type="range" class="slider-input" id="b-days-slider" min="15" max="20" value="18" oninput="calcBudget()">
          </div>
          <div class="slider-row">
            <div class="slider-header">
              <span>同行分摊人数</span>
              <span class="mono" id="b-pax-val" style="color:var(--active-color);">2 人</span>
            </div>
            <input type="range" class="slider-input" id="b-pax-slider" min="1" max="4" value="2" oninput="calcBudget()">
          </div>
          <div class="slider-row">
            <div class="slider-header">
              <span>传统温泉旅馆晚数 (一泊二食会席)</span>
              <span class="mono" id="b-ryokan-val" style="color:var(--active-color);">2 晚</span>
            </div>
            <input type="range" class="slider-input" id="b-ryokan-slider" min="0" max="5" value="2" oninput="calcBudget()">
          </div>

          <div class="budget-result-display">
            <div>
              <div style="font-size:0.75rem;color:var(--slate-500);font-weight:600;">预估单人全口径总支出</div>
              <div style="font-size:0.68rem;color:var(--slate-400);">含机票/签证/长途特急/住宿/餐饮/杂费</div>
            </div>
            <div>
              <span class="budget-val-big" id="b-total-rmb">¥17,800</span>
              <span class="mono" id="b-total-jpy" style="font-size:0.75rem;color:var(--slate-500);margin-left:6px;">≈ 418,800 JPY</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Right Column: Interactive Map & Elevation Dock -->
    <aside class="viewport-col">
      <div class="map-wrapper">
        <div class="map-overlay-top">
          <div class="map-chip">
            <span style="font-size:0.7rem;font-weight:600;color:var(--slate-500);">底图：</span>
            <select class="tile-select" id="tile-selector-overlay" onchange="switchBaseTile(this.value)">
              <option value="carto">CARTO 人文 (Voyager)</option>
              <option value="carto_positron">CARTO 浅灰 (Positron)</option>
              <option value="gsi">GSI 国土院标准图</option>
              <option value="gsi_pale">GSI 淡彩地形图</option>
              <option value="osm">OSM 全球开源图</option>
            </select>
          </div>
          <div class="map-chip">
            <button class="btn-util-sm" onclick="resetMapBounds()">
              <svg class="icon" viewBox="0 0 24 24"><path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></svg>
              全览路线
            </button>
          </div>
        </div>
        <div id="map-canvas"></div>
      </div>

      <!-- D3 Elevation Dock -->
      <div class="elevation-dock">
        <div class="dock-header">
          <span class="dock-title">
            <svg class="icon" viewBox="0 0 24 24"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
            D3.js 实时地形高程剖面图 (鼠标悬停剖面可联动高亮地图站点)
          </span>
          <span class="probe-readout" id="probe-readout">当前聚焦：-</span>
        </div>
        <svg id="elevation-svg"></svg>
      </div>
    </aside>
  </main>

  <!-- MODALS SYSTEM -->
  <!-- 1. Modal: Rules (Visa & Driving Law) -->
  <div class="modal-backdrop" id="modal-rules" onclick="if(event.target===this)closeModal()">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">签证资质要求与在日驾驶法律红线</h3>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <div style="background:var(--vermilion-soft);border:1px solid var(--vermilion-border);border-left:4px solid var(--vermilion);padding:12px;border-radius:6px;margin-bottom:12px;">
          <h4 style="color:var(--vermilion);margin-bottom:6px;font-size:0.85rem;">【自驾红线】中国大陆驾照在日无证驾驶刑事犯罪！</h4>
          <p style="margin-bottom:6px;">1. 日本严格遵循《1949年日内瓦道路交通公约》。<strong>中国大陆驾驶证、公证书、翻译件及国内电商平台售卖的任何“国际驾照认证件 (KIDA/KRP等)”在日本均完全无效</strong>。</p>
          <p style="margin-bottom:6px;">2. 持无效件驾车一旦临检或事故，日本警方依法按<strong>“无免許運転（无照驾驶犯罪）”</strong>立案逮捕，面临最高3年监禁或50万日元罚金，所有车辆保险直接全额拒赔，留底拘役并遣返驱逐出境。</p>
          <p>3. <strong>合法在日驾驶唯一途径</strong>：持有缔约国/地区（中国香港、中国澳门、英美加澳等）官方核发之 1 年期 IDP 实体原件；或中国台湾驾照配 JAF 官方日文译本。</p>
        </div>

        <div style="background:var(--amber-soft);border:1px solid var(--amber-border);border-left:4px solid var(--amber);padding:12px;border-radius:6px;margin-bottom:12px;">
          <h4 style="color:var(--amber);margin-bottom:6px;font-size:0.85rem;">【签证办理】福州领区归属、2026新费用与停留期警示</h4>
          <p style="margin-bottom:6px;">1. <strong>厦门属福州领区</strong>：厦门户籍及常住居民由日本国驻福州总领事馆受理，必须通过福州领区指定旅行社送签，个人无法直递。</p>
          <p style="margin-bottom:6px;">2. <strong>2026年7月1日起新规费</strong>：单次签证使馆费已上调至 <strong>715 元</strong>，多次签证 <strong>1,430 元</strong>（代办服务费另计，切勿轻信200/400元旧价宣传）。冲绳及东北三县三年多次免收使馆规费。</p>
          <p style="margin-bottom:6px;">3. <strong>电子签联网验真铁律</strong>：单次签证出签为电子签（PDF），入境海关核验时必须在手机联网环境下登录展示<strong>官方动态防伪倒计时页面</strong>，任何截屏或离线打印均被拒入。</p>
          <p style="margin-bottom:6px;">4. <strong>15–20日行程停留期匹配</strong>：标准单次签仅批复 15 天停留。若行程超过 15 天，送签时务必申请 <strong>30 天单次旅游签证</strong>（提交全覆盖机票预订单与日文滞在予定表），或办理三年/五年多次往返签，切防逾期非法滞留。</p>
          <p>5. <strong>高校学历简化通道</strong>：教育部直属全日制本科在读或毕业 3 年内，凭学信网学籍报告可免资产流水办理单次签证。</p>
        </div>

        <div style="background:var(--indigo-soft);border:1px solid var(--indigo-border);border-left:4px solid var(--indigo);padding:12px;border-radius:6px;">
          <h4 style="color:var(--indigo);margin-bottom:6px;font-size:0.85rem;">【入境申报与免税】Visit Japan Web 与 2026 免税新政</h4>
          <p style="margin-bottom:6px;">1. <strong>Visit Japan Web (VJW)</strong>：官方唯一域名 <code>vjw.digital.go.jp</code>，<strong>官方从未推出手机 App</strong>，切勿下载应用市场仿冒扣费软件。提前 2-3 天填好入境与海关表生成单一 QR 码截屏备用。</p>
          <p style="margin-bottom:6px;">2. <strong>2026年11月1日起免税变更</strong>：日本免税改为<strong>机场统一退税</strong>（店内先付含税价，离境当天在机场办理消费税退款），离境当天请多预留 1 小时。</p>
          <p>3. <strong>现金储备不可替代</strong>：日本仍是现金社会，小店、投币式洗衣机（Coin Laundry）、食券拉面机、神社纳经只收现金，单人务必备齐 20,000–30,000 日元纸币与硬币。</p>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-util" style="background:var(--washi-subtle);" onclick="closeModal()">我已完全知晓</button>
      </div>
    </div>
  </div>

  <!-- 1.1 Modal: IDP Legal Compliance Alert -->
  <div class="modal-backdrop" id="modal-idp" onclick="if(event.target===this)closeModal()">
    <div class="modal-card" style="max-width:620px;">
      <div class="modal-header" style="background:var(--vermilion);color:#fff;">
        <h3 class="modal-title" style="color:#fff;">
          <svg class="icon" viewBox="0 0 24 24" style="stroke:#fff;"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          日本自驾法定驾驶资质严正警示与合规确认
        </h3>
        <button class="modal-close" style="color:#fff;" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <div style="background:var(--vermilion-soft);border:1px solid var(--vermilion-border);border-left:4px solid var(--vermilion);padding:12px;border-radius:6px;margin-bottom:12px;">
          <h4 style="color:var(--vermilion);margin-bottom:6px;font-size:0.85rem;">【刑事红线】中国大陆驾照及电商“翻译件”在日违法！</h4>
          <p style="margin-bottom:6px;">根据日本《道路交通法》第64条与警察厅权威通告：日本仅承认缔约国依<strong>《1949年日内瓦道路交通公约》</strong>官方核发的正式“国际驾驶许可证（IDP）”，中国大陆非该公约缔约方，因此：</p>
          <ul style="margin: 0.4rem 0 0 1.2rem; line-height: 1.6;">
            <li>国内租车平台售卖的任何“国际驾照翻译认证件 (KRP/KIDA/KTA等)”在日本<strong>不具任何法律效力</strong>；</li>
            <li>持无效翻译件在日驾车，一旦被日本警察临检或卷入交通事故，日本警方将依法认定为<strong>“无免許運転（无照驾驶犯罪）”</strong>；</li>
            <li><strong>刑事后果</strong>：最高判处 3 年有期徒刑或 50 万日元罚金；所有车辆保险公司<strong>直接全额拒赔</strong>；追究全部财产赔偿责任并当场拘役、驱逐出境且长期限制再入境！</li>
          </ul>
        </div>

        <div style="background:var(--pine-soft);border:1px solid var(--pine-border);border-left:4px solid var(--pine);padding:12px;border-radius:6px;margin-bottom:12px;">
          <h4 style="color:var(--pine);margin-bottom:6px;font-size:0.85rem;">【合法合规条件】合法在日自驾的唯一资格途径</h4>
          <p>1. 持有日内瓦公约缔约国/地区官方签发的<strong>正规1年期IDP纸质实体本</strong>（如中国香港驾照+正式IDP、中国澳门IDP、美英加澳官方IDP等）；<br>
          2. 持有中国台湾地区驾照 + 台湾监理所或JAF官方认证的日文译本；<br>
          3. 持有日本官方公安委员会颁发之正规本土“日本免许证”。</p>
        </div>

        <div style="background:var(--amber-soft);border:1px solid var(--amber-border);border-left:4px solid var(--amber);padding:12px;border-radius:6px;">
          <h4 style="color:var(--amber);margin-bottom:6px;font-size:0.85rem;">【冬季行车警示】豪雪路段必须配备无钉雪胎（Studless）</h4>
          <p>1–2月在北海道、东北、信越北陆等豪雪区域租车，必须在租车时提前确认加选<strong>“无钉防滑雪胎（スタッドレスタイヤ）”</strong>与 4WD 四驱车型，遇暴风雪能见度不足时严禁盲目开入盘山公路。</p>
        </div>
      </div>
      <div class="modal-footer" style="display:flex;justify-content:flex-end;gap:8px;">
        <button class="btn-util" style="background:var(--washi-subtle);" onclick="cancelDriveMode()">返回公共交通模式（推荐）</button>
        <button class="btn-util" style="background:var(--vermilion);color:#fff;" onclick="confirmDriveMode()">我已持有合法官方IDP，确认开启自驾模式</button>
      </div>
    </div>
  </div>

  <!-- 2. Modal: Transit -->
  <div class="modal-backdrop" id="modal-transit" onclick="if(event.target===this)closeModal()">
    <div class="modal-card" style="max-width:900px;">
      <div class="modal-header">
        <h3 class="modal-title">跨地交通购票、起讫参数与新干线行李</h3>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <h4 style="color:var(--navy-900);margin-bottom:6px;">SmartEX 购票与新干线特大行李预约规定</h4>
        <p style="margin-bottom:12px;">
          1. <strong>SmartEX 手机扫码乘车</strong>：东海道·山阳·九州新干线官方平台，支持绑定海外信用卡与 Apple Wallet 虚拟 Suica/ICOCA，提前 21/28 天购买早特（Hayatoku）可享 15%–25% 优惠，闸机直接刷手机。<br>
          2. <strong>特大行李（161cm–250cm）预约</strong>：28 寸及以上大行李箱乘搭新干线，<strong>必须免费提前预订最后一排「附带特大行李放置处座席」</strong>。未预约强行带上车将被列车长当场强制征收 1,000 日元手续费并强制移置！
        </p>
        <h4 style="color:var(--navy-900);margin-bottom:6px;">2026 JR Pass 暴涨避坑实算</h4>
        <p>
          全国版 JR Pass 7 日券已暴涨至 50,000 / 53,000 日元。经典东京-名古屋-京都-大阪走廊单买全程票价仅需 19,790 日元，买全国版 Pass 人均净亏 30,000+ 日元（1,300+ 元人民币）！
          强烈推荐点对点单买或选购 <strong>JR 关西广域 5 日券 (12,000 JPY)</strong>、<strong>北陆拱形 7 日券 (30,000 JPY)</strong> 等高性价比区域 Pass。
        </p>
      </div>
      <div class="modal-footer">
        <button class="btn-util" style="background:var(--washi-subtle);" onclick="closeModal()">关闭</button>
      </div>
    </div>
  </div>

  <!-- 3. Modal: Stay & Airbnb Tips -->
  <div class="modal-backdrop" id="modal-stay" onclick="if(event.target===this)closeModal()">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">食住在地智慧与高性价比攻略</h3>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <div style="background:var(--pine-soft);border:1px solid var(--pine-border);border-left:4px solid var(--pine);padding:12px;border-radius:6px;margin-bottom:12px;">
          <h4 style="color:var(--pine);margin-bottom:6px;font-size:0.85rem;">【住】商务酒店与温泉旅馆的最佳配比</h4>
          <p style="margin-bottom:6px;"><strong>黄金组合</strong>：全程16-18晚中，<strong>80%晚数选择优质商务连锁酒店</strong>，精选 <strong>2–3 晚入住传统温泉旅馆</strong>。</p>
          <p style="margin-bottom:6px;">1. <strong>Dormy Inn 连锁酒店</strong>：强烈推荐。大多数分馆自带天然温泉大浴场与桑拿，每晚 21:30–23:00 免费供应清爽的“夜鸣拉面（酱油荞麦面）”，早餐融入地方特产，人均每晚仅需 7,000–12,000 日元。</p>
          <p style="margin-bottom:6px;">2. <strong>Toyoko Inn（东横INN）/ Super Hotel</strong>：经济托底首选，全员免费含早，价格常年平稳在 5,500–8,500 日元。</p>
          <p>3. <strong>温泉旅馆</strong>：避开每晚连住。温泉旅馆的“一泊二食（会席料理）”分量极大且仪式感重，连续食用胃肠负担大且预算昂贵。在长野、乳头温泉或山代温泉等核心节点精选体验即可。</p>
        </div>

        <div style="background:var(--indigo-soft);border:1px solid var(--indigo-border);border-left:4px solid var(--indigo);padding:12px;border-radius:6px;margin-bottom:12px;">
          <h4 style="color:var(--indigo);margin-bottom:6px;font-size:0.85rem;">【食】地道、美味且经济的美食法则</h4>
          <p style="margin-bottom:6px;">1. <strong>精明利用“午间定食（Lunch Special）”</strong>：日本诸多高档料理店（和牛烧肉、割烹、鳗鱼饭），晚餐人均常达 10,000 日元以上，但其周中午市推出的限定定食仅需 1,000–1,800 日元，品质毫不妥协。</p>
          <p style="margin-bottom:6px;">2. <strong>市民生鲜市场食堂</strong>：如金泽近江町市场、青森古川市场（Nokkedon 自选手撕海鲜丼）、鸟取贺露港。清晨直接品尝刚上岸的天然海味，性价比远超观光区餐厅。</p>
          <p style="margin-bottom:6px;">3. <strong>百货地下食品街（Depachika）晚间打折</strong>：每晚 19:00 至 20:00，大丸、伊势丹、高岛屋等百货地下街的高级和牛便当、新鲜刺身、炸物会贴上 20%–50% 的“Time Sale（タイムセール）”折扣签。</p>
          <p>4. <strong>高阶本土回转寿司</strong>：避开千篇一律的廉价连锁，认准日本老饕钟爱的“根室花丸”、“銚子丸”、“金泽まいもん寿司”，人均 2,000–3,500 日元即可享受媲美板前手握的鲜度与品质。</p>
        </div>

        <div style="background:var(--washi-subtle);border:1px solid var(--slate-200);border-left:4px solid var(--slate-500);padding:12px;border-radius:6px;">
          <h4 style="color:var(--navy-900);margin-bottom:6px;font-size:0.85rem;">【Airbnb 民泊四大生死避坑铁律】</h4>
          <p style="margin-bottom:6px;">1. <strong>查验执照编号 M</strong>：必须公示『第 MXXXXXXXX 号』，严防无证黑民泊被官方查封强制退单。<br>
          2. <strong>严禁混装垃圾</strong>：严格按可燃、不可燃、塑料包装プラ、洗净踩扁的PET瓶分类，违规扣除 5,000–20,000 JPY 清理费。<br>
          3. <strong>晚 21:00 静音公约</strong>：木造建筑隔音极弱，晚间严禁喧哗，否则邻居极易直接报警 110。<br>
          4. <strong>大件行李切勿直寄民宿</strong>：民泊无前台代收！行李应寄送至附近的「大和运输直营营业所自提（センター止め）」或便利店。</p>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-util" style="background:var(--washi-subtle);" onclick="closeModal()">关闭</button>
      </div>
    </div>
  </div>

  <!-- 4. Modal: Checklist -->
  <div class="modal-backdrop" id="modal-checklist" onclick="if(event.target===this)closeModal()">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">首次访日必备清单与 24 小时应急求助指南</h3>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <div style="background:var(--vermilion-soft);border:1px solid var(--vermilion-border);border-left:4px solid var(--vermilion);padding:12px;border-radius:6px;margin-bottom:12px;">
          <h4 style="color:var(--vermilion);margin-bottom:6px;font-size:0.85rem;">24 小时官方紧急热线通讯录</h4>
          <ul style="margin: 0.35rem 0 0 1.2rem; line-height: 1.7;">
            <li><strong>警察报警</strong>：拨打 <code>110</code> (免费直拨，公用电话按红色紧急按钮)</li>
            <li><strong>急救 / 火警救护车</strong>：拨打 <code>119</code></li>
            <li><strong>JNTO 日本观光局多语种专线</strong>：拨打 <code>050-3816-2720</code> (24小时支持中文，医疗翻译与灾害求助)</li>
            <li><strong>中国驻日使馆领保电话</strong>：拨打 <code>+81-3-6450-2195</code> / 外交部全球热线 <code>+86-10-12308</code></li>
          </ul>
        </div>

        <div style="background:var(--washi-subtle);border:1px solid var(--slate-200);border-left:4px solid var(--indigo);padding:12px;border-radius:6px;">
          <h4 style="color:var(--navy-900);margin-bottom:6px;font-size:0.85rem;">出发前倒计时准备清单 (T-60 至 T-1)</h4>
          <div style="font-size:0.78rem;line-height:1.75;color:var(--slate-700);">
            <p><strong>□ T-60 天</strong>：确定出行时段（1–2月雪季需留列车停运缓冲；9–10月初秋无红叶）；核对护照有效期 ≥6 个月、空白页 ≥2；选定福州领区指定旅行社并预订机票。</p>
            <p><strong>□ T-45 天</strong>：递交签证申请材料；特展与美术馆预约（直岛地中美术馆、李禹焕、吉卜力提前 1–3 个月官网抢订指定时段票）。</p>
            <p><strong>□ T-30 天</strong>：出签核对护照号与姓名拼音；下载日本原生 eSIM 或购买物理数据卡；预订热门不可退住宿（直岛岛上宿点等）。</p>
            <p><strong>□ T-14 天</strong>：登录 Visit Japan Web 官方网页填写申报生成单一 QR 码；打印机票行程单、酒店确认单与签证 PDF；确认购买含日本紧急医疗的境外旅游保险。</p>
            <p><strong>□ T-7 天</strong>：查询日本气象厅及各 JR 铁道公司运行预警；下载离线地图与翻译包；确认首晚酒店日文名称与地址。</p>
            <p><strong>□ T-3 天</strong>：通过「厦门高崎国际机场」微信小程序提前进行出境证件预审核；重物打包规划黑猫宅急便分箱。</p>
            <p><strong>□ T-1 天</strong>：准备 20,000–30,000 日元纸币与硬币；检查移动电源随身携带（严禁托运）；手机充满电迎接安静有序的旅程。</p>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-util" style="background:var(--washi-subtle);" onclick="closeModal()">关闭</button>
      </div>
    </div>
  </div>

  <!-- 4.1 Modal: Visa Schedule of Stay Table -->
  <div class="modal-backdrop" id="modal-visa" onclick="if(event.target===this)closeModal()">
    <div class="modal-card" style="max-width:960px;">
      <div class="modal-header">
        <h3 class="modal-title">赴日签证送签专用《滞在予定表 (Schedule of Stay)》</h3>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body" id="visa-table-container">
        <!-- Dynamically rendered -->
      </div>
      <div class="modal-footer" style="display:flex;justify-content:flex-end;gap:8px;">
        <button class="btn-util" style="background:var(--washi-subtle);" onclick="window.print()">打印 / 另存为 PDF</button>
        <button class="btn-util" style="background:var(--active-color);color:#fff;" onclick="closeModal()">关闭窗口</button>
      </div>
    </div>
  </div>

  <!-- 5. Modal: Carto Key -->
  <div class="modal-backdrop" id="modal-carto-key" onclick="if(event.target===this)closeModal()">
    <div class="modal-card" style="max-width:520px;">
      <div class="modal-header">
        <h3 class="modal-title">CARTO 底图 API Key 配置</h3>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <p style="margin-bottom:10px;">
          当前系统已内置默认 CARTO Voyager 高清人文瓦片密钥，通常无需额外修改。若您有自己的 CARTO 商业授权密钥，可在此自定义配置：
        </p>
        <input type="text" id="carto-key-input" style="width:100%;padding:8px 10px;border:1px solid var(--slate-300);border-radius:6px;font-family:var(--font-mono);font-size:0.8rem;margin-bottom:10px;" placeholder="输入 CARTO API Key">
        <div style="font-size:0.72rem;color:var(--slate-500);">密钥将自动保存在浏览器的 localStorage 中，仅在本地生效。</div>
      </div>
      <div class="modal-footer">
        <button class="btn-util" style="background:var(--washi-subtle);margin-right:6px;" onclick="closeModal()">取消</button>
        <button class="btn-util" style="background:var(--active-color);color:#fff;" onclick="saveCartoKey()">保存并刷新底图</button>
      </div>
    </div>
  </div>

  <!-- 6. Modal: Versions Matrix -->
  <div class="modal-backdrop" id="modal-versions" onclick="if(event.target===this)closeModal()">
    <div class="modal-card" style="max-width:680px;">
      <div class="modal-header">
        <h3 class="modal-title">日本深度自助旅行导览系统 · 版本矩阵导航</h3>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <div style="display:flex;flex-direction:column;gap:8px;">
          <div style="padding:10px;border:1px solid var(--slate-200);border-radius:6px;background:var(--washi-subtle);">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
              <strong style="color:var(--navy-900);">v4.0 实践版 (WBD核心落地)</strong>
              <a href="v4.html" style="font-size:0.75rem;color:var(--indigo);text-decoration:none;font-weight:700;">打开 v4.html &rarr;</a>
            </div>
            <div style="font-size:0.72rem;color:var(--slate-600);">基于 wbd.md 独立规划与 v2.html 架构构建，涵盖三大落地框架、六大专题与村上文学短线。</div>
          </div>
          <div style="padding:10px;border:1px solid var(--slate-200);border-radius:6px;background:var(--washi-subtle);">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
              <strong style="color:var(--navy-900);">v3.0 旗舰版 (Argon-v2主体)</strong>
              <a href="v3.html" style="font-size:0.75rem;color:var(--indigo);text-decoration:none;font-weight:700;">打开 v3.html &rarr;</a>
            </div>
            <div style="font-size:0.72rem;color:var(--slate-600);">43/57 黄金双栏分屏，D3 地形高程联动探针，以浮世绘《富岳三十六景》溯源为代表的大师级路线。</div>
          </div>
          <div style="padding:10px;border:1px solid var(--slate-200);border-radius:6px;background:var(--washi-subtle);">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
              <strong style="color:var(--navy-900);">v2.0 全景融合版</strong>
              <a href="v2.html" style="font-size:0.75rem;color:var(--indigo);text-decoration:none;font-weight:700;">打开 v2.html &rarr;</a>
            </div>
            <div style="font-size:0.72rem;color:var(--slate-600);">侧边折叠抽屉，分类标签联动，多源底图热切换，经典信越北陆与熊野古道纵贯线。</div>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-util" style="background:var(--washi-subtle);" onclick="closeModal()">关闭</button>
      </div>
    </div>
  </div>

  <!-- JAVASCRIPT CONTROLLER -->
  <script>
    // ==========================================
    // 1. DATASET
    // ==========================================
    const ROUTES_DATA = {ROUTES_JSON};

    // ==========================================
    // 2. APP STATE
    // ==========================================
    let currentRouteKey = 'r1_gt';
    let currentTransportMode = 'public';
    let currentSubPanel = 'itinerary';
    let currentTileKey = 'carto';
    let isNightTheme = false;
    let isRouteDrawerOpen = false;

    let map = null;
    let currentTileLayer = null;
    let routePolyline = null;
    let nodeMarkers = [];

    const TILE_CONFIGS = {{
      carto: {{
        url: 'https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png',
        attribution: '&copy; CARTO &copy; OpenStreetMap'
      }},
      carto_positron: {{
        url: 'https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png',
        attribution: '&copy; CARTO &copy; OpenStreetMap'
      }},
      gsi: {{
        url: 'https://cyberjapandata.gsi.go.jp/xyz/std/{{z}}/{{x}}/{{y}}.png',
        attribution: '&copy; 国土地理院 (GSI)'
      }},
      gsi_pale: {{
        url: 'https://cyberjapandata.gsi.go.jp/xyz/pale/{{z}}/{{x}}/{{y}}.png',
        attribution: '&copy; 国土地理院 (GSI)'
      }},
      osm: {{
        url: 'https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
        attribution: '&copy; OpenStreetMap contributors'
      }}
    }};

    // ==========================================
    // 3. MAP INITIALIZATION
    // ==========================================
    function initMap() {{
      map = L.map('map-canvas', {{
        zoomControl: true,
        attributionControl: true
      }}).setView([35.6895, 139.6917], 7);

      switchBaseTile(currentTileKey);
    }}

    function switchBaseTile(tileKey) {{
      currentTileKey = tileKey;
      if (currentTileLayer) {{
        map.removeLayer(currentTileLayer);
      }}
      const conf = TILE_CONFIGS[tileKey] || TILE_CONFIGS.carto;
      currentTileLayer = L.tileLayer(conf.url, {{
        attribution: conf.attribution,
        maxZoom: 18
      }}).addTo(map);

      // sync select elements
      document.getElementById('tile-selector').value = tileKey;
      document.getElementById('tile-selector-overlay').value = tileKey;
    }}

    function resetMapBounds() {{
      if (routePolyline && map) {{
        map.fitBounds(routePolyline.getBounds(), {{ padding: [40, 40] }});
      }}
    }}

    // ==========================================
    // 4. ROUTE SWITCHING & RENDERING
    // ==========================================
    function switchRoute(routeKey) {{
      if (!ROUTES_DATA[routeKey]) return;
      currentRouteKey = routeKey;
      activeNodeIndex = 0;
      const route = ROUTES_DATA[routeKey];

      // Update root active-color
      document.documentElement.style.setProperty('--active-color', route.color);

      // Update Header Trigger
      document.getElementById('header-route-dot').style.background = route.color;
      document.getElementById('header-route-label').textContent = route.shortName || route.title;

      // Update Hero
      const catNames = {{
        framework: '落地主干框架',
        classic: '经典大长线',
        theme: '专题深度微循环',
        literature: '村上文学寻踪'
      }};
      document.getElementById('hero-cat-badge').textContent = catNames[route.cat] || '规划路线';
      document.getElementById('hero-tag').textContent = route.tag || '';
      document.getElementById('hero-title').textContent = route.title || '';
      document.getElementById('hero-desc').textContent = route.desc || '';

      // Update Route Meta Grid
      document.getElementById('meta-days-val').textContent = route.daysText || '';
      document.getElementById('meta-pass-val').textContent = route.pass || '点对点单买';
      document.getElementById('meta-transit-val').textContent = route.transit || '干线铁道';
      document.getElementById('meta-ports-val').textContent = route.ports || '主要机场进出';

      // Update Phenology Month Pills
      renderMonthPills(route.bestMonths || []);

      // Update Seasonal Advice Box
      const advice = route.winterAdvice || route.autumnAdvice || {{ title: '气候适行建议', text: '四季皆有绝美风物。' }};
      document.getElementById('season-advice-title').textContent = advice.title;
      document.getElementById('season-advice-text').textContent = advice.text;

      // Render Day Cards
      renderDayCards(route);

      // Render Map Polyline & Markers
      renderMapRoute(route);

      // Render D3 Elevation Chart
      renderElevationChart(route);

      // Highlight Active in Drawer
      document.querySelectorAll('.drawer-card').forEach(card => {{
        card.classList.toggle('active', card.dataset.key === routeKey);
      }});
    }}

    function renderMonthPills(bestMonths) {{
      const container = document.getElementById('month-pills-container');
      container.innerHTML = '';
      for (let m = 1; m <= 12; m++) {{
        const pill = document.createElement('div');
        pill.className = 'month-pill' + (bestMonths.includes(m) ? ' active' : '');
        pill.textContent = m + '月';
        container.appendChild(pill);
      }}
    }}

    let activeNodeIndex = 0;
    let isIdpConfirmed = false;

    // Focus Node Sync (Linkage matching v2.html)
    function focusNode(idx, isFromMap) {{
      activeNodeIndex = idx;
      const route = ROUTES_DATA[currentRouteKey];
      if (!route || !route.nodes || !route.nodes[idx]) return;
      const node = route.nodes[idx];

      // 1. Update active day card
      document.querySelectorAll('.day-card').forEach((card, i) => {{
        card.classList.toggle('active', i === idx);
      }});

      // 2. Scroll card into view if clicked from map/elevation
      if (isFromMap) {{
        const targetCard = document.getElementById('day-card-' + idx);
        if (targetCard) {{
          targetCard.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
        }}
      }}

      // 3. Fly to marker and open popup
      if (nodeMarkers[idx]) {{
        map.flyTo([node.lat, node.lng], Math.max(map.getZoom(), 9), {{ duration: 0.75 }});
        nodeMarkers[idx].openPopup();
      }}

      // 4. Update probe readout
      const distKmText = (node.distKm !== undefined) ? ` · 累计 ${{node.distKm}}km` : '';
      document.getElementById('probe-readout').textContent = `当前聚焦：${{node.day}} ${{node.name}} (海拔 ${{node.elev}}m${{distKmText}})`;

      // 5. Redraw elevation profile active indicator
      renderElevationChart(route);
    }}

    function renderDayCards(route) {{
      const container = document.getElementById('day-list-container');
      container.innerHTML = '';

      route.nodes.forEach((node, idx) => {{
        const card = document.createElement('div');
        card.className = 'day-card' + (idx === activeNodeIndex ? ' active' : '');
        card.id = 'day-card-' + idx;
        card.onclick = () => focusNode(idx, false);

        const isPublic = currentTransportMode === 'public';
        const transitInfo = isPublic ? node.public : node.drive;

        let transitHtml = '';
        if (transitInfo) {{
          transitHtml = `
            <div class="transit-block">
              <div class="transit-row">
                <span>${{isPublic ? '公共交通：' : '自驾路线：'}}${{transitInfo.line || ''}}</span>
                <span class="mono" style="color:var(--vermilion);">${{transitInfo.costJPY ? '¥' + transitInfo.costJPY.toLocaleString() + '円' : ''}}</span>
              </div>
              <div class="transit-alert">${{transitInfo.alert || ''}}</div>
            </div>
          `;
        }}

        card.innerHTML = `
          <div class="day-header">
            <span class="day-badge" style="background:${{route.color}};">${{node.day}}</span>
            <span class="day-coords">${{node.pref || ''}} · 标高 ${{node.elev}}m · 累计 ${{node.distKm}}km</span>
          </div>
          <h3 class="day-name">${{node.name}}</h3>
          <p class="day-exp">${{node.exp}}</p>
          ${{transitHtml}}
          <div class="food-stay-block">
            <div class="fs-item">
              <span class="fs-label">在地美食推荐</span>
              <span class="fs-val">${{node.food || '当地名物'}} <span class="tabelog-tag">${{node.tabelog ? '<svg class="icon" style="width:10px;height:10px;fill:var(--amber);stroke:var(--amber);vertical-align:baseline;" viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg> ' + node.tabelog : ''}}</span></span>
            </div>
            <div class="fs-item">
              <span class="fs-label">住宿精选 / 民宿建议</span>
              <span class="fs-val">${{node.stay || '推荐就近入住枢纽车站周边'}}</span>
            </div>
          </div>
        `;

        container.appendChild(card);
      }});
    }}

    function renderMapRoute(route) {{
      if (!map) return;

      // Clear existing markers
      nodeMarkers.forEach(m => map.removeLayer(m));
      nodeMarkers = [];

      if (routePolyline) {{
        map.removeLayer(routePolyline);
      }}

      const latlngs = route.nodes.map(n => [n.lat, n.lng]);

      // Add polyline
      routePolyline = L.polyline(latlngs, {{
        color: route.color,
        weight: 4,
        opacity: 0.85,
        lineJoin: 'round'
      }}).addTo(map);

      // Add SVG Circle Markers
      route.nodes.forEach((n, idx) => {{
        const iconHtml = `
          <div style="background:${{route.color}};width:20px;height:20px;border-radius:50%;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.4);display:flex;align-items:center;justify-content:center;color:#fff;font-size:9.5px;font-family:var(--font-mono);font-weight:700;cursor:pointer;">
            ${{idx + 1}}
          </div>
        `;
        const customIcon = L.divIcon({{
          html: iconHtml,
          className: 'custom-node-icon',
          iconSize: [20, 20],
          iconAnchor: [10, 10]
        }});

        const marker = L.marker([n.lat, n.lng], {{ icon: customIcon }}).addTo(map);
        marker.bindPopup(`
          <div style="font-family:var(--font-sans);font-size:12px;padding:2px;">
            <strong style="color:var(--navy-900);font-size:13px;">${{n.name}}</strong><br>
            <span style="color:var(--slate-500);font-size:11px;">${{n.day}} · 标高 ${{n.elev}}m · 累计 ${{n.distKm}}km</span><br>
            <span style="color:var(--slate-700);margin-top:3px;display:block;">${{n.food || ''}}</span>
          </div>
        `);

        marker.on('click', () => {{
          focusNode(idx, true);
        }});

        nodeMarkers.push(marker);
      }});

      // Auto fit
      map.fitBounds(routePolyline.getBounds(), {{ padding: [40, 40] }});
    }}

    // ==========================================
    // 5. D3.JS ELEVATION CHART (v2.html Linkage)
    // ==========================================
    function renderElevationChart(route) {{
      const svg = d3.select('#elevation-svg');
      svg.selectAll('*').remove();

      const containerNode = document.getElementById('elevation-svg');
      const width = containerNode.clientWidth || 400;
      const height = containerNode.clientHeight || 119;
      const margin = {{ top: 10, right: 15, bottom: 25, left: 35 }};

      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;

      const data = route.nodes.map((n, i) => ({{
        idx: i,
        name: n.name,
        day: n.day,
        elev: n.elev,
        dist: n.distKm
      }}));

      const maxDist = d3.max(data, d => d.dist) || 100;
      const maxElev = Math.max(1200, (d3.max(data, d => d.elev) || 1000) * 1.15);

      const xScale = d3.scaleLinear().domain([0, maxDist]).range([0, innerWidth]);
      const yScale = d3.scaleLinear().domain([0, maxElev]).range([innerHeight, 0]);

      const g = svg.append('g')
        .attr('transform', `translate(${{margin.left}}, ${{margin.top}})`);

      // Gradient Area
      const defs = svg.append('defs');
      const gradient = defs.append('linearGradient')
        .attr('id', 'elev-grad')
        .attr('x1', '0%').attr('y1', '0%')
        .attr('x2', '0%').attr('y2', '100%');
      gradient.append('stop').attr('offset', '0%').attr('stop-color', route.color).attr('stop-opacity', 0.45);
      gradient.append('stop').attr('offset', '100%').attr('stop-color', route.color).attr('stop-opacity', 0.05);

      const area = d3.area()
        .x(d => xScale(d.dist))
        .y0(innerHeight)
        .y1(d => yScale(d.elev))
        .curve(d3.curveMonotoneX);

      const line = d3.line()
        .x(d => xScale(d.dist))
        .y(d => yScale(d.elev))
        .curve(d3.curveMonotoneX);

      g.append('path')
        .datum(data)
        .attr('fill', 'url(#elev-grad)')
        .attr('d', area);

      g.append('path')
        .datum(data)
        .attr('fill', 'none')
        .attr('stroke', route.color)
        .attr('stroke-width', 2.5)
        .attr('d', line);

      // Axes
      const xAxis = d3.axisBottom(xScale).ticks(5).tickFormat(d => d + 'km');
      const yAxis = d3.axisLeft(yScale).ticks(3).tickFormat(d => d + 'm');

      g.append('g')
        .attr('transform', `translate(0, ${{innerHeight}})`)
        .call(xAxis)
        .attr('color', 'var(--slate-400)')
        .attr('font-size', '9px')
        .attr('font-family', 'var(--font-mono)');

      g.append('g')
        .call(yAxis)
        .attr('color', 'var(--slate-400)')
        .attr('font-size', '9px')
        .attr('font-family', 'var(--font-mono)');

      // Active guide vertical line
      const activeDatum = data[activeNodeIndex];
      if (activeDatum) {{
        g.append('line')
          .attr('x1', xScale(activeDatum.dist))
          .attr('x2', xScale(activeDatum.dist))
          .attr('y1', 0)
          .attr('y2', innerHeight)
          .attr('stroke', '#d97706')
          .attr('stroke-width', 2)
          .attr('stroke-dasharray', '3,2');
      }}

      // Interactive Circles
      const nodesG = g.selectAll('.elev-node')
        .data(data)
        .enter()
        .append('g')
        .attr('class', 'elev-node')
        .style('cursor', 'pointer')
        .on('click', (event, d) => {{
          focusNode(d.idx, true);
        }});

      nodesG.append('circle')
        .attr('cx', d => xScale(d.dist))
        .attr('cy', d => yScale(d.elev))
        .attr('r', (d, i) => i === activeNodeIndex ? 6.5 : 4)
        .attr('fill', (d, i) => i === activeNodeIndex ? '#f59e0b' : route.color)
        .attr('stroke', '#ffffff')
        .attr('stroke-width', 2);

      // Probe tracker line
      const probeLine = g.append('line')
        .attr('y1', 0).attr('y2', innerHeight)
        .attr('stroke', 'var(--slate-400)')
        .attr('stroke-width', 1)
        .attr('stroke-dasharray', '3,3')
        .style('display', 'none');

      svg.on('mousemove', function(event) {{
        const [mx] = d3.pointer(event, g.node());
        if (mx >= 0 && mx <= innerWidth) {{
          probeLine.style('display', null).attr('x1', mx).attr('x2', mx);
          const dist = xScale.invert(mx);
          let closest = data[0];
          let minDiff = Math.abs(data[0].dist - dist);
          data.forEach(d => {{
            const diff = Math.abs(d.dist - dist);
            if (diff < minDiff) {{ minDiff = diff; closest = d; }}
          }});
          const closestNode = route.nodes[closest.idx];
          const distKmText = (closestNode.distKm !== undefined) ? ` · 累计 ${{closestNode.distKm}}km` : '';
          document.getElementById('probe-readout').textContent = `当前聚焦：${{closestNode.day}} ${{closestNode.name}} (海拔 ${{closestNode.elev}}m${{distKmText}})`;
        }}
      }}).on('mouseleave', function() {{
        probeLine.style('display', 'none');
        const activeNode = route.nodes[activeNodeIndex];
        if (activeNode) {{
          const distKmText = (activeNode.distKm !== undefined) ? ` · 累计 ${{activeNode.distKm}}km` : '';
          document.getElementById('probe-readout').textContent = `当前聚焦：${{activeNode.day}} ${{activeNode.name}} (海拔 ${{activeNode.elev}}m${{distKmText}})`;
        }}
      }});
    }}

    // ==========================================
    // 6. ROUTE DRAWER & SUBPANEL CONTROLLERS
    // ==========================================
    function toggleRouteDrawer() {{
      if (isRouteDrawerOpen) closeRouteDrawer();
      else openRouteDrawer();
    }}

    function openRouteDrawer() {{
      isRouteDrawerOpen = true;
      document.getElementById('route-drawer').classList.add('open');
      document.getElementById('route-drawer-backdrop').classList.add('show');
      document.getElementById('btn-route-drawer').classList.add('open');
    }}

    function closeRouteDrawer() {{
      isRouteDrawerOpen = false;
      document.getElementById('route-drawer').classList.remove('open');
      document.getElementById('route-drawer-backdrop').classList.remove('show');
      document.getElementById('btn-route-drawer').classList.remove('open');
    }}

    function selectRouteFromDrawer(key) {{
      closeRouteDrawer();
      switchRoute(key);
    }}

    function filterDrawerCat(cat) {{
      document.querySelectorAll('.drawer-tab').forEach(t => {{
        t.classList.toggle('active', t.dataset.cat === cat);
      }});

      document.querySelectorAll('.drawer-card').forEach(card => {{
        if (cat === 'all' || card.dataset.cat === cat) {{
          card.style.display = 'block';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    function setTransportMode(mode) {{
      if (mode === 'drive' && !isIdpConfirmed) {{
        openModal('modal-idp');
        return;
      }}
      currentTransportMode = mode;
      document.getElementById('mode-btn-public').classList.toggle('active', mode === 'public');
      document.getElementById('mode-btn-drive').classList.toggle('active', mode === 'drive');

      // Re-render day cards with new transport info
      const route = ROUTES_DATA[currentRouteKey];
      if (route) {{
        renderDayCards(route);
      }}
    }}

    function confirmDriveMode() {{
      isIdpConfirmed = true;
      closeModal();
      setTransportMode('drive');
    }}

    function cancelDriveMode() {{
      closeModal();
      setTransportMode('public');
    }}

    function openVisaModal() {{
      const route = ROUTES_DATA[currentRouteKey];
      if (!route) return;
      const container = document.getElementById('visa-table-container');
      const rowsHtml = route.nodes.map(n => `
        <tr>
          <td class="mono" style="white-space:nowrap;font-weight:700;">${{n.day}}</td>
          <td><strong>${{n.name}}</strong><br><span style="color:var(--slate-500);font-size:0.75rem;">${{n.pref || ''}} · 行程游览与文化探索</span></td>
          <td style="font-size:0.75rem;">${{currentTransportMode === 'public' ? (n.public ? n.public.line : '新干线 / 在来线特急') : 'レンタカー (Rental Car)'}}</td>
          <td style="font-size:0.75rem;">${{n.stay ? n.stay.split('(')[0] : '车站周边商务酒店'}}<br><span class="mono" style="color:var(--slate-500);">TEL: ${{n.stayTel || '03-3212-2424'}}</span></td>
        </tr>
      `).join('');

      container.innerHTML = `
        <p style="font-size:0.8rem;color:var(--slate-600);margin-bottom:10px;">
          当前申请路线：<strong>${{route.title}}</strong><br>
          <span style="color:var(--slate-500);">提示：根据日本外务省标准格式自动生成，可直接使用浏览器打印（Ctrl+P / Cmd+P）另存为 PDF 提交福州领区指定代办旅行社。</span>
        </p>
        <table class="visa-table">
          <thead>
            <tr>
              <th style="width:12%;">年月日 (Day)</th>
              <th style="width:38%;">行動予定 (Activity Plan)</th>
              <th style="width:25%;">交通機関 (Transport)</th>
              <th style="width:25%;">宿泊先・連絡先 (Accommodation & Tel)</th>
            </tr>
          </thead>
          <tbody>${{rowsHtml}}</tbody>
        </table>
      `;
      openModal('modal-visa');
    }}

    function switchSubPanel(panelId) {{
      currentSubPanel = panelId;
      const panels = ['itinerary', 'transit', 'stay', 'budget'];
      panels.forEach(p => {{
        const el = document.getElementById('panel-' + p);
        const tab = document.getElementById('ptab-' + p);
        if (el && tab) {{
          if (p === panelId) {{
            el.style.display = 'block';
            tab.classList.add('active');
          }} else {{
            el.style.display = 'none';
            tab.classList.remove('active');
          }}
        }}
      }});
    }}

    // ==========================================
    // 7. MODALS
    // ==========================================
    function openModal(modalId) {{
      const m = document.getElementById(modalId);
      if (m) m.classList.add('show');
    }}

    function closeModal() {{
      document.querySelectorAll('.modal-backdrop').forEach(m => m.classList.remove('show'));
    }}

    function saveCartoKey() {{
      const key = document.getElementById('carto-key-input').value.trim();
      if (key) {{
        localStorage.setItem('carto_api_key', key);
        TILE_CONFIGS.carto.url = `https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png?api_key=${{key}}`;
        switchBaseTile(currentTileKey);
      }}
      closeModal();
    }}

    function toggleNightTheme() {{
      isNightTheme = !isNightTheme;
      document.body.classList.toggle('theme-night', isNightTheme);
      localStorage.setItem('theme_night', isNightTheme ? '1' : '0');

      // Update theme toggle icon
      const themeIcon = document.getElementById('theme-icon');
      if (isNightTheme) {{
        themeIcon.innerHTML = '<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>';
        switchBaseTile('carto_positron');
      }} else {{
        themeIcon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';
        switchBaseTile('carto');
      }}
    }}

    // ==========================================
    // 8. BUDGET SANDBOX
    // ==========================================
    function calcBudget() {{
      const days = parseInt(document.getElementById('b-days-slider').value, 10);
      const pax = parseInt(document.getElementById('b-pax-slider').value, 10);
      const ryokan = parseInt(document.getElementById('b-ryokan-slider').value, 10);

      document.getElementById('b-days-val').textContent = days + ' 天';
      document.getElementById('b-pax-val').textContent = pax + ' 人';
      document.getElementById('b-ryokan-val').textContent = ryokan + ' 晚';

      // Cost calculation in RMB (based on 100 JPY ≈ 4.25 RMB)
      const flight = 3800; // direct return flight
      const visa = 850;   // eVISA + agency
      const transit = 2400 + (days - 15) * 80; // intercity + local
      const normalHotelNights = days - 1 - ryokan;
      const hotelCost = (normalHotelNights * 550) / (pax > 1 ? 1.8 : 1);
      const ryokanCost = ryokan * 1400; // Kaiseki + onsen
      const foodCost = days * 280;
      const ticketsAndMisc = days * 60;

      const totalRMB = Math.round(flight + visa + transit + hotelCost + ryokanCost + foodCost + ticketsAndMisc);
      const totalJPY = Math.round(totalRMB / 0.0425);

      document.getElementById('b-total-rmb').textContent = '¥' + totalRMB.toLocaleString() + ' RMB';
      document.getElementById('b-total-jpy').textContent = '≈ ' + totalJPY.toLocaleString() + ' JPY';
    }}

    // ==========================================
    // 9. DOM INITIALIZATION
    // ==========================================
    window.addEventListener('DOMContentLoaded', () => {{
      initMap();
      switchRoute(currentRouteKey);
      calcBudget();

      // Load saved theme
      if (localStorage.getItem('theme_night') === '1') {{
        toggleNightTheme();
      }}
    }});
  </script>
</body>
</html>
"""

# Write to OUTPUT_FILE
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)

print("Master index.html generated successfully!")
print("File size:", os.path.getsize(OUTPUT_FILE), "bytes")
