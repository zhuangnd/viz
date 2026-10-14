# -*- coding: utf-8 -*-
"""
Build script for japan-travel-guide/v3.html
Aggregates all 4 previous versions into a Version Matrix hub.
Uses japan_deep_travel_interactive_guide_argon-v2.html as the primary body.
Enhances Route 1 with Tokyo, Tokyo National Museum, Sumida Hokusai Museum,
Katsushika Hokusai Thirty-Six Views of Mount Fuji, Obuse Hokusai-kan,
Gansho-in Eight-Direction Phoenix, Matsumoto Castle, Kamikochi, etc.
Integrates 2026 Visa & Driving guidelines, MapCodes, multi-tile mapping with CARTO Key.
Zero emojis, SVG icons prioritized.
"""
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGON_V2_PATH = os.path.join(BASE_DIR, "japan_deep_travel_interactive_guide_argon-v2.html")
OUTPUT_V3_PATH = os.path.join(BASE_DIR, "v3.html")

with open(ARGON_V2_PATH, "r", encoding="utf-8") as f:
    argon_content = f.read()

# 1. Extract r2 to r6 code from argon-v2
r2_match = re.search(r'(r2:\s*\{.*?)(?=\n\s*\};\s*\n\s*//\s*=)', argon_content, re.DOTALL)
if not r2_match:
    raise ValueError("Could not extract r2..r6 from argon-v2.html")

r2_to_r6_code = r2_match.group(1).rstrip()

# Clean up any '★' in r4, r5, r6 titles in data if any
r2_to_r6_code = r2_to_r6_code.replace("★", "")

# 2. Define the enhanced Flagship Route 1
r1_code = '''r1: {
    id: "r1",
    tag: "ROUTE 01 · TOKYO CULTURE, HOKUSAI UKIYO-E, CENTRAL ALPS & HOKURIKU CRAFTS",
    title: "本州脊梁与千年古道：东京博物馆集群、浮世绘《富岳三十六景》、信越北陆加贺物语与关西名刹纵贯线",
    desc: "东京(HND/NRT)进 / 大阪关西(KIX)出 · 溯源浮世绘大师葛饰北斋《富岳三十六景》灵感线，串联东京国立博物馆与墨田北斋馆、信州小布施晚年肉笔画圣地、国宝松本城天守、阿尔卑斯上高地、五箇山合掌造、加贺百万石工艺与关西千年名刹。",
    color: "#264653",
    daysText: "18 日 / 17 晚",
    maxElev: "1,505 m (上高地梓川)",
    trailKm: "42.0 km",
    baseCostRMB: 19800,
    bestMonths: [4, 5, 6, 9, 10, 11],
    nodes: [
      {
        day: "D1–D2",
        name: "东京：下町历史遗存、东京国立博物馆与墨田北斋美术馆（《富岳三十六景》诞生之源）",
        pref: "东京都",
        lat: 35.7188, lng: 139.7765,
        elev: 24, distKm: 0,
        exp: "【溯源浮世绘与国宝鉴赏】落地东京。漫步谷中银座老街与根津神社千本鸟居；参访上野【东京国立博物馆】（本馆及法隆寺宝物馆，日本最高规格文物典藏）；下午前往墨田区【墨田北斋美术馆】（妹岛和世设计建筑，葛饰北斋诞生地），瞻仰《富岳三十六景·神奈川冲浪里》与《凯风快晴（红富士）》早期珍罕原版拓印，追溯江户平民艺术巅峰。",
        public: {
          line: "成田特急N'EX / 京成Skyliner直达市区 + 都营大江户线(两国站)/JR山手线(上野站)",
          costJPY: 3200,
          alert: "成田机场出关后在JR东日本旅行服务中心兑换周游券；东京国立博物馆建议预留3小时；墨田北斋馆周一休馆。"
        },
        drive: {
          line: "首都高速都心环线(C1) → 上野线 → 停靠上野公园地下停车场",
          costJPY: 1950,
          mapCode: "738 884*77",
          alert: "东京市区道路复杂狭窄，停车费用极高，首日强烈建议使用公共交通及地下铁通票。"
        },
        food: "浅草 并木薮荞麦（百年老铺鸭南蛮荞麦，Tabelog 3.78） & 谷中银座 招财猫今川烧",
        tabelog: "3.78",
        stay: "上野 Dormy Inn 徒步圈 / 东京站丸之内大都会酒店 (人均 9,500 JPY)",
        stayTel: "03-3211-2233"
      },
      {
        day: "D3–D4",
        name: "浅间山麓：轻井泽高原洋风近代史与《富岳三十六景·轻井泽》山岳记忆",
        pref: "长野县 (北佐久郡)",
        lat: 36.3418, lng: 138.6353,
        elev: 940, distKm: 145,
        exp: "【对应《富岳三十六景·信州浅间山》】乘坐北陆新干线直达高原名胜轻井泽。对照北斋浮世绘中浅间山火山喷烟意象与中山道驿站旅情；探访旧轻井泽银座通、星野榆树街小镇与近代建筑大师之作；漫步云场池，感受高原落叶松林初秋红叶与冬雪的极致空灵。",
        public: {
          line: "JR北陆新干线 Asama号(东京至轻井泽仅1小时10分) + 西武高原观光巴士",
          costJPY: 5490,
          alert: "北陆拱形铁路周游券(Hokuriku Arch Pass)全额覆盖北陆新干线普通车指定席；轻井泽站南口可免费接驳星野区域。"
        },
        drive: {
          line: "关越自动车道（藤冈JCT） → 上信越自动车道（碓冰轻井泽IC出） → 国道18号",
          costJPY: 4100,
          mapCode: "292 645 831*25",
          alert: "碓冰峠山道坡度大、弯道急；11月至次年4月出车务必配齐防滑雪胎。"
        },
        food: "轻井泽 川上庵（名物核桃酱冷蘸荞麦面，Tabelog 3.65） & 泽村SAWAMURA欧式烘焙",
        tabelog: "3.65",
        stay: "轻井泽 虹夕诺雅 / 星野 BEB5 轻井泽 (人均 11,800 JPY)",
        stayTel: "0267-45-6000"
      },
      {
        day: "D5–D6",
        name: "栗之乡小布施：葛饰北斋晚年肉笔画圣地（北斋馆·岩松院八方睨之凤凰图） → 国宝善光寺",
        pref: "长野县 (小布施町/长野市)",
        lat: 36.6958, lng: 138.3142,
        elev: 360, distKm: 215,
        exp: "【全线核心艺术圣地】探访信州“栗之町”小布施。葛饰北斋83岁高龄受豪商高井鸿山资助隐居于此，创作出晚年肉笔画巅峰。参访【北斋馆】（珍藏祭屋台《怒涛图·男浪女浪》天花板真迹）；漫步至古刹【岩松院】，仰望本堂21块榻榻米巨大的北斋绝笔天井画《八方睨之凤皇图》（历经170余年矿物颜料依旧艳丽惊人，无论站立殿内任何角落，凤凰利目皆凝视观者）；午后参拜根本道场【国宝善光寺】体验“戒坛巡礼”（于绝对黑暗的地下回廊中摸索极乐之锁）。",
        public: {
          line: "信浓铁道(轻井泽至长野) + 长野电铁特急Yukemuri号(长野至小布施站) + 善光寺门前巴士",
          costJPY: 2850,
          alert: "长野电铁特急展望席无需额外加价，先到先得；岩松院凤凰图讲解每15分钟一场，内部禁止摄影。"
        },
        drive: {
          line: "上信越自动车道（信州中野IC出） → 国道403号北斋小道直达小布施町",
          costJPY: 1650,
          mapCode: "248 107 432*14",
          alert: "小布施老街保存有传统“栗之小径”，车辆需停放于外围町营停车场后步行入内。"
        },
        food: "小布施堂 栗蒸羊羹与秋季限定朱雀栗子泥（Tabelog 3.72） & 善光寺门前 八幡屋礒五郎七味唐辛子",
        tabelog: "3.72",
        stay: "小布施 桝一客殿（古酿酒厂改建精品和宿） / 长野 大都会酒店 (人均 8,900 JPY)",
        stayTel: "026-247-2111"
      },
      {
        day: "D7–D8",
        name: "国宝松本城（五重木造天守） → 安昙野山葵田 → 北阿尔卑斯上高地梓川（神之降临地）",
        pref: "长野县 (松本市/安昙野)",
        lat: 36.2380, lng: 137.9720,
        elev: 1505, distKm: 295,
        exp: "参访日本现存最古老五重六层木造天守【国宝松本城】，在黑漆白灰之间品读战国防御智慧；北上安昙野清泉涌水保护区，在黑泽明电影《梦》取景地【大王山葵农场】看古朴水车转动；深入北阿尔卑斯圣地【上高地】（梓川清流、大正池枯木林与穗高连峰倒影），在河童桥听落叶松林风声（1–2月封山期调整为地狱谷野猿公苑雪猴泡汤与美原高原雪原漫步）。",
        public: {
          line: "JR篠之井线特急Shinano至松本；换乘Alpico电铁至新岛岛站，转专用环保登山巴士至上高地",
          costJPY: 4750,
          alert: "上高地属国家公园核心保护区，禁止任何外来私家车驶入；大正池下车徒步至河童桥单程约1小时。"
        },
        drive: {
          line: "长野自动车道（松本IC出） → 国道158号至泽渡（Sawando）停车场换乘穿梭接驳车",
          costJPY: 2100,
          mapCode: "405 281 723*66",
          alert: "自驾车辆必须停靠在泽渡停车场，往返穿梭巴士票价 2,400 JPY/人。"
        },
        food: "松本 山贼烧（酥脆香蒜炸鸡排） & 安昙野 现磨现擦生山葵冷手打十割荞麦面",
        tabelog: "3.68",
        stay: "上高地 帝国酒店（秋季） / 松本 扉温泉 明神馆（冬季雪见露天） (人均 14,500 JPY)",
        stayTel: "0263-31-2000"
      },
      {
        day: "D9–D10",
        name: "木曾路江户宿场（妻笼宿·马笼宿古道） → 飞驒高山三町通老街",
        pref: "长野县 / 岐阜县",
        lat: 35.5781, lng: 137.5684,
        elev: 580, distKm: 390,
        exp: "踏上江户五街道之一的【中山道·木曾路】，徒步妻笼宿至马笼宿约8公里的森林石板古道，保留江户时代的黑色木格窗与水车；午后穿越安房山脉隧道抵达飞驒高山，漫步“上三之町”传统建造物群保护区，触摸江户官府“高山阵屋”四百年杉木柱梁。",
        public: {
          line: "JR中央本线特急至中津川站，转浓飞木曾巴士；前往高山转JR高山本线特急Hida号",
          costJPY: 5200,
          alert: "妻笼至马笼古道徒步约需2.5–3小时，可在观光案内所办理行李异地托运送达服务。"
        },
        drive: {
          line: "国道19号木曾古道快速路 → 国道158号安房岭收费隧道直通飞驒高山",
          costJPY: 1800,
          mapCode: "191 195 210*33",
          alert: "安房岭隧道长达4.3公里，出隧道后气温骤降，冬季路面易有暗冰。"
        },
        food: "飞驒高山 坂口屋 飞驒牛握寿司（Tabelog 3.66） & 朴叶味噌炭火和牛烧肉",
        tabelog: "3.66",
        stay: "飞驒高山 本阵平野屋 花兆庵 / 高山樱庵 (人均 9,800 JPY)",
        stayTel: "0577-34-1234"
      },
      {
        day: "D11–D12",
        name: "世界文化遗产【五箇山·相仓合掌集落】 → 加贺工艺名都金泽（兼六园·21世纪美术馆）",
        pref: "富山县 / 石川县",
        lat: 36.5613, lng: 136.6562,
        elev: 210, distKm: 485,
        exp: "避开白川乡喧嚣商业人流，深入富山县深山更为原始静谧的【五箇山相仓合掌村】，参访60度陡峭茅草屋顶与江户手抄和纸作坊；午后直抵加贺百万石文化之都【金泽】，漫步日本三大名园之首“兼六园”（秋季红叶、冬季宏伟雪吊挂），对比妹岛和世设计的“金泽21世纪美术馆”泳池装置；夜游东茶屋街加贺友禅染与金箔工坊。",
        public: {
          line: "高山站搭乘浓飞/北铁世界遗产巴士至五箇山相仓口，后直抵金泽站东口",
          costJPY: 3900,
          alert: "世界遗产巴士需提前在浓飞巴士官网预约指定席，旺季座位紧俏。"
        },
        drive: {
          line: "东海北陆自动车道（五箇山IC出） → 白川乡IC → 北陆自动车道（金泽西IC）",
          costJPY: 2450,
          mapCode: "41 529 184*22",
          alert: "五箇山村落内道路狭窄，请依指示停入村口公营停车场并缴付保存协力金。"
        },
        food: "金泽 近江町市场 山さん寿司 海鲜丼（Tabelog 3.74） & 加贺传统车麸关东煮",
        tabelog: "3.74",
        stay: "金泽 日航酒店 / 金泽 白草庵 和室旅馆 (人均 8,500 JPY)",
        stayTel: "076-234-1111"
      },
      {
        day: "D13–D14",
        name: "越前禅宗大本山永平寺 → 芦原温泉 → 东寻坊安山岩海蚀崖",
        pref: "福井县",
        lat: 36.0652, lng: 136.2216,
        elev: 125, distKm: 565,
        exp: "乘北陆新干线至福井，深入大正元年杉树遮天蔽日的日本曹洞宗大本山【永平寺】（770年道元禅师清修圣地，漫步伞松阁欣赏昭和名家156幅花鸟草木天井画）；傍晚前往日本海狂澜激荡的【东寻坊】辉石安山岩柱状节理海蚀崖，听滔天海浪与海鸥啼鸣。",
        public: {
          line: "北陆新干线至福井站，换乘京福巴士特急永平寺线；转越前铁道至芦原温泉",
          costJPY: 3100,
          alert: "永平寺内须脱鞋换穿拖鞋，木质走廊极凉，建议自备厚保暖袜子。"
        },
        drive: {
          line: "北陆自动车道（福井北IC出） → 国道364号永平寺溪谷 → 越前海岸线",
          costJPY: 1750,
          mapCode: "63 658 310*15",
          alert: "东寻坊海蚀崖边缘无防护栏，海风强劲，拍照注意脚下湿滑岩面。"
        },
        food: "越前 越前蟹（冬令松叶蟹极致刺身/蒸蟹） & 越前萝卜泥冷荞麦面（Oroshi Soba）",
        tabelog: "3.69",
        stay: "芦原温泉 灰屋（Haiya）传统茶室风旅馆 (人均 13,500 JPY)",
        stayTel: "0776-78-5555"
      },
      {
        day: "D15–D16",
        name: "古都京都：三十三间堂（千尊观音群雕） → 南禅寺水路阁 → 宇治平等院凤凰堂",
        pref: "京都府",
        lat: 35.0116, lng: 135.7681,
        elev: 55, distKm: 690,
        exp: "乘坐特急雷鸟号沿琵琶湖西岸南下抵达京都。参拜【三十三间堂】瞻仰长达120米正殿内整齐排列的1001尊平安时代国宝木造千手观音立像与风神雷神像；避开拥挤清水寺，漫步【南禅寺】方丈枯山水与明治时代古红砖【水路阁】；前往宇治参拜【平等院凤凰堂】（10日元硬币图案建筑原型，藤原赖通建造的净土宗池泉舟游式名园）。",
        public: {
          line: "JR特急雷鸟号(Thunderbird)直达京都站；京阪电车与JR奈良线覆盖宇治",
          costJPY: 4400,
          alert: "三十三间堂堂内严禁拍照，建议租借官方语音导览深入理解平安雕刻精髓。"
        },
        drive: {
          line: "名神高速（京都东IC出），建议停放酒店车库后选用地下铁与步行",
          costJPY: 2800,
          mapCode: "7 618 412*08",
          alert: "京都古城区路窄单行道多且车位昂贵，市区游览推荐地下铁+Bus一日券。"
        },
        food: "京都 南禅寺 顺正 汤豆腐（Tabelog 3.63） & 宇治 中村藤吉 本店生茶冻抹茶芭菲",
        tabelog: "3.63",
        stay: "京都 八条口 大和ROYNET酒店 / 岚山 渡月亭 (人均 9,800 JPY)",
        stayTel: "075-693-0011"
      },
      {
        day: "D17–D18",
        name: "大阪水都漫步（中之岛近代建筑·木津批发市场） → 关西国际机场(KIX)返航",
        pref: "大阪府",
        lat: 34.6937, lng: 135.5023,
        elev: 10, distKm: 765,
        exp: "漫步水都大阪核心【中之岛】，欣赏红砖造大阪市中央公会堂（冈田信一郎设计）与中之岛美术馆；清晨至市民生鲜后厨房【木津批发市场】享用新鲜海鲜盖饭，采购关西传统昆布与伴手礼；下午搭乘JR关西空港特急 Haruka号直达机场，顺利出境返程。",
        public: {
          line: "大阪Osaka Metro地下铁御堂筋线 + JR关西特急 Haruka号(35分钟直达关西机场)",
          costJPY: 2850,
          alert: "Haruka特急建议提前在JR西日本订票系统绑定IC卡，可享外国人特惠折扣票。"
        },
        drive: {
          line: "阪神高速1号环状线 → 阪神高速4号湾岸线至关西国际机场联络桥还车",
          costJPY: 2150,
          mapCode: "1 285 419*50",
          alert: "机场跨海大桥在强台风天气可能临时管制封闭，返程请预留至少3.5小时提前量。"
        },
        food: "大阪 黑门/木津市场 炭火烤河豚定食 & 福太郎 正宗大阪烧/葱油烧",
        tabelog: "3.71",
        stay: "大阪 难波辉盛阁国际公寓 / 温暖的家 (当日返程) (人均 8,800 JPY)",
        stayTel: "06-6635-7111"
      }
    ]
  }'''

NEW_ROUTES_DATA = f'''const ROUTES_DATA = {{
  {r1_code},
  {r2_to_r6_code}
}};'''

# 3. Replace ROUTES_DATA in the HTML text
routes_pattern = re.compile(r'const ROUTES_DATA = \{.*?\n\};\n', re.DOTALL)
if not routes_pattern.search(argon_content):
    raise ValueError("Could not find const ROUTES_DATA = { ... }; block in argon-v2.html")

new_html = routes_pattern.sub(NEW_ROUTES_DATA + '\n', argon_content)

# 4. Update Title
new_html = new_html.replace(
    "<title>日本 15–20 日深度自助旅行交互式导览平台 | Editorial Cartography</title>",
    "<title>日本 15–20 日深度自助旅行终极交互导览系统 | Editorial Cartography v3 旗舰版</title>"
)

# 5. Update Brand Block
new_html = new_html.replace(
    '<span class="brand-sub">2026 GIS EDITION</span>',
    '<span class="brand-sub">2026 FLAGSHIP v3</span>'
)

# 6. Update Route Tabs in Header
old_route_tabs = '''    <div class="route-tabs" role="tablist" style="flex-wrap:wrap;gap:2px;">
      <button class="route-tab" onclick="switchRoute('r1')" id="tab-r1" title="本州脊梁与千年古道">
        <span class="dot" style="background:#264653"></span>经典一：本州古道 (18D)
      </button>
      <button class="route-tab" onclick="switchRoute('r2')" id="tab-r2" title="山阴神话海岸与濑户内海">
        <span class="dot" style="background:#BC4749"></span>经典二：山阴四国 (17D)
      </button>
      <button class="route-tab" onclick="switchRoute('r3')" id="tab-r3" title="奥羽山脉与北国秘汤">
        <span class="dot" style="background:#386641"></span>经典三：东北秘汤 (16D)
      </button>
      <button class="route-tab active" onclick="switchRoute('r4')" id="tab-r4" title="村上春树：北海道《寻羊冒险记》《舞！舞！舞！》">
        <span class="dot" style="background:#3D5A80"></span>★村上四：北海道寻羊 (16D)
      </button>
      <button class="route-tab" onclick="switchRoute('r5')" id="tab-r5" title="村上春树：阪神与四国《海边的卡夫卡》">
        <span class="dot" style="background:#1B4332"></span>★村上五：四国卡夫卡 (16D)
      </button>
      <button class="route-tab" onclick="switchRoute('r6')" id="tab-r6" title="村上春树：东京《1Q84》与箱根《刺杀骑士团长》">
        <span class="dot" style="background:#6D4C41"></span>★村上六：东京骑士团长 (15D)
      </button>
    </div>'''

new_route_tabs = '''    <div class="route-tabs" role="tablist" style="flex-wrap:wrap;gap:2px;">
      <button class="route-tab active" onclick="switchRoute('r1')" id="tab-r1" title="本州脊梁与千年古道：东京博物馆集群、浮世绘富岳三十六景、信越北陆与关西名刹">
        <span class="dot" style="background:#264653"></span>经典一：东京北斋·本州阿尔卑斯 (18D)
      </button>
      <button class="route-tab" onclick="switchRoute('r2')" id="tab-r2" title="山阴神话海岸与濑户内海">
        <span class="dot" style="background:#BC4749"></span>经典二：山阴四国 (17D)
      </button>
      <button class="route-tab" onclick="switchRoute('r3')" id="tab-r3" title="奥羽山脉与北国秘汤">
        <span class="dot" style="background:#386641"></span>经典三：东北秘汤 (16D)
      </button>
      <button class="route-tab" onclick="switchRoute('r4')" id="tab-r4" title="村上春树：北海道《寻羊冒险记》《舞！舞！舞！》">
        <span class="dot" style="background:#3D5A80"></span>文学四：村上春树·北海道寻羊 (16D)
      </button>
      <button class="route-tab" onclick="switchRoute('r5')" id="tab-r5" title="村上春树：阪神与四国《海边的卡夫卡》">
        <span class="dot" style="background:#1B4332"></span>文学五：村上春树·四国卡夫卡 (16D)
      </button>
      <button class="route-tab" onclick="switchRoute('r6')" id="tab-r6" title="村上春树：东京《1Q84》与箱根《刺杀骑士团长》">
        <span class="dot" style="background:#6D4C41"></span>文学六：村上春树·东京骑士团长 (15D)
      </button>
    </div>'''

new_html = new_html.replace(old_route_tabs, new_route_tabs)

# 7. Update Utility buttons in header (Include Version Matrix, Checklist, Emergency Hotlines, Visa table, Dark Mode)
old_utility_btns = '''    <!-- Utility Buttons -->
    <div class="utility-btns">
      <button class="btn-util" onclick="openVisaModal()">生成送签行程表</button>
      <button class="btn-util" onclick="toggleDarkMode()" id="dark-btn">暗色山岳模式</button>
    </div>'''

new_utility_btns = '''    <!-- Utility Buttons with SVG Icons -->
    <div class="utility-btns">
      <button class="btn-util" onclick="openVersionModal()" title="查看已汇聚的5个导览网页版本矩阵" style="border-color:var(--active-theme);font-weight:700;">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:text-bottom;margin-right:3px;"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>版本导览矩阵
      </button>
      <button class="btn-util" onclick="openChecklistModal()" title="行前必备证件、资金、电器与常备药清单">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:text-bottom;margin-right:3px;"><path d="M9 11l3 3L22 4"></path><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>行前备忘
      </button>
      <button class="btn-util" onclick="openHotlinesModal()" title="日本观光厅多语种热线、医疗救援与驻日使领馆">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:text-bottom;margin-right:3px;"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>紧急热线
      </button>
      <button class="btn-util" onclick="openVisaModal()" title="生成日本领事馆标准格式送签滞在予定表">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:text-bottom;margin-right:3px;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>送签行程表
      </button>
      <button class="btn-util" onclick="toggleDarkMode()" id="dark-btn" title="切换和纸明亮 / 暗色山岳深色模式">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:text-bottom;margin-right:3px;"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>暗色山岳模式
      </button>
    </div>'''

new_html = new_html.replace(old_utility_btns, new_utility_btns)

# 8. Update Hero Block initial content to Flagship Route 1
old_hero = '''      <span class="route-tag" id="hero-tag">ROUTE 01 · CENTRAL ALPS & KUMANO KODO</span>
      <h1 class="route-name" id="hero-title">本州脊梁与千年古道：中山道宿场、北陆工艺、纪伊半岛熊野古道纵贯线</h1>
      <p class="route-desc" id="hero-desc">名古屋进 / 大阪关西出 · 串联江户五街道之木曾路、北阿尔卑斯山岳信仰、五箇山合掌聚落与世界遗产熊野古道。</p>'''

new_hero = '''      <span class="route-tag" id="hero-tag">ROUTE 01 · TOKYO CULTURE, HOKUSAI UKIYO-E, CENTRAL ALPS & HOKURIKU CRAFTS</span>
      <h1 class="route-name" id="hero-title">本州脊梁与千年古道：东京博物馆集群、浮世绘《富岳三十六景》、信越北陆加贺物语与关西名刹纵贯线</h1>
      <p class="route-desc" id="hero-desc">东京(HND/NRT)进 / 大阪关西(KIX)出 · 溯源浮世绘大师葛饰北斋《富岳三十六景》灵感线，串联东京国立博物馆与墨田北斋馆、信州小布施晚年肉笔画圣地、国宝松本城天守、阿尔卑斯上高地、五箇山合掌造、加贺百万石工艺与关西千年名刹。</p>'''

new_html = new_html.replace(old_hero, new_hero)

# 9. Update Map Overlay Top: Add Positron and Carto Key Setting Button
old_map_overlay = '''        <div class="map-chip">
          <span>底图引擎切换（免Key双源容灾）：</span>
          <select class="tile-select" id="tile-selector" onchange="switchBaseTile(this.value)">
            <option value="osm">OpenStreetMap 全球开源底图</option>
            <option value="carto">CARTO 高清人文矢量底图 (推荐)</option>
            <option value="gsi">日本国土地理院 (GSI) 官方标准图</option>
            <option value="gsi_pale">日本国土地理院 (GSI) 淡彩地形图</option>
          </select>
        </div>
        <div class="map-chip">
          <button class="btn-util" style="padding:0.2rem 0.5rem;font-size:0.72rem;" onclick="resetMapBounds()">全览当前路线轨迹</button>
        </div>'''

new_map_overlay = '''        <div class="map-chip">
          <span>底图引擎：</span>
          <select class="tile-select" id="tile-selector" onchange="switchBaseTile(this.value)">
            <option value="carto" selected>CARTO 高清人文图 (Voyager · 内置密钥)</option>
            <option value="carto_positron">CARTO 极简浅灰图 (Positron · 高对比度)</option>
            <option value="gsi">日本国土地理院 (GSI) 官方标准图</option>
            <option value="gsi_pale">日本国土地理院 (GSI) 淡彩地形图</option>
            <option value="osm">OpenStreetMap 全球开源底图 (免Key容灾)</option>
          </select>
          <button class="btn-util" style="padding:0.18rem 0.45rem;font-size:0.7rem;margin-left:4px;" onclick="openCartoKeyModal()" title="自定义底图API Key配置">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;"><circle cx="7.5" cy="15.5" r="5.5"></circle><path d="m21 2-9.6 9.6"></path><path d="m15.5 7.5 3 3L22 7l-3-3"></path></svg> 密钥
          </button>
        </div>
        <div class="map-chip">
          <button class="btn-util" style="padding:0.2rem 0.5rem;font-size:0.72rem;" onclick="resetMapBounds()">全览路线轨迹</button>
        </div>'''

new_html = new_html.replace(old_map_overlay, new_map_overlay)

# 10. Update Panel 3 (Visa & Traffic Rules) with 2026 Visit Japan Web & Driving Rules
old_panel_visa = '''    <!-- PANEL 3: VISA & TRAFFIC RULES -->
    <div id="panel-visa" style="display:none;">
      <div class="sandbox-box">
        <h3 style="font-family:var(--font-serif);margin-bottom:0.65rem;">一、15–20 日行程签证关键预警（防逾期滞留）</h3>
        <p style="font-size:0.84rem;color:var(--ink-secondary);margin-bottom:0.85rem;">
          中国大陆赴日单次旅游电子签（eVISA）默认常见停留期为 <strong>15 天</strong>。若您的行程为 <strong>16 至 20 天</strong>，送签时必须明确向指定代办旅行社要求申请 <strong>30 天停留期的单次签证</strong>，或直接办理 <strong>三年/五年多次往返签证</strong>（单次最长可停留 30 天或 90 天）。
        </p>
        <div style="background:var(--bg-subtle);padding:0.75rem;border-radius:6px;font-size:0.8rem;margin-bottom:1rem;">
          <strong>eVISA 入境铁律：</strong> 值机与入境审查时，必须在联网状态下打开手机浏览器实时展示带动态倒计时的官方 <code>Visa Issuance Notice</code> 页面，<strong>任何截屏、离线 PDF 或纸质打印件均无效</strong>。
        </div>

        <h3 style="font-family:var(--font-serif);margin-bottom:0.65rem;">二、日本自驾法规红线（2025.10 外免切替新政后）</h3>
        <p style="font-size:0.84rem;color:var(--ink-secondary);margin-bottom:0.75rem;">
          日本仅承认基于 <strong>《1949 年日内瓦道路交通公约》</strong> 签发的纸质国际驾照（IDP）原件（或台湾/瑞士/德国等法定日文译本）。
        </p>
        <ul style="font-size:0.82rem;color:var(--ink-secondary);padding-left:1.2rem;line-height:1.75;">
          <li><strong>中国大陆驾照不可自驾：</strong> 大陆驾照配公证件、翻译件或网络平台所谓“国际驾照认证件（KIDA/IDL）”在日本均属无证驾驶，正规车行一律拒租。</li>
          <li><strong>外免切替已对游客关闭：</strong> 自 2025 年 10 月 1 日起，外国驾照换领日本驾照必须提交日本《住民票》，短期旅游签证已无法换证。</li>
          <li><strong>合规自驾替代方案：</strong> 若无港澳/海外驾照+1949 IDP，请直接将顶部开关切回 <strong>“模式A: 公共交通+eBike”</strong>，本系统已为您配齐全部地方巴士、行李托运与观光案内所电助力单车接驳方案。</li>
        </ul>
      </div>
    </div>'''

new_panel_visa = '''    <!-- PANEL 3: VISA & TRAFFIC RULES -->
    <div id="panel-visa" style="display:none;">
      <div class="sandbox-box">
        <h3 style="font-family:var(--font-serif);margin-bottom:0.65rem;border-left:3px solid var(--active-theme);padding-left:0.5rem;">一、15–20 日行程签证关键预警与 2026 入境新规</h3>
        <p style="font-size:0.84rem;color:var(--ink-secondary);margin-bottom:0.75rem;">
          中国大陆赴日单次旅游电子签（eVISA）常规签发停留期仅为 <strong>15 天</strong>。若选择本导览系统的 <strong>16 至 20 天</strong> 深度大环线，送签时务必向指定代办机构申请 <strong>30 天单次签证</strong>（须提供完整覆盖日期的机票预订单与日文《滞在予定表》），或申请 <strong>三年/五年多次签证</strong>（单次分别允许停留 30 天 / 90 天）。
        </p>
        <div style="background:var(--bg-subtle);padding:0.75rem;border-radius:6px;font-size:0.8rem;margin-bottom:0.9rem;border-left:3px solid #BC4749;">
          <strong>eVISA 在线验真准则：</strong> 在国内机场值机与抵达日本入境审查时，<strong>必须在手机联网环境下登录官方系统展示带有动态防伪倒计时的 Visa Issuance Notice 页面</strong>。任何截屏图片、离线 PDF 或非官方打印件均会被拒绝值机。
        </div>
        <div style="background:var(--bg-subtle);padding:0.75rem;border-radius:6px;font-size:0.8rem;margin-bottom:1rem;border-left:3px solid var(--active-theme);">
          <strong>Visit Japan Web (VJW) 统一申报二维码：</strong> 2026 年起入境审查（外国人入国记录）与海关申报（携带品申告）已合并为<strong>单一二次元代码 (QR Code)</strong>。请于起飞前至少 6 小时在 VJW 官网填妥申报，截屏保存单一 QR 码即可在羽田、成田、关西、中部等国际机场电子闸机秒速通关。
        </div>

        <h3 style="font-family:var(--font-serif);margin-bottom:0.65rem;border-left:3px solid #BC4749;padding-left:0.5rem;">二、日本自驾法规红线与导航检索核心机制</h3>
        <p style="font-size:0.84rem;color:var(--ink-secondary);margin-bottom:0.75rem;">
          日本道路交通法严格遵循 <strong>《1949 年日内瓦道路交通公约》</strong>，对驾驶资格审查极为严苛：
        </p>
        <ul style="font-size:0.82rem;color:var(--ink-secondary);padding-left:1.2rem;line-height:1.75;margin-bottom:0.85rem;">
          <li><strong>中国大陆驾照法律地位：</strong> 中国大陆非日内瓦公约缔约方，大陆驾照及其公证件、翻译件、国内平台自制的所谓“国际驾照认证件”在全日本<strong>均不具备任何法律效力</strong>，持此类证件租车属违法驾驶，触犯日本《道路交通法》第64条（最高可处3年以下徒刑或50万日元罚金并直接遣返驱逐出境）。</li>
          <li><strong>合法自驾唯一途径：</strong> 驾驶员必须出示<strong>香港/澳门/美国/加拿大/英国/澳洲等公约国正式驾照 + 1949 年格式正本纸质 IDP</strong>（或台湾驾照+JAF官方日文译本）。</li>
          <li><strong>车载 GPS 专用检索工具：</strong> 本系统每日节点均标注了高精度的 <strong>MapCode (8–10位地标编码)</strong> 及目的地 <strong>固定电话号码 (TEL)</strong>。日本原厂车载中控均内置 Denso/Panasonic 导航系统，直接输入 MapCode 或 TEL 是最准确且无需拼写日文地名的检索方式。</li>
          <li><strong>公共交通方案全覆盖：</strong> 无合法 IDP 的旅行者请直接使用 <strong>“模式A: 公共交通+eBike”</strong>。全线已精准匹配新干线、特急雷鸟/信浓/飞驒号、地方长途观光巴士及车站电助力单车（Docomo Bike Share / Hello Cycling）无缝衔接。</li>
        </ul>
      </div>
    </div>'''

new_html = new_html.replace(old_panel_visa, new_panel_visa)

# 11. CSS additions for Version Matrix Modal, Checklist Modal, Hotlines, and Badges
css_additions = '''
  /* Version Matrix & Utility Modals */
  .version-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin: 1rem 0;
  }
  .version-item {
    background: var(--bg-paper);
    border: 1px solid var(--border-line);
    border-radius: 6px;
    padding: 0.85rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.85rem;
    transition: all 0.2s ease;
  }
  .version-item:hover {
    border-color: var(--active-theme);
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .version-item.current {
    border-color: var(--active-theme);
    background: var(--bg-card);
    box-shadow: 0 0 0 1px var(--active-theme);
  }
  .v-title-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
  }
  .v-badge {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.12rem 0.45rem;
    border-radius: 3px;
    background: var(--active-theme);
    color: #fff;
    white-space: nowrap;
  }
  .v-badge.badge-outline {
    background: transparent;
    border: 1px solid var(--border-line);
    color: var(--ink-secondary);
  }
  .v-badge.badge-active {
    background: #2A9D8F;
    color: #fff;
  }
  .v-desc {
    font-size: 0.78rem;
    color: var(--ink-secondary);
    line-height: 1.45;
  }
  .v-btn-go {
    border: 1px solid var(--border-line);
    background: var(--bg-card);
    color: var(--ink-primary);
    padding: 0.35rem 0.65rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    text-decoration: none;
    white-space: nowrap;
    transition: all 0.15s;
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
  }
  .v-btn-go:hover {
    background: var(--active-theme);
    color: #fff;
    border-color: var(--active-theme);
  }
  .checklist-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-top: 0.75rem;
  }
  @media (max-width: 600px) {
    .checklist-grid { grid-template-columns: 1fr; }
  }
  .checklist-card {
    background: var(--bg-subtle);
    border: 1px solid var(--border-line);
    border-radius: 6px;
    padding: 0.75rem;
  }
  .checklist-card h4 {
    font-size: 0.82rem;
    margin-bottom: 0.4rem;
    color: var(--ink-primary);
    display: flex;
    align-items: center;
    gap: 0.35rem;
  }
  .checklist-card ul {
    list-style: none;
    padding: 0;
    font-size: 0.76rem;
    color: var(--ink-secondary);
    line-height: 1.6;
  }
  .checklist-card ul li {
    position: relative;
    padding-left: 1rem;
    margin-bottom: 0.2rem;
  }
  .checklist-card ul li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: var(--active-theme);
    font-weight: bold;
  }
  .hotline-card {
    background: var(--bg-card);
    border: 1px solid var(--border-line);
    border-radius: 6px;
    padding: 0.85rem;
    margin-bottom: 0.65rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .hotline-num {
    font-family: var(--font-mono);
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--active-theme);
  }
'''

new_html = new_html.replace('  /* Custom Map Marker Styling */', css_additions + '\n  /* Custom Map Marker Styling */')

# 12. Update Script Section: TILE_SOURCES, Key modal, and new modals
old_script_start = '''let markersArray = [];
let hasConfirmedIDP = false;

const TILE_SOURCES = {
  carto: {
    url: "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png?key=cb1_4jug_1_dbb7506275049777c6a92fee",
    attr: "&copy; OpenStreetMap contributors &copy; CARTO"
  },
  gsi: {
    url: "https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png",
    attr: "&copy; 国土地理院 (GSI Japan Standard Map)"
  },
  gsi_pale: {
    url: "https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png",
    attr: "&copy; 国土地理院 (GSI Japan Pale Topo)"
  },
  osm: {
    url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    attr: "&copy; OpenStreetMap contributors"
  }
};'''

new_script_start = '''let markersArray = [];
let hasConfirmedIDP = false;
let currentCartoKey = "cb1_4jug_1_dbb7506275049777c6a92fee";

function getTileSources(key) {
  const kParam = key ? `?key=${key}` : "";
  return {
    carto: {
      url: `https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png${kParam}`,
      attr: "&copy; OpenStreetMap contributors &copy; CARTO"
    },
    carto_positron: {
      url: `https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png${kParam}`,
      attr: "&copy; OpenStreetMap contributors &copy; CARTO"
    },
    gsi: {
      url: "https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png",
      attr: "&copy; 国土地理院 (GSI Japan Standard Map)"
    },
    gsi_pale: {
      url: "https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png",
      attr: "&copy; 国土地理院 (GSI Japan Pale Topo)"
    },
    osm: {
      url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
      attr: "&copy; OpenStreetMap contributors"
    }
  };
}

let TILE_SOURCES = getTileSources(currentCartoKey);'''

new_html = new_html.replace(old_script_start, new_script_start)

# 13. Update initMap to load CARTO Voyager by default
old_init_map = '''function initMap() {
  mapInstance = L.map("map-canvas", {
    center: [35.6, 136.8],
    zoom: 7,
    zoomControl: true
  });

  switchBaseTile("osm");
  renderRouteAll();
}'''

new_init_map = '''function initMap() {
  mapInstance = L.map("map-canvas", {
    center: [35.7, 138.2],
    zoom: 7,
    zoomControl: true
  });

  // Default to CARTO Voyager with built-in API Key, fallback to OSM if unavailable
  switchBaseTile("carto");
  renderRouteAll();
}'''

new_html = new_html.replace(old_init_map, new_init_map)

# 14. Ensure default currentRouteKey is 'r1'
new_html = new_html.replace('let currentRouteKey = "r4";', 'let currentRouteKey = "r1";')
new_html = new_html.replace('let currentRouteKey = "r1";', 'let currentRouteKey = "r1";') # idempotence

# 15. In popup marker, replace (★${node.tabelog}) with clean badge without emoji
old_popup_meta = '<div style="font-size:11px;background:#F4F1EA;padding:4px 6px;border-radius:4px;">\n          <strong>美食：</strong>${node.food} (★${node.tabelog})\n        </div>'
new_popup_meta = '<div style="font-size:11px;background:#F4F1EA;padding:4px 6px;border-radius:4px;">\n          <strong>风味推荐：</strong>${node.food} <span style="color:#C88A32;font-weight:700;">Tabelog ${node.tabelog}</span>\n        </div>'
new_html = new_html.replace(old_popup_meta, new_popup_meta)

# 16. Add helper functions for Version Matrix, Checklist, Hotlines, and Carto Key
extra_js_functions = '''
// ============================================================================
// 6. VERSION MATRIX & PRACTICAL TOOLKIT MODALS
// ============================================================================
function openVersionModal() {
  const modal = document.getElementById("modal-backdrop");
  const content = document.getElementById("modal-content");
  content.innerHTML = `
    <h3 class="modal-title">日本深度自助旅行导览系统 · 版本导览矩阵 (Version Matrix)</h3>
    <p style="font-size:0.82rem;color:var(--ink-secondary);margin-bottom:0.85rem;">
      本项目经多轮迭代已形成 5 套各具特色的可视化导览系统。您可以根据需要随时切换至任意历史版本或探索不同设计架构：
    </p>
    <div class="version-list">
      <div class="version-item current">
        <div>
          <div class="v-title-row">
            <span class="v-badge badge-active">当前版本 · v3</span>
            <strong style="font-size:0.92rem;">v3.html (旗舰终极集大成版)</strong>
          </div>
          <div class="v-desc">
            以 Argon-v2 为主体，深度吸收 v1 路线A经典文化（东京博物馆集群、浮世绘富岳三十六景溯源、信州小布施北斋晚年绝笔、松本城、五箇山合掌造等），配置 D3 实时高程探针、免Key/内置Key多源底图热切换、2026年出入境单一QR码与自驾合规预警。
          </div>
        </div>
        <div>
          <span style="font-size:0.75rem;color:#2A9D8F;font-weight:700;white-space:nowrap;">正在浏览</span>
        </div>
      </div>

      <div class="version-item">
        <div>
          <div class="v-title-row">
            <span class="v-badge">v2.html</span>
            <strong style="font-size:0.92rem;">v2.html (全景融合与抽屉规划版)</strong>
          </div>
          <div class="v-desc">
            以 index.html 为基础重构，集成底图热切换选择器、侧边抽屉式日程导览、动态预算沙盒与全景路线地图。
          </div>
        </div>
        <div>
          <a class="v-btn-go" href="v2.html">进入此版本 &rarr;</a>
        </div>
      </div>

      <div class="version-item">
        <div>
          <div class="v-title-row">
            <span class="v-badge">Argon v2</span>
            <strong style="font-size:0.92rem;">japan_deep_travel_interactive_guide_argon-v2.html (文学深潜与黄金分屏版)</strong>
          </div>
          <div class="v-desc">
            43%/57% 黄金分割双栏排版、D3.js 高程剖面探针联动、暗黑山岳夜景模式、3条经典地理文化线 + 3条村上春树文学寻踪线。
          </div>
        </div>
        <div>
          <a class="v-btn-go" href="japan_deep_travel_interactive_guide_argon-v2.html">进入此版本 &rarr;</a>
        </div>
      </div>

      <div class="version-item">
        <div>
          <div class="v-title-row">
            <span class="v-badge badge-outline">Argon v1</span>
            <strong style="font-size:0.92rem;">japan_deep_travel_interactive_guide_argon.html (探索走廊与文学路线版)</strong>
          </div>
          <div class="v-desc">
            首创融入村上春树文学地图（北海道寻羊、四国卡夫卡、东京骑士团长）与日本三大经典古道。
          </div>
        </div>
        <div>
          <a class="v-btn-go" href="japan_deep_travel_interactive_guide_argon.html">进入此版本 &rarr;</a>
        </div>
      </div>

      <div class="version-item">
        <div>
          <div class="v-title-row">
            <span class="v-badge badge-outline">v1 经典版</span>
            <strong style="font-size:0.92rem;">index.html (原生经典关东关西与本州导览)</strong>
          </div>
          <div class="v-desc">
            经典原生 Leaflet 架构，包含东京、京都、小布施葛饰北斋、兼六园等详尽人文历史解读与高分食宿指南。
          </div>
        </div>
        <div>
          <a class="v-btn-go" href="index.html">进入此版本 &rarr;</a>
        </div>
      </div>
    </div>
    <div style="display:flex;justify-content:flex-end;margin-top:0.85rem;">
      <button class="btn-util" style="background:var(--active-theme);color:#fff;" onclick="closeModal()">关闭</button>
    </div>
  `;
  modal.classList.add("open");
}

function openChecklistModal() {
  const modal = document.getElementById("modal-backdrop");
  const content = document.getElementById("modal-content");
  content.innerHTML = `
    <h3 class="modal-title">日本 15–20 日深度自由行 · 行前备忘与装备核对清单</h3>
    <div class="checklist-grid">
      <div class="checklist-card">
        <h4>证件与通关 (必检)</h4>
        <ul>
          <li>护照原件（有效期 6 个月以上，留有空白签注页）</li>
          <li>日本电子签证 (eVISA) 联网验证页（登机前动态验证）</li>
          <li>Visit Japan Web (VJW) 单一 QR 码（通关截屏备用）</li>
          <li>往返机票行程单打印件、首晚/全程酒店预订单</li>
          <li>合规国际驾照 IDP 原件（若租车自驾，大陆驾照无效）</li>
        </ul>
      </div>

      <div class="checklist-card">
        <h4>支付、通信与乘车</h4>
        <ul>
          <li>Apple Wallet 预先绑定或添加电子 Suica / ICOCA</li>
          <li>现金储备：准备 20,000–30,000 日元纸币与硬币（小镇投币拉面机、神社纳经、投币寄存箱）</li>
          <li>双币/多币种信用卡（Visa / Mastercard / JCB），开通境外无密支付</li>
          <li>日本当地 Docomo/SoftBank 4G/5G eSIM 或随身 WiFi</li>
        </ul>
      </div>

      <div class="checklist-card">
        <h4>电器、电压与穿戴</h4>
        <ul>
          <li>日本电压为 100V 60Hz/50Hz，双脚扁平插头通用无需转换器</li>
          <li>三脚接地插头（如部分笔记本电脑）须自备三转二转换头</li>
          <li>移动电源（须随身携带，严禁托运，额定能量≤100Wh）</li>
          <li>上高地/中山道徒步舒适防滑步行鞋、轻量防风防水冲锋衣</li>
        </ul>
      </div>

      <div class="checklist-card">
        <h4>健康与应急随行</h4>
        <ul>
          <li>个人常备药品（止泻药、感冒药、止痛药、防晕车药、创口贴）</li>
          <li>温泉礼仪需知：大面积纹身需使用肤色防水胶贴遮盖</li>
          <li>小型垃圾袋：日本街头极少设公用垃圾桶，须随身带回酒店分类</li>
          <li>日本观光厅多语种热线与驻日使馆领保电话随身备存</li>
        </ul>
      </div>
    </div>
    <div style="display:flex;justify-content:flex-end;margin-top:1rem;">
      <button class="btn-util" style="background:var(--active-theme);color:#fff;" onclick="closeModal()">我已确认备齐</button>
    </div>
  `;
  modal.classList.add("open");
}

function openHotlinesModal() {
  const modal = document.getElementById("modal-backdrop");
  const content = document.getElementById("modal-content");
  content.innerHTML = `
    <h3 class="modal-title">在日紧急求助、医疗支援与领事保护通讯录</h3>
    <p style="font-size:0.82rem;color:var(--ink-secondary);margin-bottom:0.85rem;">
      遇到突发伤病、自然灾害或治安事故时，可通过以下全天候官方专线获取即时支持：
    </p>

    <div class="hotline-card">
      <div>
        <strong style="font-size:0.88rem;">日本观光厅 24小时多语种访日热线 (Japan Visitor Hotline)</strong>
        <p style="font-size:0.76rem;color:var(--ink-secondary);margin-top:2px;">
          官方全天候提供中文、英文、韩文服务，覆盖意外事故、灾害通报与医疗指引。
        </p>
      </div>
      <div class="hotline-num">050-3816-2720</div>
    </div>

    <div class="hotline-card">
      <div>
        <strong style="font-size:0.88rem;">紧急报警 (警察署 Police)</strong>
        <p style="font-size:0.76rem;color:var(--ink-secondary);margin-top:2px;">
          遭遇盗窃、交通事故、人身侵害时直接拨打（无需加拨区号，公用电话按红色紧急按钮免费拨打）。
        </p>
      </div>
      <div class="hotline-num">110</div>
    </div>

    <div class="hotline-card">
      <div>
        <strong style="font-size:0.88rem;">急救送医与火警 (Ambulance / Fire)</strong>
        <p style="font-size:0.76rem;color:var(--ink-secondary);margin-top:2px;">
          突发急病、需要救护车救援或火灾事故时呼叫。
        </p>
      </div>
      <div class="hotline-num">119</div>
    </div>

    <div class="hotline-card">
      <div>
        <strong style="font-size:0.88rem;">中国外交部全球领事保护与服务应急热线</strong>
        <p style="font-size:0.76rem;color:var(--ink-secondary);margin-top:2px;">
          海外中国公民遭遇重大变故时 24 小时全球直拨求助。
        </p>
      </div>
      <div class="hotline-num">+86-10-12308</div>
    </div>

    <div class="hotline-card">
      <div>
        <strong style="font-size:0.88rem;">中国驻日本大使馆领事保护与协助电话</strong>
        <p style="font-size:0.76rem;color:var(--ink-secondary);margin-top:2px;">
          驻东京大使馆应急专线（非紧急签证业务咨询请勿拨打）。
        </p>
      </div>
      <div class="hotline-num">03-6450-2195</div>
    </div>

    <div style="display:flex;justify-content:flex-end;margin-top:0.85rem;">
      <button class="btn-util" style="background:var(--active-theme);color:#fff;" onclick="closeModal()">关闭</button>
    </div>
  `;
  modal.classList.add("open");
}

function openCartoKeyModal() {
  const modal = document.getElementById("modal-backdrop");
  const content = document.getElementById("modal-content");
  content.innerHTML = `
    <h3 class="modal-title">CARTO 高清人文矢量底图 API Key 设置</h3>
    <p style="font-size:0.82rem;color:var(--ink-secondary);margin-bottom:0.75rem;">
      系统已为您预置合法有效的 CARTO 高清底图密钥。若您有自备的 CARTO API Key，亦可在此输入更新：
    </p>
    <div style="margin-bottom:1rem;">
      <label style="display:block;font-size:0.78rem;font-weight:600;margin-bottom:0.35rem;">当前使用的 API Key：</label>
      <input type="text" id="custom-carto-key-input" value="${currentCartoKey}" 
        style="width:100%;padding:0.45rem 0.65rem;font-family:var(--font-mono);font-size:0.82rem;border:1px solid var(--border-line);border-radius:4px;background:var(--bg-paper);color:var(--ink-primary);">
    </div>
    <div style="font-size:0.76rem;color:var(--ink-secondary);background:var(--bg-subtle);padding:0.65rem;border-radius:4px;margin-bottom:1rem;">
      <strong>容灾保障机制：</strong> 若外部网络无法访问 CARTO 瓦片服务器，系统将无感降级至日本国土地理院 (GSI) 官方地图或 OpenStreetMap 全球开源瓦片。
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <button class="btn-util" onclick="resetDefaultCartoKey()">恢复系统预置 Key</button>
      <div style="display:flex;gap:0.5rem;">
        <button class="btn-util" onclick="closeModal()">取消</button>
        <button class="btn-util" style="background:var(--active-theme);color:#fff;" onclick="saveCustomCartoKey()">保存并刷新底图</button>
      </div>
    </div>
  `;
  modal.classList.add("open");
}

function resetDefaultCartoKey() {
  document.getElementById("custom-carto-key-input").value = "cb1_4jug_1_dbb7506275049777c6a92fee";
}

function saveCustomCartoKey() {
  const inputVal = document.getElementById("custom-carto-key-input").value.trim();
  currentCartoKey = inputVal;
  TILE_SOURCES = getTileSources(currentCartoKey);
  const currentSelectVal = document.getElementById("tile-selector").value;
  switchBaseTile(currentSelectVal);
  closeModal();
}
'''

new_html = new_html.replace('function openVisaModal() {', extra_js_functions + '\nfunction openVisaModal() {')

# 17. Write out v3.html
with open(OUTPUT_V3_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print("v3.html generated successfully! File size:", os.path.getsize(OUTPUT_V3_PATH))
