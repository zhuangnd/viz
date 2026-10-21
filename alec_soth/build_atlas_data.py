#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build comprehensive geospatial & temporal dataset (atlas-data.json) and updated photos.json
for Alec Soth's 11 photography projects, including full photobook plate supplementation
for 'Sleeping by the Mississippi' and 'Niagara'.
"""

import json
import math
import re
from pathlib import Path

BASE_DIR = Path("/Users/zhuangnd/Documents/my_projects/viz/alec_soth")

# ==============================================================================
# 1. PROJECT METADATA (11 Official Projects on alecsoth.com)
# ==============================================================================
PROJECTS_META = [
    {
        "slug": "looking-for-love",
        "title": "Looking for Love",
        "titleZh": "寻找爱情",
        "yearRange": "1995–1997",
        "pubYear": 2012,
        "publisher": "Kominek Books",
        "color": "#6b705c",
        "routeType": "urban-cluster",
        "routeTitle": "明尼苏达双子城夜生活与单身俱乐部纪行",
        "routeDesc": "1995至1997年间，年轻的 Soth 使用中画幅黑白相机游走于明尼阿波利斯、圣保罗及近郊的酒吧、舞厅、台球室与高中舞会，捕捉中西部男女在社交场合寻找亲密关系的笨拙与渴望。",
        "defaultLocus": {
            "country": "United States",
            "state": "Minnesota",
            "stateCode": "MN",
            "county": "Hennepin County",
            "city": "Minneapolis",
            "landmark": "Downtown Minneapolis Nightlife District",
            "lat": 44.9799,
            "lng": -93.2638
        }
    },
    {
        "slug": "sleeping-by-the-mississippi",
        "title": "Sleeping by the Mississippi",
        "titleZh": "密西西比河畔的沉睡",
        "yearRange": "1999–2002",
        "pubYear": 2004,
        "publisher": "Steidl (2004) / MACK (2017)",
        "color": "#b55d35",
        "routeType": "river-corridor",
        "routeTitle": "密西西比河 2,300 英里顺流南下公路巡礼（明尼苏达 → 路易斯安那）",
        "routeDesc": "自明尼苏达州北部森林与冰封湖泊出发，沿美国「第三海岸」密西西比河顺流南下，纵贯威斯康星、爱荷华、伊利诺伊、密苏里、肯塔基、田纳西、阿肯色、密西西比，直至路易斯安那州威尼斯入海口。完整收录官网原作与实体画册/MIA馆藏全部图版。",
        "defaultLocus": {
            "country": "United States",
            "state": "Minnesota",
            "stateCode": "MN",
            "county": "Winona County",
            "city": "Winona",
            "landmark": "Mississippi River Corridor",
            "lat": 44.0588,
            "lng": -91.6322
        }
    },
    {
        "slug": "dog-days-bogota",
        "title": "Dog Days, Bogotá",
        "titleZh": "波哥大三伏天",
        "yearRange": "2002–2003",
        "pubYear": 2007,
        "publisher": "Steidl",
        "color": "#9c6644",
        "routeType": "urban-cluster",
        "routeTitle": "哥伦比亚波哥大领养等待期的城市漫游",
        "routeDesc": "2003年2月，Soth 与妻子前往哥伦比亚首都波哥大办理领养女儿 Carmen 的手续。在长达两个月的焦虑等待中，他根据女婴生母留下的书信线索，用镜头记录下波哥大老城、公园、动物与街头百态。",
        "defaultLocus": {
            "country": "Colombia",
            "state": "Cundinamarca / Distrito Capital",
            "stateCode": "BOG",
            "county": "Bogotá D.C.",
            "city": "Bogotá",
            "landmark": "La Candelaria & Centro Histórico, Bogotá",
            "lat": 4.5981,
            "lng": -74.0758
        }
    },
    {
        "slug": "niagara",
        "title": "Niagara",
        "titleZh": "尼亚加拉",
        "yearRange": "2004–2005",
        "pubYear": 2006,
        "publisher": "Steidl (2006) / MACK (2018)",
        "color": "#3d6b7d",
        "routeType": "border-corridor",
        "routeTitle": "美加边境尼亚加拉瀑布双城与汽车旅馆走廊（Lundy's Lane ↔ Niagara Falls Blvd）",
        "routeDesc": "横跨加拿大安大略省（Lundy's Lane 汽车旅馆长廊）与美国纽约州（Niagara Falls Blvd 工业衰退带）两侧，以轰鸣的马蹄瀑布与美利坚瀑布为背景，探讨「蜜月之都」廉价浪漫神话背后的激情、心碎与告别。完整收录官网与实体画册图版。",
        "defaultLocus": {
            "country": "Canada",
            "state": "Ontario",
            "stateCode": "ON",
            "county": "Niagara Region",
            "city": "Niagara Falls (ON)",
            "landmark": "Lundy's Lane Motel Strip, Niagara Falls, ON",
            "lat": 43.0886,
            "lng": -79.0965
        }
    },
    {
        "slug": "paris-minnesota",
        "title": "Paris / Minnesota",
        "titleZh": "巴黎 / 明尼苏达",
        "yearRange": "2007",
        "pubYear": 2007,
        "publisher": "Magnum Fashion Magazine",
        "color": "#7f5539",
        "routeType": "transatlantic",
        "routeTitle": "巴黎高级定制时装周与明尼苏达冰封森林的双城蒙太奇",
        "routeDesc": "2007年2月至3月，Soth 受玛格南委托拍摄巴黎时装周（大皇宫 Chanel 秀场、Azzedine Alaïa 工作室、YSL 基金会），随后立即返回冰天雪地的明尼苏达北部小镇（Walker 冰钓节、Akeley 林区），将极尽奢华的时尚名流与粗粝质朴的北方日常并置。",
        "defaultLocus": {
            "country": "France",
            "state": "Île-de-France",
            "stateCode": "IDF",
            "county": "Paris",
            "city": "Paris",
            "landmark": "Grand Palais, Avenue Winston Churchill, Paris",
            "lat": 48.8661,
            "lng": 2.3125
        }
    },
    {
        "slug": "last-days-of-w",
        "title": "The Last Days of W.",
        "titleZh": "小布什时代的最后日子",
        "yearRange": "2001–2008",
        "pubYear": 2008,
        "publisher": "Little Brown Mushroom",
        "color": "#8c4a3e",
        "routeType": "national-network",
        "routeTitle": "2001–2008 横跨全美 11 州的时代挽歌",
        "routeDesc": "在 2008 年美国大选前夕编纂出版，汇集小布什执政八年间 Soth 从阿拉斯加诺姆、密歇根底特律、加州圣迭戈到德州圣安东尼奥的纪实创作，折射后 9·11 战争阴影与次贷危机前夜的美国社会。",
        "defaultLocus": {
            "country": "United States",
            "state": "Minnesota",
            "stateCode": "MN",
            "county": "Rice County",
            "city": "Northfield",
            "landmark": "Northfield, MN",
            "lat": 44.4583,
            "lng": -93.1616
        }
    },
    {
        "slug": "broken-manual",
        "title": "Broken Manual",
        "titleZh": "破碎指南",
        "yearRange": "2006–2010",
        "pubYear": 2010,
        "publisher": "Steidl",
        "color": "#52684f",
        "routeType": "national-network",
        "routeTitle": "北美荒野隐士、沙漠洞穴与避世木屋寻访线",
        "routeDesc": "2006至2010年间，Soth 与作家 Lester B. Morrison 深入阿巴拉契亚山脉、蒙大拿林区、犹他红岩峡谷与阿拉巴马密林，寻找逃离现代文明的隐修士、生存主义者与荒野独居者。",
        "defaultLocus": {
            "country": "United States",
            "state": "Utah",
            "stateCode": "UT",
            "county": "San Juan County",
            "city": "Canyonlands Region",
            "landmark": "Colorado Plateau Wilderness",
            "lat": 38.3269,
            "lng": -109.8783
        }
    },
    {
        "slug": "songbook",
        "title": "Songbook",
        "titleZh": "歌本",
        "yearRange": "2012–2014",
        "pubYear": 2015,
        "publisher": "MACK",
        "color": "#4a5d80",
        "routeType": "national-network",
        "routeTitle": "《LBM Dispatch》全美七州社群生活采风走廊",
        "routeDesc": "2012至2014年，Soth 与诗人 Brad Zellar 化身为虚构地方小报《LBM Dispatch》的社区记者，使用刺眼的机顶闪光灯与黑白胶片穿越俄亥俄、纽约上州、密歇根、科罗拉多、德克萨斯、佐治亚与加州硅谷。",
        "defaultLocus": {
            "country": "United States",
            "state": "Ohio",
            "stateCode": "OH",
            "county": "Cuyahoga County",
            "city": "Cleveland",
            "landmark": "Cleveland, OH",
            "lat": 41.4993,
            "lng": -81.6944
        }
    },
    {
        "slug": "i-know-how-furiously-your-heart-is-beating",
        "title": "I Know How Furiously Your Heart Is Beating",
        "titleZh": "我知你心跳动何其剧烈",
        "yearRange": "2017–2018",
        "pubYear": 2019,
        "publisher": "MACK",
        "color": "#7b5283",
        "routeType": "global-network",
        "routeTitle": "横跨北美与欧洲 14 城的私密室内肖像巡礼",
        "routeDesc": "经历一年自我反思后，Soth 放弃宏大公路叙事，走进全球陌生人的私人房间（从旧金山湾区、新奥尔良、纽约到柏林、华沙、敖德萨、布加勒斯特、图卢兹与伦敦），在自然窗光下凝视生命的脆弱与律动。",
        "defaultLocus": {
            "country": "United States",
            "state": "Minnesota",
            "stateCode": "MN",
            "county": "Hennepin County",
            "city": "Minneapolis",
            "landmark": "Minneapolis, MN",
            "lat": 44.9778,
            "lng": -93.2650
        }
    },
    {
        "slug": "a-pound-of-pictures",
        "title": "A Pound of Pictures",
        "titleZh": "一磅照片",
        "yearRange": "2018–2021",
        "pubYear": 2022,
        "publisher": "MACK",
        "color": "#a8763e",
        "routeType": "national-network",
        "routeTitle": "林肯葬礼列车轨迹与疫情后重返美国公路之旅",
        "routeDesc": "起初计划追寻亚伯拉罕·林肯 1865 年葬礼专列路线，后在疫情期间演变为一场对图像物质性与存在记忆的自由漫游，足迹遍及宾夕法尼亚、伊利诺伊、俄克拉荷马、德克萨斯、田纳西与亚利桑那。",
        "defaultLocus": {
            "country": "United States",
            "state": "Illinois",
            "stateCode": "IL",
            "county": "Sangamon County",
            "city": "Springfield",
            "landmark": "Lincoln's Tomb, Oak Ridge Cemetery, Springfield, IL",
            "lat": 39.8233,
            "lng": -89.6558
        }
    },
    {
        "slug": "advice-for-young-artists",
        "title": "Advice for Young Artists",
        "titleZh": "给青年艺术家的建议",
        "yearRange": "2022–2024",
        "pubYear": 2024,
        "publisher": "MACK",
        "color": "#3d7a68",
        "routeType": "national-network",
        "routeTitle": "全美艺术学院工作室与青春创作现场巡访",
        "routeDesc": "年过五旬的 Soth 走访全美超过 25 所本科艺术院校（明尼阿波利斯 MCAD、加州艺术学院、新奥尔良杜兰大学、马萨诸塞艺术学院等），在乱中有序的画室中重新汲取青年学子的实验精神。",
        "defaultLocus": {
            "country": "United States",
            "state": "Minnesota",
            "stateCode": "MN",
            "county": "Hennepin County",
            "city": "Minneapolis",
            "landmark": "Minneapolis College of Art and Design (MCAD)",
            "lat": 44.9576,
            "lng": -93.2743
        }
    }
]

PROJECT_MAP = {p["slug"]: p for p in PROJECTS_META}

# ==============================================================================
# 2. SUPPLEMENTED BOOK PLATES FOR SLEEPING BY THE MISSISSIPPI, NIAGARA & SONGBOOK
# ==============================================================================
SUPPLEMENTED_PLATES = {
    "sleeping-by-the-mississippi": [
        {
            "title": "Sheila, Leech Lake Indian Reservation, MN, 2002",
            "src": "https://1.api.artsmia.org/800/105031.jpg",
            "year": 2002, "month": 2,
            "sourceType": "book_plate",
            "miaId": "105031"
        },
        {
            "title": "Celebrity Room, Brainerd, MN, 2000",
            "src": "https://1.api.artsmia.org/800/105039.jpg",
            "year": 2000, "month": 6,
            "sourceType": "book_plate",
            "miaId": "105039"
        },
        {
            "title": "Mother and Daughter, Saint Paul, MN, 1999",
            "src": "https://1.api.artsmia.org/800/98614.jpg",
            "year": 1999, "month": 8,
            "sourceType": "book_plate",
            "miaId": "98614"
        },
        {
            "title": "Home, Treasure Island Casino, Red Wing, MN, 2002",
            "src": "https://1.api.artsmia.org/800/105029.jpg",
            "year": 2002, "month": 3,
            "sourceType": "book_plate",
            "miaId": "105029"
        },
        {
            "title": "Green Island, IA, 2002",
            "src": "https://1.api.artsmia.org/800/105028.jpg",
            "year": 2002, "month": 3,
            "sourceType": "book_plate",
            "miaId": "105028"
        },
        {
            "title": "Sacred Heart Hall, Green Island, IA, 2002",
            "src": "https://1.api.artsmia.org/800/105030.jpg",
            "year": 2002, "month": 3,
            "sourceType": "book_plate",
            "miaId": "105030"
        },
        {
            "title": "Green Island (Hospital Bed), IA, 2002",
            "src": "https://1.api.artsmia.org/800/105052.jpg",
            "year": 2002, "month": 3,
            "sourceType": "book_plate",
            "miaId": "105052"
        },
        {
            "title": "Buena Vista, IA, 2002",
            "src": "https://1.api.artsmia.org/800/105057.jpg",
            "year": 2002, "month": 3,
            "sourceType": "book_plate",
            "miaId": "105057"
        },
        {
            "title": "Dallas City, IL, 2002",
            "src": "https://1.api.artsmia.org/800/105026.jpg",
            "year": 2002, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105026"
        },
        {
            "title": "Dallas City, IL (Muscle Figure), 2002",
            "src": "https://1.api.artsmia.org/800/105032.jpg",
            "year": 2002, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105032"
        },
        {
            "title": "Jim, Wax Museum, Hannibal, MO, 2002",
            "src": "https://1.api.artsmia.org/800/105034.jpg",
            "year": 2002, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105034"
        },
        {
            "title": "Saint Genevieve, MO, 2002",
            "src": "https://1.api.artsmia.org/800/105016.jpg",
            "year": 2002, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105016"
        },
        {
            "title": "Immaculate Conception Church, Kaskaskia, IL, 2002",
            "src": "https://1.api.artsmia.org/800/105050.jpg",
            "year": 2002, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105050"
        },
        {
            "title": "Fishermen, Wickliffe, KY, 2002",
            "src": "https://1.api.artsmia.org/800/105042.jpg",
            "year": 2002, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105042"
        },
        {
            "title": "Hickman, KY, 2002",
            "src": "https://1.api.artsmia.org/800/105040.jpg",
            "year": 2002, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105040"
        },
        {
            "title": "Eggleston in His Music Room, Memphis, TN, 2000",
            "src": "https://1.api.artsmia.org/800/105027.jpg",
            "year": 2000, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105027"
        },
        {
            "title": "Sunshine, Memphis, TN, 2000",
            "src": "https://1.api.artsmia.org/800/105053.jpg",
            "year": 2000, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105053"
        },
        {
            "title": "Harbor Marina, Memphis, TN, 2000",
            "src": "https://1.api.artsmia.org/800/105055.jpg",
            "year": 2000, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105055"
        },
        {
            "title": "Memphis, TN, 2000",
            "src": "https://1.api.artsmia.org/800/105041.jpg",
            "year": 2000, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105041"
        },
        {
            "title": "Jessie's Prayer Room, Memphis, TN, 2002",
            "src": "https://1.api.artsmia.org/800/105035.jpg",
            "year": 2002, "month": 4,
            "sourceType": "book_plate",
            "miaId": "105035"
        },
        {
            "title": "Helena, AR, 2002",
            "src": "https://1.api.artsmia.org/800/105017.jpg",
            "year": 2002, "month": 5,
            "sourceType": "book_plate",
            "miaId": "105017"
        },
        {
            "title": "Shotgun Lounge, Greenville, MS, 2002",
            "src": "https://1.api.artsmia.org/800/105036.jpg",
            "year": 2002, "month": 5,
            "sourceType": "book_plate",
            "miaId": "105036"
        },
        {
            "title": "Bible Study Book, Vicksburg, MS, 2002",
            "src": "https://1.api.artsmia.org/800/105045.jpg",
            "year": 2002, "month": 5,
            "sourceType": "book_plate",
            "miaId": "105045"
        },
        {
            "title": "The Reverend and Margaret's Bedroom, Vicksburg, MS, 2002",
            "src": "https://1.api.artsmia.org/800/105059.jpg",
            "year": 2002, "month": 5,
            "sourceType": "book_plate",
            "miaId": "105059"
        },
        {
            "title": "Frankie, Ferriday, LA, 2002",
            "src": "https://1.api.artsmia.org/800/105054.jpg",
            "year": 2002, "month": 5,
            "sourceType": "book_plate",
            "miaId": "105054"
        },
        {
            "title": "Angola, LA, 2002",
            "src": "https://1.api.artsmia.org/800/105025.jpg",
            "year": 2002, "month": 5,
            "sourceType": "book_plate",
            "miaId": "105025"
        },
        {
            "title": "The Farm, Angola State Prison, LA, 2002",
            "src": "https://1.api.artsmia.org/800/105064.jpg",
            "year": 2002, "month": 5,
            "sourceType": "book_plate",
            "miaId": "105064"
        },
        {
            "title": "Patrick, Palm Sunday, Baton Rouge, LA, 2002",
            "src": "https://1.api.artsmia.org/800/105022.jpg",
            "year": 2002, "month": 3,
            "sourceType": "book_plate",
            "miaId": "105022"
        },
        {
            "title": "Baton Rouge, LA, 2002",
            "src": "https://1.api.artsmia.org/800/105062.jpg",
            "year": 2002, "month": 5,
            "sourceType": "book_plate",
            "miaId": "105062"
        },
        {
            "title": "Crystal, Easter, New Orleans, LA, 2002",
            "src": "https://1.api.artsmia.org/800/105038.jpg",
            "year": 2002, "month": 3,
            "sourceType": "book_plate",
            "miaId": "105038"
        },
        {
            "title": "Holt Cemetery, New Orleans, LA, 2002",
            "src": "https://1.api.artsmia.org/800/105044.jpg",
            "year": 2002, "month": 5,
            "sourceType": "book_plate",
            "miaId": "105044"
        },
        {
            "title": "Memorial, Holt Cemetery, New Orleans, LA, 2002",
            "src": "https://1.api.artsmia.org/800/105046.jpg",
            "year": 2002, "month": 5,
            "sourceType": "book_plate",
            "miaId": "105046"
        },
        {
            "title": "Venice, LA, 2002",
            "src": "https://1.api.artsmia.org/800/105023.jpg",
            "year": 2002, "month": 5,
            "sourceType": "book_plate",
            "miaId": "105023"
        }
    ],
    "niagara": [
        {
            "title": "Candlelight Hotel, Niagara Falls, ON, 2004",
            "src": "https://content.magnumphotos.com/wp-content/uploads/2018/09/cortex/nyc53285-teaser-xxl.jpg",
            "year": 2004, "month": 9,
            "sourceType": "book_plate"
        },
        {
            "title": "Christina and Jonathan, Niagara Falls, NY, 2004",
            "src": "https://content.magnumphotos.com/wp-content/uploads/2016/05/cortex/nyc53286-teaser-xxl.jpg",
            "year": 2004, "month": 9,
            "sourceType": "book_plate"
        },
        {
            "title": "Michele and James, Niagara Falls, ON, 2004",
            "src": "https://content.magnumphotos.com/wp-content/uploads/2018/09/cortex/nyc53287-teaser-xxl.jpg",
            "year": 2004, "month": 10,
            "sourceType": "book_plate"
        },
        {
            "title": "Fairway Motor Inn, Lundy's Lane, Niagara Falls, ON, 2005",
            "src": "https://content.magnumphotos.com/wp-content/uploads/2018/09/cortex/nyc53292-teaser-story-big.jpg",
            "year": 2005, "month": 5,
            "sourceType": "book_plate"
        },
        {
            "title": "Balloon, Niagara Falls, ON, 2005",
            "src": "https://content.magnumphotos.com/wp-content/uploads/2018/09/cortex/nyc53302-teaser-story-big.jpg",
            "year": 2005, "month": 6,
            "sourceType": "book_plate"
        },
        {
            "title": "Happiness Inn, Niagara Falls, ON, 2005",
            "src": "https://content.magnumphotos.com/wp-content/uploads/2018/09/cortex/nyc53303-teaser-story-big.jpg",
            "year": 2005, "month": 6,
            "sourceType": "book_plate"
        },
        {
            "title": "Best Western, Clifton Hill, Niagara Falls, ON, 2005",
            "src": "https://content.magnumphotos.com/wp-content/uploads/2018/09/cortex/nyc53306-teaser-xxl.jpg",
            "year": 2005, "month": 7,
            "sourceType": "book_plate"
        },
        {
            "title": "Wedding Dress, Niagara Falls, ON, 2005",
            "src": "https://content.magnumphotos.com/wp-content/uploads/2016/05/cortex/nyc53307-teaser-xxl.jpg",
            "year": 2005, "month": 7,
            "sourceType": "book_plate"
        },
        {
            "title": "Comfort Inn, Niagara Falls, ON, 2005",
            "src": "https://content.magnumphotos.com/wp-content/uploads/2018/10/cortex/nyc53311-teaser-story-big.jpg",
            "year": 2005, "month": 8,
            "sourceType": "book_plate"
        },
        {
            "title": "\"To the love of my life\", Niagara Falls, ON, 2005",
            "src": "https://content.magnumphotos.com/wp-content/uploads/2018/09/cortex/nyc53374-teaser-xxl.jpg",
            "year": 2005, "month": 8,
            "sourceType": "book_plate"
        },
        {
            "title": "\"Well what can I say?\", Niagara Falls, ON, 2005",
            "src": "https://content.magnumphotos.com/wp-content/uploads/2018/09/cortex/nyc53375-teaser-xxl.jpg",
            "year": 2005, "month": 8,
            "sourceType": "book_plate"
        },
        {
            "title": "Falls Manor Resort, Lundy's Lane, Niagara Falls, ON, 2005",
            "src": "https://1.api.artsmia.org/800/100937.jpg",
            "year": 2005, "month": 6,
            "sourceType": "book_plate",
            "miaId": "100937"
        },
        {
            "title": "Bonanza Motel, Lundy's Lane, Niagara Falls, ON, 2005",
            "src": "https://1.api.artsmia.org/800/100938.jpg",
            "year": 2005, "month": 6,
            "sourceType": "book_plate",
            "miaId": "100938"
        }
    ]
}

# ==============================================================================
# 3. HIGH-PRECISION GEOCODING GAZETTEER (Exact Landmarks, Streets, Counties)
# ==============================================================================
# Each entry maps a substring or exact key to:
# (country, state, stateCode, county, city, landmark, lat, lng, precision, notes)
GAZETTEER = [
    # --- SLEEPING BY THE MISSISSIPPI (North -> South along the river) ---
    ("Leech Lake", ("United States", "Minnesota", "MN", "Cass County", "Cass Lake / Walker", "Leech Lake Indian Reservation", 47.2233, -94.4536, "landmark", "密西西比河源头流域李奇湖印第安保留地，距源头艾塔斯卡湖仅数英里。")),
    ("Brainerd", ("United States", "Minnesota", "MN", "Crow Wing County", "Brainerd", "Celebrity Room, Brainerd", 46.3580, -94.2008, "landmark", "明尼苏达州中部上密西西比河畔城镇布雷纳德，科恩兄弟电影《冰血暴》背景地。")),
    ("Little Falls", ("United States", "Minnesota", "MN", "Morrison County", "Little Falls", "Charles Lindbergh State Park & Boyhood Home", 45.9575, -94.3881, "landmark", "传奇飞行员查尔斯·林德伯格童年故居（密西西比河西岸林德伯格州立公园内，夏纱门廊上的行军床）。")),
    ("Polish Palace", ("United States", "Minnesota", "MN", "Hennepin County", "Minneapolis", "Polish Palace Bar, Northeast Minneapolis", 45.0025, -93.2628, "landmark", "明尼阿波利斯东北波兰移民街区老酒吧 Polish Palace。")),
    ("Lenny, Minneapolis", ("United States", "Minnesota", "MN", "Hennepin County", "Minneapolis", "West Bank / Cedar-Riverside, Minneapolis", 44.9686, -93.2464, "city", "明尼阿波利斯密西西比河西岸街区。")),
    ("Saint Paul, MN, 1999", ("United States", "Minnesota", "MN", "Ramsey County", "Saint Paul", "Harriet Island / West Side, Saint Paul", 44.9381, -93.0955, "city", "明尼苏达首府圣保罗密西西比河岸。")),
    ("Treasure Island Casino", ("United States", "Minnesota", "MN", "Goodhue County", "Red Wing / Welch", "Treasure Island Resort & Casino, Prairie Island", 44.6331, -92.6481, "landmark", "红翼市（Red Wing）上游草原岛印第安社区的星际赌场与河畔居所。")),
    ("Vasa", ("United States", "Minnesota", "MN", "Goodhue County", "Vasa", "Vasa Township, Goodhue County", 44.5041, -92.7238, "landmark", "画册封面经典之作《Charles, Vasa, MN》拍摄地：古德休县瑞典裔小镇瓦萨农舍屋顶，Charles 手持两架自制飞机模型。")),
    ("Peter's Houseboat", ("United States", "Minnesota", "MN", "Winona County", "Winona", "Latsch Island Boathouse Community, Winona", 44.0588, -91.6322, "landmark", "画册开篇首图：威诺纳第 43 号公路大桥下 Latsch Island 百年水上船屋社区。")),
    ("Neil. Winona", ("United States", "Minnesota", "MN", "Winona County", "Winona", "Winona Riverfront, MN", 44.0525, -91.6393, "city", "Soth 在《A Pound of Pictures》中重返威诺纳密西西比河岸拍摄。")),
    ("Fountain City", ("United States", "Wisconsin", "MN/WI Border (WI)", "Buffalo County", "Fountain City", "Fountain City Public Cemetery, WI", 44.1325, -91.6912, "landmark", "威诺纳对岸威斯康星州喷泉城（Fountain City）俯瞰密西西比河谷的山坡公墓。")),
    ("Green Island (Hospital Bed)", ("United States", "Iowa", "IA", "Jackson County", "Green Island", "Green Island Bottoms, IA", 42.1528, -90.3085, "landmark", "爱荷华州格林岛（Green Island）废弃建筑内孤立的医院病床。")),
    ("Sacred Heart Hall, Green Island", ("United States", "Iowa", "IA", "Jackson County", "Green Island", "Sacred Heart Hall, Green Island", 42.1502, -90.3122, "landmark", "爱荷华州格林岛天主教圣心堂旧址。")),
    ("Green Island, IA", ("United States", "Iowa", "IA", "Jackson County", "Green Island", "Green Island Wildlife Management Area", 42.1551, -90.3045, "city", "爱荷华州杰克逊县密西西比河与马科基塔河交汇湿地格林岛。")),
    ("Cooper. Green Island, Illinois", ("United States", "Iowa", "IA", "Jackson County", "Green Island", "Green Island Riverfront (IA/IL Border)", 42.1575, -90.2995, "city", "密西西比河伊利诺伊与爱荷华交界处格林岛。")),
    ("Buena Vista, IA", ("United States", "Iowa", "IA", "Clayton County", "North Buena Vista", "North Buena Vista River Bluffs, IA", 42.6719, -90.9632, "city", "爱荷华州克莱顿县密西西比河陡峭崖壁小镇 North Buena Vista。")),
    ("Sugar's, Davenport", ("United States", "Iowa", "IA", "Scott County", "Davenport", "West 3rd Street, Downtown Davenport", 41.5218, -90.5795, "landmark", "爱荷华州达文波特市中心，身着黑色连衣裙坐在铺满钞票床垫上的 Sugar。")),
    ("Mother and Daughter", ("United States", "Iowa", "IA", "Scott County", "Davenport", "Centennial Bridge Area, Davenport, IA", 41.5236, -90.5776, "city", "爱荷华州达文波特（Davenport）母女肖像，MIA 馆藏明确标注摄于 Davenport, Iowa。")),
    ("Hotel, Dallas City", ("United States", "Illinois", "IL", "Hancock County", "Dallas City", "Riverside Hotel, Dallas City, IL", 40.6358, -91.1662, "landmark", "伊利诺伊州达拉斯城（Dallas City）密西西比河畔旅馆，荧光绿墙壁前的床铺与电视。")),
    ("Dallas City, IL (Muscle Figure)", ("United States", "Illinois", "IL", "Hancock County", "Dallas City", "Dallas City Riverfront, IL", 40.6341, -91.1688, "city", "伊利诺伊州汉考克县达拉斯城。")),
    ("Dallas City, IL", ("United States", "Illinois", "IL", "Hancock County", "Dallas City", "Dallas City, Hancock County, IL", 40.6372, -91.1635, "city", "伊利诺伊州汉考克县达拉斯城。")),
    ("Hannibal, MO", ("United States", "Missouri", "MO", "Marion County", "Hannibal", "Mark Twain Historic District Wax Museum, Hannibal", 39.7108, -91.3571, "landmark", "马克·吐温故乡密苏里州汉尼拔（Hannibal）老城蜡像馆。")),
    ("Reverend Cecil and Felica", ("United States", "Missouri", "MO", "St. Louis City", "St. Louis", "North St. Louis Riverfront, MO", 38.6531, -90.1978, "city", "密苏里州圣路易斯牧师 Cecil 与 Felicia 的肖像。")),
    ("Reverend Cecil and Felicia", ("United States", "Missouri", "MO", "St. Louis City", "St. Louis", "North St. Louis Riverfront, MO", 38.6531, -90.1978, "city", "密苏里州圣路易斯牧师 Cecil 与 Felicia 的肖像。")),
    ("Saint Genevieve", ("United States", "Missouri", "MO", "Ste. Genevieve County", "Ste. Genevieve", "Ste. Genevieve Historic French Colonial District", 37.9814, -90.0418, "landmark", "密西西比河西岸最古老的法属殖民城镇圣热讷维耶沃。")),
    ("Kaskaskia", ("United States", "Illinois", "IL", "Randolph County", "Kaskaskia", "Church of the Immaculate Conception, Kaskaskia Island", 37.9214, -89.9132, "landmark", "1881年密西西比河改道后位于河西岸的伊利诺伊州飞地卡斯卡斯基亚岛无玷始胎堂。")),
    ("Cape Giirardeau", ("United States", "Missouri", "MO", "Cape Girardeau County", "Cape Girardeau", "Mississippi River Floodwall, Cape Girardeau", 37.3059, -89.5181, "landmark", "密苏里州开普吉拉多河畔防洪墙街区。")),
    ("Cape Girardeau", ("United States", "Missouri", "MO", "Cape Girardeau County", "Cape Girardeau", "Mississippi River Floodwall, Cape Girardeau", 37.3059, -89.5181, "landmark", "密苏里州开普吉拉多河畔防洪墙街区。")),
    ("Fort Jefferson Memorial Cross", ("United States", "Kentucky", "KY", "Ballard County", "Wickliffe", "Fort Jefferson Hill, Confluence of Ohio & Mississippi Rivers", 36.9589, -89.0928, "landmark", "肯塔基州威克利夫（Wickliffe），矗立于俄亥俄河与密西西比河壮阔交汇处高达 95 英尺的巨型白色十字架。")),
    ("Fishermen, Wickliffe", ("United States", "Kentucky", "KY", "Ballard County", "Wickliffe", "Confluence Point Riverbank, Wickliffe, KY", 36.9615, -89.0955, "landmark", "威克利夫两河交汇处岸边垂钓的渔夫。")),
    ("Hickman, KY", ("United States", "Kentucky", "KY", "Fulton County", "Hickman", "Hickman River Bluff, Fulton County, KY", 36.5712, -89.1862, "city", "肯塔基州最西端密西西比河弯道悬崖城镇希克曼。")),
    ("Luxora", ("United States", "Arkansas", "AR", "Mississippi County", "Luxora", "Mississippi River Levee, Luxora, AR", 35.7562, -89.9287, "landmark", "阿肯色州密西西比县卢克索拉河堤荒原。官网原注误作 AK，实为阿肯色州 AR。")),
    ("Johnny Cash's Boyhood Home", ("United States", "Arkansas", "AR", "Mississippi County", "Dyess", "Historic Dyess Colony, Johnny Cash Boyhood Home", 35.5901, -90.2134, "landmark", "阿肯色州戴斯新政农业殖民地（Dyess Colony），传奇乡村歌手 Johnny Cash 童年木屋故居。")),
    ("Johnny Cash's boyhood home", ("United States", "Arkansas", "AR", "Mississippi County", "Dyess", "Historic Dyess Colony, Johnny Cash Boyhood Home", 35.5901, -90.2134, "landmark", "阿肯色州戴斯新政农业殖民地（Dyess Colony），传奇乡村歌手 Johnny Cash 童年木屋故居。")),
    ("Jimmie's Apartment, Memphis", ("United States", "Tennessee", "TN", "Shelby County", "Memphis", "Midtown / Pinch District, Memphis", 35.1522, -90.0489, "landmark", "田纳西州孟菲斯 Jimmie 的公寓，窗外可见密西西比河大桥。")),
    ("Eggleston in His Music Room", ("United States", "Tennessee", "TN", "Shelby County", "Memphis", "Overton Park / Midtown Memphis (William Eggleston Residence)", 35.1388, -89.9922, "landmark", "现代彩色摄影先驱 William Eggleston 在孟菲斯家中音乐室的肖像，向大师致敬之作。")),
    ("Sunshine, Memphis", ("United States", "Tennessee", "TN", "Shelby County", "Memphis", "Lamar Avenue Motel Strip, Memphis", 35.1145, -90.0085, "landmark", "孟菲斯汽车旅馆房间内的经典人体肖像《Sunshine》。")),
    ("Harbor Marina, Memphis", ("United States", "Tennessee", "TN", "Shelby County", "Memphis", "Mud Island Harbor Marina, Memphis", 35.1585, -90.0562, "landmark", "孟菲斯泥岛（Mud Island）密西西比河游艇码头。")),
    ("Jessie's Prayer Room, Memphis", ("United States", "Tennessee", "TN", "Shelby County", "Memphis", "South Memphis, TN", 35.0982, -90.0412, "city", "田纳西州南孟菲斯 Jessie 的祈祷室。")),
    ("Memphis, TN, 2000", ("United States", "Tennessee", "TN", "Shelby County", "Memphis", "Riverside Drive, Memphis, TN", 35.1435, -90.0598, "city", "田纳西州孟菲斯密西西比河岸。")),
    ("Quan Am Monastery. Memphis", ("United States", "Tennessee", "TN", "Shelby County", "Memphis", "Quan Am Monastery, 3500uf, Memphis", 35.0568, -89.9612, "landmark", "孟菲斯观音寺（Quan Am Monastery）巨型白衣观音像。")),
    ("Helena, AR", ("United States", "Arkansas", "AR", "Phillips County", "Helena-West Helena", "Cherry Street Historic District, Helena, AR", 34.5293, -90.5915, "landmark", "阿肯色州三角洲蓝调重镇海伦娜（Helena）密西西比河渡口。")),
    ("Coahoma, Mississippi", ("United States", "Mississippi", "MS", "Coahoma County", "Coahoma", "US Route 61 Blues Highway, Coahoma, MS", 34.2654, -90.5143, "landmark", "密西西比三角洲科ahoma县 61 号蓝调公路旁被藤蔓吞噬的废弃老宅。")),
    ("Shotgun Lounge, Greenville", ("United States", "Mississippi", "MS", "Washington County", "Greenville", "Nelson Street Blues District, Greenville, MS", 33.4101, -91.0618, "landmark", "密西西比州格林维尔传奇蓝调街区 Nelson Street 的 Shotgun Lounge。")),
    ("Bible Study Book, Vicksburg", ("United States", "Mississippi", "MS", "Warren County", "Vicksburg", "Vicksburg Bluffs, MS", 32.3526, -90.8779, "city", "密西西比州维克斯堡圣经研读手记。")),
    ("The Reverend and Margaret's Bedroom, Vicksburg", ("United States", "Mississippi", "MS", "Warren County", "Vicksburg", "Historic Vicksburg, MS", 32.3482, -90.8815, "landmark", "密西西比州维克斯堡牧师与玛格丽特的卧室。")),
    ("Bonnie, Port Gibson", ("United States", "Mississippi", "MS", "Claiborne County", "Port Gibson", "Church Street Historic District, Port Gibson, MS", 31.9607, -90.9839, "landmark", "密西西比州吉布森港（Port Gibson）手捧天使照片的小女孩 Bonnie。")),
    ("Frankie, Ferriday", ("United States", "Louisiana", "LA", "Concordia Parish", "Ferriday", "Ferriday, Concordia Parish, LA", 31.6302, -91.5543, "city", "路易斯安那州康科迪亚堂区费里迪（Jerry Lee Lewis 故乡）。")),
    ("Joshua, Angola State Prison", ("United States", "Louisiana", "LA", "West Feliciana Parish", "Angola", "Louisiana State Penitentiary (Angola)", 30.9658, -91.6025, "landmark", "三面环绕密西西比河的路易斯安那州立安哥拉监狱（前身为蓄奴种植园）。")),
    ("The Farm, Angola State Prison", ("United States", "Louisiana", "LA", "West Feliciana Parish", "Angola", "Angola Prison Farm Fields, Tunica Hills", 30.9712, -91.5942, "landmark", "安哥拉州立监狱劳改农场（绰号「The Farm」）。")),
    ("Angola, LA", ("United States", "Louisiana", "LA", "West Feliciana Parish", "Angola", "Angola Ferry Landing, Mississippi River", 30.9585, -91.6115, "landmark", "路易斯安那州安哥拉密西西比河岸。")),
    ("Patrick, Palm Sunday, Baton Rouge", ("United States", "Louisiana", "LA", "East Baton Rouge Parish", "Baton Rouge", "Downtown Baton Rouge, LA", 30.4515, -91.1871, "landmark", "路易斯安那州首府巴吞鲁日棕枝主日（Palm Sunday），西装革履站在杂草庭院中的 Patrick。")),
    ("Baton Rouge, LA", ("United States", "Louisiana", "LA", "East Baton Rouge Parish", "Baton Rouge", "Mississippi River Levee, Baton Rouge", 30.4455, -91.1912, "city", "路易斯安那州巴吞鲁日河岸。")),
    ("Herman's Bed, Kenner", ("United States", "Louisiana", "LA", "Jefferson Parish", "Kenner", "Rivertown, Kenner, LA", 29.9745, -90.2417, "landmark", "新奥尔良西郊肯纳（Kenner）密西西比河畔 Herman 的床铺。")),
    ("Adelyn, Ash Wednesday, New Orleans", ("United States", "Louisiana", "LA", "Orleans Parish", "New Orleans", "French Quarter / St. Louis Cathedral Area, New Orleans", 29.9574, -90.0629, "landmark", "新奥尔良狂欢节次日圣灰星期三（Ash Wednesday），额头画有灰十字的 Adelyn。")),
    ("Holt Cemetery, New Orleans", ("United States", "Louisiana", "LA", "Orleans Parish", "New Orleans", "Holt Cemetery, 527 City Park Ave, New Orleans", 29.9822, -90.1058, "landmark", "新奥尔良著名的穷人公墓霍尔特墓园（Holt Cemetery），坟冢由家属手工装饰。")),
    ("Memorial, Holt Cemetery", ("United States", "Louisiana", "LA", "Orleans Parish", "New Orleans", "Holt Cemetery, 527 City Park Ave, New Orleans", 29.9831, -90.1045, "landmark", "新奥尔良霍尔特公墓内的手工纪念碑。")),
    ("Crystal, Easter, New Orleans", ("United States", "Louisiana", "LA", "Orleans Parish", "New Orleans", "Tremé / Seventh Ward, New Orleans", 29.9695, -90.0685, "city", "新奥尔良复活节盛装的 Crystal。")),
    ("New Orleans, LA, 2002", ("United States", "Louisiana", "LA", "Orleans Parish", "New Orleans", "Algiers Point / Mississippi River Bend, New Orleans", 29.9511, -90.0545, "city", "新奥尔良密西西比河大回湾。")),
    ("Leyla and Sabine. New Orleans", ("United States", "Louisiana", "LA", "Orleans Parish", "New Orleans", "Bywater / Marigny, New Orleans", 29.9635, -90.0442, "city", "新奥尔良室内双人肖像（《I Know How Furiously...》）。")),
    ("Zibby’s Kitchen. New Orleans", ("United States", "Louisiana", "LA", "Orleans Parish", "New Orleans", "Garden District, New Orleans", 29.9288, -90.0835, "landmark", "新奥尔良花园街区 Zibby 的厨房。")),
    ("Venice, LA", ("United States", "Louisiana", "LA", "Plaquemines Parish", "Venice", "Venice (\"The End of the World\"), Mississippi River Delta", 29.2764, -89.3548, "landmark", "密西西比河公路的绝对终点——路易斯安那州威尼斯（Venice，当地人称「世界尽头」），河流在此注入墨西哥湾。")),

    # --- NIAGARA (US / Canada Border Motels & Landmarks) ---
    ("A-1 Motel", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "A-1 Motel, 7895 Lundy's Lane, Niagara Falls, ON", 43.0865, -79.1182, "landmark", "加拿大安大略省尼亚加拉瀑布城 Lundy's Lane 7895 号 A-1 汽车旅馆。")),
    ("Cadillac Motel", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Cadillac Motel, 5342 Ferry St / Lundy's Lane, Niagara Falls, ON", 43.0894, -79.0842, "landmark", "尼亚加拉瀑布城 Ferry Street 复古霓虹灯汽车旅馆 Cadillac Motel。")),
    ("Flamingo Inn", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Flamingo Motor Inn, 7701 Lundy's Lane, Niagara Falls, ON", 43.0869, -79.1135, "landmark", "Lundy's Lane 7701 号火烈鸟汽车旅馆（代表作《Melissa》拍摄地，身穿婚纱站在停车场的新娘）。")),
    ("Melissa", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Flamingo Motor Inn, 7701 Lundy's Lane, Niagara Falls, ON", 43.0869, -79.1135, "landmark", "代表作《Melissa》：摄于加拿大侧 Lundy's Lane 7701 号 Flamingo Motor Inn 旅馆外。")),
    ("Falls Manor", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Falls Manor Resort, 7104 Lundy's Lane, Niagara Falls, ON", 43.0878, -79.1045, "landmark", "Lundy's Lane 7104 号老牌度假旅馆 Falls Manor。")),
    ("Bonanza Motel", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Bonanza Motel, 6267 Lundy's Lane, Niagara Falls, ON", 43.0888, -79.0942, "landmark", "Lundy's Lane 6267 号 Bonanza 汽车旅馆。")),
    ("Fairway Motor Inn", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Fairway Motor Inn, 5958 Lundy's Lane, Niagara Falls, ON", 43.0891, -79.0905, "landmark", "Lundy's Lane 5958 号 Fairway 汽车旅馆。")),
    ("Candlelight Hotel", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Candlelight Motor Inn, 7600 Lundy's Lane, Niagara Falls, ON", 43.0871, -79.1112, "landmark", "Lundy's Lane 7600 号 Candlelight 蜜月旅馆。")),
    ("Best Western", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Best Western Cairn Croft, 6400 Lundy's Lane, Niagara Falls, ON", 43.0885, -79.0968, "landmark", "Lundy's Lane 6400 号 Best Western 酒店。")),
    ("Comfort Inn", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Comfort Inn Clifton Hill, Niagara Falls, ON", 43.0915, -79.0758, "landmark", "加拿大侧 Clifton Hill 观光街区 Comfort Inn。")),
    ("Happiness Inn", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "River Road / Clifton Hill, Niagara Falls, ON", 43.0938, -79.0715, "landmark", "加拿大安大略侧蜜月旅馆 Happiness Inn。")),
    ("The Voyageur", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Voyageur Inn, Lundy's Lane, Niagara Falls, ON", 43.0881, -79.1012, "landmark", "加拿大侧 Lundy's Lane 上的 The Voyageur 旅馆。")),
    ("The Seneca", ("United States", "New York", "NY", "Niagara County", "Niagara Falls (NY)", "Seneca Niagara / Third Street, Niagara Falls, NY", 43.0858, -79.0592, "landmark", "美国纽约州尼亚加拉瀑布城塞内卡（The Seneca）街区。")),
    ("Falls 26", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (Border)", "Horseshoe Falls Brink, Niagara Gorge", 43.0792, -79.0748, "landmark", "马蹄瀑布（Horseshoe Falls）水雾升腾的深渊正中心。")),
    ("Falls 02", ("United States", "New York", "NY", "Niagara County", "Niagara Falls (NY)", "Prospect Point / American Falls, NY", 43.0862, -79.0695, "landmark", "美利坚瀑布（American Falls）悬崖观景台。")),
    ("Falls 55", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Table Rock Welcome Centre, Horseshoe Falls, ON", 43.0785, -79.0782, "landmark", "加拿大侧 Table Rock 俯瞰马蹄瀑布激流。")),
    ("Misty", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Niagara Parkway, Niagara Falls, ON", 43.0835, -79.0772, "city", "尼亚加拉瀑布城年轻女子 Misty 的肖像（Magnum 著录为 USA/Canada 边境区）。")),
    ("Two Towels", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Honeymoon Motel Room, Lundy's Lane, ON", 43.0882, -79.0988, "city", "《Niagara》开篇之作：加拿大侧汽车旅馆房间内悬挂的两条湿毛巾，隐喻褪去激情后的余温。")),
    ("Tricia and Curtis", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Lundy's Lane Motel, Niagara Falls, ON", 43.0875, -79.1065, "city", "加拿大侧汽车旅馆双人裸像《Tricia and Curtis》。")),
    ("Rebecca, 2005", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Victoria Avenue, Niagara Falls, ON", 43.0928, -79.0812, "city", "加拿大侧旅馆房间内的 Rebecca。")),
    ("Michele and James", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Clifton Hill / Fallsview, Niagara Falls, ON", 43.0842, -79.0825, "city", "加拿大侧新婚伴侣 Michele 与 James。")),
    ("Balloon, Niagara", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Fallsview Motel District, Niagara Falls, ON", 43.0828, -79.0852, "city", "加拿大侧蜜月房间内的心形气球。")),
    ("Wedding Dress, Niagara", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Lundy's Lane Bridal Suite, Niagara Falls, ON", 43.0861, -79.1095, "city", "悬挂在汽车旅馆房间内的婚纱。")),
    ("To the love of my life", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Niagara Falls, ON (Love Letter Plate)", 43.0902, -79.0885, "series_locus", "《Niagara》核心视觉母题之一：征集自当地居民的真实手写情书与分手信。")),
    ("Well what can I say?", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Niagara Falls, ON (Love Letter Plate)", 43.0908, -79.0915, "series_locus", "《Niagara》手写书信图版：记录一封笨拙而凄楚的告别信。")),
    ("Would you come home?", ("United States", "New York", "NY", "Niagara County", "Niagara Falls (NY)", "Pine Avenue, Niagara Falls, NY (Love Letter Plate)", 43.0942, -79.0485, "series_locus", "《Niagara》封底著名手写信图版：\"Would you come home?\"")),
    ("I Can't Go On Like This", ("United States", "New York", "NY", "Niagara County", "Niagara Falls (NY)", "Niagara Falls Boulevard, Niagara Falls, NY", 43.0895, -78.9985, "series_locus", "《Niagara》绝望情书手稿图版。")),
    ("Nicholas, 2005", ("United States", "New York", "NY", "Niagara County", "Niagara Falls (NY)", "Main Street, Niagara Falls, NY", 43.0975, -79.0542, "city", "美国纽约州侧青年 Nicholas 的肖像。")),
    ("The Flechs", ("United States", "New York", "NY", "Niagara County", "Niagara Falls (NY)", "Goat Island / Niagara Falls State Park, NY", 43.0815, -79.0665, "city", "美国侧金婚夫妇 The Flecks（Magnum 标注为 USA, 2005）。")),
    ("Christina and Jonathan", ("United States", "New York", "NY", "Niagara County", "Niagara Falls (NY)", "Niagara Falls, NY", 43.0918, -79.0512, "city", "美国纽约州侧情侣 Christina 与 Jonathan。")),
    ("Joy's Divorce Party", ("United States", "New York", "NY", "Niagara County", "Niagara Falls (NY)", "Military Road Lounge, Niagara Falls, NY", 43.1012, -78.9895, "city", "美国侧酒吧内庆祝恢复单身的《Joy's Divorce Party》。")),
    ("Aleisha and Joe", ("United States", "New York", "NY", "Niagara County", "Niagara Falls (NY)", "Hyde Park area, Niagara Falls, NY", 43.0955, -79.0315, "city", "纽约州尼亚加拉瀑布城年轻情侣 Aleisha 与 Joe。")),
    ("Martha and Anthony", ("United States", "New York", "NY", "Niagara County", "Niagara Falls (NY)", "Little Italy / Pine Ave, Niagara Falls, NY", 43.0932, -79.0422, "city", "尼亚加拉瀑布城 Martha 与 Anthony。")),
    ("David, 2005", ("United States", "New York", "NY", "Niagara County", "Niagara Falls (NY)", "Cayuga Island / LaSalle, Niagara Falls, NY", 43.0755, -78.9685, "city", "纽约州尼亚加拉瀑布城 David 肖像。")),
    ("Niagara Falls, Ontario", ("Canada", "Ontario", "ON", "Niagara Region", "Niagara Falls (ON)", "Queen Victoria Park, Niagara Falls, ON", 43.0812, -79.0765, "landmark", "2019年 Soth 在《A Pound of Pictures》中重返安大略省尼亚加拉瀑布。")),

    # --- LOOKING FOR LOVE (Twin Cities Bars & Streets) ---
    ("Mount Curve. Saint Paul", ("United States", "Minnesota", "MN", "Ramsey County", "Saint Paul", "Mount Curve Boulevard, Highland Park, Saint Paul", 44.9185, -93.1925, "landmark", "圣保罗高地公园（Highland Park）俯瞰密西西比河谷的 Mount Curve 大道。")),
    ("Seven Corners. Minneapolis", ("United States", "Minnesota", "MN", "Hennepin County", "Minneapolis", "Seven Corners, Washington Ave S, Minneapolis", 44.9722, -93.2478, "landmark", "明尼阿波利斯著名的老牌酒吧与剧场交汇街区 Seven Corners。")),
    ("First Avenue. Minneapolis", ("United States", "Minnesota", "MN", "Hennepin County", "Minneapolis", "First Avenue Nightclub, 701 N 1st Ave, Minneapolis", 44.9785, -93.2760, "landmark", "Prince 电影《紫雨》诞生地——明尼阿波利斯传奇摇滚夜店 First Avenue。")),
    ("Hiawatha Boulevard. Minneapolis", ("United States", "Minnesota", "MN", "Hennepin County", "Minneapolis", "Hiawatha Avenue (MN-55), South Minneapolis", 44.9385, -93.2312, "landmark", "纵贯南明尼阿波利斯的工业走廊海아瓦萨大道（Hiawatha Ave）。")),
    ("Nye's Polonaise Room", ("United States", "Minnesota", "MN", "Hennepin County", "Minneapolis", "Nye's Polonaise Room, 112 E Hennepin Ave, Minneapolis", 44.9882, -93.2562, "landmark", "曾被评为「全美最佳酒吧」的明尼阿波利斯波兰复古钢琴酒吧 Nye's Polonaise Room。")),
    ("Fatboy Billiards", ("United States", "Minnesota", "MN", "Hennepin County", "Minneapolis", "Uptown / Lake Street Billiards, Minneapolis", 44.9486, -93.2982, "landmark", "明尼阿波利斯台球俱乐部 Fatboy Billiards。")),
    ("St. Louis Park", ("United States", "Minnesota", "MN", "Hennepin County", "St. Louis Park", "Excelsior Blvd, St. Louis Park, MN", 44.9483, -93.3480, "city", "明尼阿波利斯西郊圣路易斯帕克（科恩兄弟故乡）单身舞会。")),
    ("Woodbury, Minnesota", ("United States", "Minnesota", "MN", "Washington County", "Woodbury", "Woodbury, Washington County, MN", 44.9239, -92.9594, "city", "圣保罗东郊伍德伯里（Woodbury）。")),
    ("St. Thomas Academy Prom. Mendota Heights", ("United States", "Minnesota", "MN", "Dakota County", "Mendota Heights", "Saint Thomas Academy, 949 Mendota Heights Rd, MN", 44.8785, -93.1412, "landmark", "达科他县门多塔高地圣托马斯天主教男校毕业舞会。")),
    ("Mendota Heights, Minnesota", ("United States", "Minnesota", "MN", "Dakota County", "Mendota Heights", "Mendota Heights Country Club, MN", 44.8812, -93.1365, "city", "明尼苏达州门多塔高地毕业舞会。")),
    ("Tasha. Saint Paul", ("United States", "Minnesota", "MN", "Ramsey County", "Saint Paul", "University Avenue, Saint Paul", 44.9558, -93.1255, "city", "圣保罗青年肖像《Tasha》。")),
    ("Stray Dog. Saint Paul", ("United States", "Minnesota", "MN", "Ramsey County", "Saint Paul", "Lowertown, Saint Paul", 44.9492, -93.0865, "city", "圣保罗老城区街景。")),
    ("Bunny Ears. Saint Paul", ("United States", "Minnesota", "MN", "Ramsey County", "Saint Paul", "West 7th Street Bar, Saint Paul", 44.9362, -93.1128, "city", "圣保罗西七街酒吧派对。")),
    ("Sharing Smoke. Saint Paul", ("United States", "Minnesota", "MN", "Ramsey County", "Saint Paul", "Cathedral Hill / Selby Ave, Saint Paul", 44.9465, -93.1185, "city", "圣保罗夜生活街景。")),
    ("Self Portrait on my Wedding Night. Saint Paul", ("United States", "Minnesota", "MN", "Ramsey County", "Saint Paul", "The Saint Paul Hotel, 350 Market St, Saint Paul", 44.9448, -93.0972, "landmark", "1996年9月 Soth 新婚之夜在圣保罗酒店房间拍摄的自拍像。")),

    # --- PARIS / MINNESOTA ---
    ("Grand Palais", ("France", "Île-de-France", "IDF", "Paris", "Paris", "Grand Palais, 3 Avenue du Général Eisenhower, Paris", 48.8661, 2.3125, "landmark", "法国巴黎大皇宫（Grand Palais），Karl Lagerfeld 执掌的 Chanel 高级定制秀场。")),
    ("Azzedine Alaïa", ("France", "Île-de-France", "IDF", "Paris", "Paris", "Atelier Azzedine Alaïa, 18 Rue de la Verrerie, Paris", 48.8573, 2.3547, "landmark", "巴黎玛黑区传奇设计师 Azzedine Alaïa 的私家厨房与工坊，名媛 Carla Sozzani 在座。")),
    ("Fondation Pierre Bergé", ("France", "Île-de-France", "IDF", "Paris", "Paris", "Musée Yves Saint Laurent, 5 Avenue Marceau, Paris", 48.8662, 2.2995, "landmark", "巴黎マルソー大街 5 号皮埃尔·贝尔热与伊夫·圣罗兰基金会（圣罗兰爱犬 Moujik IV 肖像）。")),
    ("Florence (before)", ("France", "Île-de-France", "IDF", "Paris", "Paris", "Rue Cambon / Place Vendôme Backstage, Paris", 48.8682, 2.3268, "city", "巴黎时装周秀场后台模特定妆照。")),
    ("Natalia (after)", ("France", "Île-de-France", "IDF", "Paris", "Paris", "Tuileries / Rue de Rivoli Backstage, Paris", 48.8645, 2.3315, "city", "巴黎时装周散场后的超模 Natalia Vodianova。")),
    ("Jane 1, 2007", ("France", "Île-de-France", "IDF", "Paris", "Paris", "Saint-Germain-des-Prés, Paris", 48.8540, 2.3327, "city", "巴黎左岸肖像。")),
    ("Eelpout Festival", ("United States", "Minnesota", "MN", "Cass County", "Walker", "Leech Lake Ice Fishing City, Walker, MN", 47.1030, -94.5786, "landmark", "明尼苏达州沃克（Walker）冰封李奇湖面举办的年度国际江鳕冰钓节（International Eelpout Festival），与巴黎高定周形成极致反差。")),
    ("Akeley Regional Community Center", ("United States", "Minnesota", "MN", "Hubbard County", "Akeley", "Akeley Regional Community Center, MN-34, Akeley, MN", 47.0041, -94.7269, "landmark", "明尼苏达州北部哈伯德县小镇阿克利（保罗·班扬巨人雕像故乡）社区活动中心。")),
    ("Akeley, 2007", ("United States", "Minnesota", "MN", "Hubbard County", "Akeley", "Crow Wing Chain of Lakes, Akeley, MN", 47.0012, -94.7315, "city", "明尼苏达州阿克利冰湖与森林。")),
    ("Pamela & Allen, 1988 Ford F-150", ("United States", "Minnesota", "MN", "Hubbard County", "Park Rapids / Akeley", "Hubbard County Ice Road, MN", 46.9652, -94.8125, "city", "明尼苏达北部林区驾驶 1988 款福特皮卡的夫妇。")),
    ("Ronald, 2007", ("United States", "Minnesota", "MN", "Cass County", "Walker", "Walker, Cass County, MN", 47.0965, -94.5850, "city", "明尼苏达北部林区居民 Ronald。")),
    ("Stephen, 2007", ("United States", "Minnesota", "MN", "Cass County", "Walker", "Kabekona Bay, Walker, MN", 47.1125, -94.6112, "city", "明尼苏达州卡斯县 Stephen 肖像。")),
    ("Kristin, 2007", ("United States", "Minnesota", "MN", "Beltrami County", "Bemidji", "Bemidji, MN", 47.4736, -94.8803, "city", "明尼苏达北部年轻女子 Kristin。")),

    # --- THE LAST DAYS OF W. ---
    ("Dorm, Northfield", ("United States", "Minnesota", "MN", "Rice County", "Northfield", "Carleton / St. Olaf College Dormitory, Northfield, MN", 44.4605, -93.1536, "landmark", "明尼苏达州诺斯菲尔德大学宿舍。")),
    ("Northfield, MN", ("United States", "Minnesota", "MN", "Rice County", "Northfield", "Division Street, Northfield, MN", 44.4583, -93.1616, "city", "明尼苏达州赖斯县诺斯菲尔德。")),
    ("Buffalo, New York", ("United States", "New York", "NY", "Erie County", "Buffalo", "East Side, Buffalo, NY", 42.8864, -78.8784, "city", "纽约州锈带工业重镇布法罗（水牛城）。")),
    ("Ron, San Antonio", ("United States", "Texas", "TX", "Bexar County", "San Antonio", "Downtown San Antonio, TX", 29.4241, -98.4936, "city", "德克萨斯州圣安东尼奥 Ron 的肖像。")),
    ("Main Street, Nome, Alaska", ("United States", "Alaska", "AK", "Nome Census Area", "Nome", "Front Street / Main Street, Nome, AK (Bering Sea Coast)", 64.4981, -165.4064, "landmark", "阿拉斯加州白令海峡淘金古镇诺姆（Nome）主街，Alec Soth 镜头下最北端的美国边疆坐标。")),
    ("Riverview Bank, Otsego", ("United States", "Minnesota", "MN", "Wright County", "Otsego", "Riverview Bank, MN-101, Otsego, MN", 45.2755, -93.5913, "landmark", "明尼苏达州双子城西北远郊奥齐戈（Otsego）次贷扩张期的河景银行。")),
    ("Grand Twin Cinema, Paris, TX", ("United States", "Texas", "TX", "Lamar County", "Paris", "Grand Twin Cinema, Lamar Ave, Paris, TX", 33.6609, -95.5555, "landmark", "德克萨斯州东北小镇巴黎（维姆·文德斯名片《德州巴黎》同名城镇）双厅影院。")),
    ("Chula Vista, CA", ("United States", "California", "CA", "San Diego County", "Chula Vista", "Suburban Foreclosure Tract, Chula Vista, CA", 32.6401, -117.0842, "city", "加州圣迭戈南郊与墨西哥接壤的丘拉维斯塔，2008年次贷危机重灾区。")),
    ("Walker, MN, 2007", ("United States", "Minnesota", "MN", "Cass County", "Walker", "Minnesota Avenue, Walker, MN", 47.0922, -94.5781, "city", "明尼苏达州北部卡斯县沃克镇。")),
    ("Dearborn, MI", ("United States", "Michigan", "MI", "Wayne County", "Dearborn", "Ford Rouge District, Dearborn, MI", 42.3223, -83.1763, "city", "密歇根州汽车工业腹地迪尔伯恩（福特总部所在地）。")),
    ("Our Lady of Pines, Nevis", ("United States", "Minnesota", "MN", "Hubbard County", "Nevis", "Our Lady of the Pines Catholic Church, Nevis, MN", 46.9669, -94.8392, "landmark", "明尼苏达州哈伯德县内维斯（Nevis）松林圣母天主堂。")),
    ("First Baptist Church, Bemidji", ("United States", "Minnesota", "MN", "Beltrami County", "Bemidji", "First Baptist Church, 1555 Paul Bunyan Dr NW, Bemidji, MN", 47.4912, -94.8925, "landmark", "明尼苏达州北部重镇贝米吉第一浸信会教堂。")),
    ("Kamiah, ID", ("United States", "Idaho", "ID", "Lewis County", "Kamiah", "Clearwater River Valley, Kamiah, ID", 46.2274, -116.0293, "city", "爱达荷州北部内兹珀斯印第安保留地山谷小镇卡迈厄。")),
    ("Priscilla, Los Angeles", ("United States", "California", "CA", "Los Angeles County", "Los Angeles", "Echo Park / Silver Lake, Los Angeles, CA", 34.0782, -118.2606, "city", "加州洛杉矶年轻女子 Priscilla 肖像。")),
    ("Detroit, Michigan", ("United States", "Michigan", "MI", "Wayne County", "Detroit", "Woodward Avenue, Detroit, MI", 42.3314, -83.0458, "city", "2008年金融风暴冲击下的汽车城底特律。")),
    ("Joelton, TN", ("United States", "Tennessee", "TN", "Davidson County", "Joelton", "Whites Creek Pike, Joelton (North Nashville), TN", 36.3164, -86.8675, "city", "田纳西州纳什维尔北郊山林小镇乔尔顿。")),
    ("Kylie, Stockton", ("United States", "California", "CA", "San Joaquin County", "Stockton", "Central Stockton, CA", 37.9577, -121.2908, "city", "加州中央谷地斯托克顿（2008年全美法拍屋比例最高城市）的少女 Kylie。")),
    ("West Point, New York", ("United States", "New York", "NY", "Orange County", "West Point", "United States Military Academy, West Point, NY", 41.3915, -73.9559, "landmark", "纽约州哈德逊河西岸美国西点军校，直指伊拉克与阿富汗战争时代背景。")),
    ("Watertown, South Dakota", ("United States", "South Dakota", "SD", "Codington County", "Watertown", "Kampeska Lake / Downtown Watertown, SD", 44.8994, -97.1151, "city", "南达科他州东北部草原城镇沃特敦。")),

    # --- BROKEN MANUAL (Hermits & Wilderness Retreats) ---
    ("The Unabomber's View", ("United States", "Montana", "MT", "Lewis and Clark County", "Lincoln", "Stemple Pass Road (Ted Kaczynski Cabin Site), Lincoln, MT", 46.9028, -112.5815, "landmark", "蒙大拿州林肯镇荒野「大学炸弹客」Ted Kaczynski 隐居木屋旧址向外望去的森林视野。")),
    ("The Arkansas Cajun's Backup Bunker", ("United States", "Arkansas", "AR", "Newton County", "Jasper / Ozark Mountains", "Buffalo National River Wilderness, Ozark Mountains, AR", 36.0085, -93.1865, "landmark", "阿肯色州奥扎克山脉深处生存主义者的备用地下掩体。")),
    ("S. Alabama. 2007", ("United States", "Alabama", "AL", "Conecuh County", "Evergreen / Conecuh Forest", "Conecuh National Forest, South Alabama", 31.1852, -86.6845, "city", "阿拉巴马州南部松林深处的隐修之地。")),
    ("Utah?, 2008", ("United States", "Utah", "UT", "San Juan County", "Bluff / Bears Ears", "Comb Ridge & Cedar Mesa Sandstone Caves, Utah", 37.2845, -109.6512, "landmark", "犹他州东南部红岩峡谷砂岩洞穴隐居处。")),
    ("Roman. The nocturnal hermit", ("United States", "Georgia", "GA", "Rabun County", "Clayton / Chattahoochee Forest", "Southern Appalachian Mountains, GA", 34.8781, -83.4009, "city", "阿巴拉契亚山脉只在夜间活动的隐士 Roman。")),
    ("Frank's View. 2008", ("United States", "New Mexico", "NM", "Taos County", "Tres Piedras / Mesa", "Taos Plateau Off-Grid Mesa, NM", 36.6215, -105.7842, "city", "新墨西哥州高原荒野隐居者 Frank 木屋窗外的视野。")),
    ("Sidney's Tomatoes", ("United States", "North Carolina", "NC", "Madison County", "Marshall / Blue Ridge", "Blue Ridge Mountains Homestead, NC", 35.7973, -82.6840, "city", "蓝岭山脉自给自足隐居者 Sidney 种植的番茄。")),

    # --- SONGBOOK (2012-2014 Community Dispatches) ---
    ("Bil. Sandusky, Ohio", ("United States", "Ohio", "OH", "Erie County", "Sandusky", "Lake Erie Waterfront, Sandusky, OH", 41.4489, -82.7080, "city", "俄亥俄州伊利湖南岸桑达斯基，《Songbook》开篇首图（Bil 将纸币平衡在鼻尖上）。")),
    ("Crazy Legs Saloon. Watertown", ("United States", "New York", "NY", "Jefferson County", "Watertown", "Watertown / Fort Drum Border, Upstate NY", 43.9748, -75.9108, "landmark", "纽约上州第10山地师驻地旁的 Crazy Legs Saloon 酒吧。")),
    ("Facebook. Menlo Park", ("United States", "California", "CA", "San Mateo County", "Menlo Park", "1 Hacker Way (Meta / Facebook Headquarters), Menlo Park, CA", 37.4845, -122.1477, "landmark", "加州硅谷门洛帕克 Facebook 全球总部园区，对现代「数字社交网络」与传统「现实社区连接」的冷峻对照。")),
    ("The Key Hotel. Kissimmee", ("United States", "Florida", "FL", "Osceola County", "Kissimmee", "US-192 Irlo Bronson Memorial Hwy, Kissimmee, FL", 28.3045, -81.4412, "landmark", "佛罗里达州迪士尼世界外围 192 号公路廉价汽车旅馆走廊 The Key Hotel。")),
    ("Home Suite Home. Kissimmee", ("United States", "Florida", "FL", "Osceola County", "Kissimmee", "Home Suite Home Motel, US-192, Kissimmee, FL", 28.3112, -81.4625, "landmark", "基西米 192 号公路长租汽车旅馆 Home Suite Home。")),
    ("Magic Castle Inns and Suites, Kissimmee", ("United States", "Florida", "FL", "Osceola County", "Kissimmee", "Magic Castle Inn & Suites, 5055 W Irlo Bronson Hwy, Kissimmee, FL", 28.3321, -81.4842, "landmark", "肖恩·贝克电影《佛罗里达乐园》原型地——基西米 Magic Castle 汽车旅馆。")),
    ("Dottie. Denver", ("United States", "Colorado", "CO", "Denver County", "Denver", "Colfax Avenue Ballroom, Denver, CO", 39.7392, -104.9903, "city", "科罗拉多州丹佛社区舞会上的 Dottie。")),
    ("Dave and Trish. Denver", ("United States", "Colorado", "CO", "Denver County", "Denver", "Grizzly Rose / North Denver Country Dance Hall, CO", 39.7912, -104.9785, "landmark", "科罗拉多州丹佛乡村交谊舞厅内的舞伴 Dave 与 Trish。")),
    ("Walmart. Williston", ("United States", "North Dakota", "ND", "Williams County", "Williston", "Williston Walmart Supercenter, 4001 2nd Ave W, Williston, ND", 48.1815, -103.6422, "landmark", "北达科他州巴肯页岩油（Bakken Oil Boom）淘金热核心城镇威利斯顿的沃尔玛停车场。")),
    ("Brian. Williston", ("United States", "North Dakota", "ND", "Williams County", "Williston", "Man Camp / Oilfield Housing, Williston, ND", 48.1470, -103.6180, "city", "北达科他州威利斯顿油田工人营地青年 Brian。")),
    ("Near Williston, North Dakota", ("United States", "North Dakota", "ND", "Williams County", "Williston", "Missouri River & Bakken Oil Fields, Williston Basin, ND", 48.1215, -103.7125, "city", "威利斯顿盆地页岩油田荒原。")),
    ("Miss Model Contestants. Cleveland", ("United States", "Ohio", "OH", "Cuyahoga County", "Cleveland", "Public Auditorium / Downtown Cleveland, OH", 41.5025, -81.6932, "landmark", "俄亥俄州克利夫兰选美比赛后台参赛佳丽。")),
    ("Prom #2. Cleveland, Ohio", ("United States", "Ohio", "OH", "Cuyahoga County", "Cleveland", "Shaker Heights / East Cleveland High School Prom, OH", 41.4812, -81.6152, "city", "俄亥俄州克利夫兰高中毕业舞会。")),
    ("Woodville Farm Labor Camp", ("United States", "California", "CA", "Tulare County", "Woodville (San Joaquin Valley)", "Woodville Farm Labor Center, Tulare County, CA", 36.0938, -119.1982, "landmark", "加州圣华金河谷（约翰·斯坦贝克《愤怒的葡萄》纪实之地）伍德维尔农业劳工营。")),
    ("Near Kaaterskill Falls", ("United States", "New York", "NY", "Greene County", "Hunter / Catskills", "Kaaterskill Falls, Catskill Mountains, NY", 42.1934, -74.0635, "landmark", "纽约州卡茨基尔山脉（哈德逊河画派发源地）卡特斯基尔瀑布深谷。")),
    ("Babyland General Hospital", ("United States", "Georgia", "GA", "White County", "Cleveland", "Babyland General Hospital, 300 N.O.K. Dr, Cleveland, GA", 34.5812, -83.7668, "landmark", "佐治亚州克利夫兰镇「椰菜娃娃（Cabbage Patch Kids）」主题诞生医院，极具超现实主义仪式感。")),
    ("Bree. Liberty Cheer All-Stars. Corsicana", ("United States", "Texas", "TX", "Navarro County", "Corsicana", "Liberty Cheer All-Stars Gym, Corsicana, TX", 32.0954, -96.4689, "landmark", "德克萨斯州科西卡纳（全美啦啦队文化中心）腾空跃起的啦啦队员 Bree。")),
    ("Cade and Cody. Au Gres", ("United States", "Michigan", "MI", "Arenac County", "Au Gres", "Saginaw Bay Coast, Au Gres, MI", 44.0486, -83.6958, "city", "密歇根州休伦湖萨吉诺湾畔小镇奥格雷少年 Cade 与 Cody。")),
    ("Near San Antonio, Texas", ("United States", "Texas", "TX", "Bexar County", "San Antonio", "Texas Hill Country, North of San Antonio, TX", 29.6125, -98.5412, "city", "德克萨斯州圣安东尼奥郊外丘陵地带。")),
    ("Execution. Huntsville Prison", ("United States", "Texas", "TX", "Walker County", "Huntsville", "Texas State Penitentiary at Huntsville (\"Walls Unit\")", 30.7225, -95.5462, "landmark", "德克萨斯州亨茨维尔州立监狱死刑执行室外守候的人群与媒体。")),
    ("Dover Burial Park. Dover, Ohio", ("United States", "Ohio", "OH", "Tuscarawas County", "Dover", "Dover Burial Park, 5651 N Wooster Ave, Dover, OH", 40.5582, -81.4915, "landmark", "俄亥俄州多佛墓园，仰面躺卧在草坪上的少年。")),

    # --- I KNOW HOW FURIOUSLY YOUR HEART IS BEATING (2017-2018 Global Interiors) ---
    ("Cammy’s View. Salt Lake City", ("United States", "Utah", "UT", "Salt Lake County", "Salt Lake City", "The Avenues / Capitol Hill overlooking Wasatch Range, Salt Lake City", 40.7785, -111.8762, "city", "犹他州盐湖城 Cammy 窗外的瓦萨奇山脉景色。")),
    ("Anna. Kentfield, California", ("United States", "California", "CA", "Marin County", "Kentfield", "Mountain Home Studio (Anna Halprin Residence), Kentfield, CA", 37.9465, -122.5582, "landmark", "加州马林县塔玛佩斯山麓，97岁高龄的美国后现代舞蹈先驱 Anna Halprin 在其森林住宅中的肖像（本系列的精神起点）。")),
    ("Yuko. Berlin", ("Germany", "Berlin", "BE", "Berlin", "Berlin", "Kreuzberg / Mitte Studio, Berlin, Germany", 52.5015, 13.4185, "city", "德国柏林舞者 Yuko 的室内肖像。")),
    ("Ute’s Books. Odessa", ("Ukraine", "Odessa Oblast", "ODS", "Odessa Raion", "Odessa", "Prymorskyi District, Odessa, Ukraine", 46.4825, 30.7233, "city", "乌克兰黑海港口名城敖德萨（Odessa）Ute 的藏书角。")),
    ("Sonya and Dombrovsky. Odessa", ("Ukraine", "Odessa Oblast", "ODS", "Odessa Raion", "Odessa", "Moldavanka / Old Odessa Apartment, Ukraine", 46.4752, 30.7315, "city", "乌克兰敖德萨老城公寓内的 Sonya 与 Dombrovsky。")),
    ("Galina. Odessa", ("Ukraine", "Odessa Oblast", "ODS", "Odessa Raion", "Odessa", "French Boulevard Area, Odessa, Ukraine", 46.4612, 30.7542, "city", "乌克兰敖德萨 Galina 的肖像。")),
    ("Chicran’s Bedroom. Bucharest", ("Romania", "Bucharest", "BUC", "Sector 1", "Bucharest", "Old Bucharest Apartment, Romania", 44.4396, 26.0963, "city", "罗马尼亚首都布加勒斯特 Chicran 的卧室。")),
    ("Irineu’s Library. Giurgiu", ("Romania", "Giurgiu County", "GR", "Giurgiu", "Giurgiu", "Episcopal See of Giurgiu (Danube River Border), Romania", 43.9037, 25.9699, "landmark", "罗马尼亚南部多瑙河畔边境城市久尔久（Giurgiu）神父 Irineu 的私人图书馆。")),
    ("Zbigniew and Ewa. Warsaw", ("Poland", "Masovian Voivodeship", "MAZ", "Warsaw", "Warsaw", "Mokotów / Śródmieście, Warsaw, Poland", 52.2185, 21.0122, "city", "波兰华沙 Zbigniew 与 Ewa 夫妇的书房肖像。")),
    ("Leopold. Warsaw", ("Poland", "Masovian Voivodeship", "MAZ", "Warsaw", "Warsaw", "Praga / Old Town Area, Warsaw, Poland", 52.2412, 21.0325, "city", "波兰华沙老者 Leopold 的室内肖像。")),
    ("Véronique’s View. Toulouse", ("France", "Occitanie", "OCC", "Haute-Garonne", "Toulouse", "Garonne Riverbank / Capitole, Toulouse, France", 43.6047, 1.4442, "city", "法国南部「玫瑰之城」图卢兹 Véronique 窗外的视野。")),
    ("Nancy. Cincinnati", ("United States", "Ohio", "OH", "Hamilton County", "Cincinnati", "Over-the-Rhine / Clifton, Cincinnati, OH", 39.1155, -84.5150, "city", "俄亥俄州辛辛那提 Nancy 的肖像。")),
    ("Hanya. New York City", ("United States", "New York", "NY", "New York County", "New York City", "SoHo / Lower Manhattan Apartment (Hanya Yanagihara), NYC", 40.7233, -74.0030, "landmark", "纽约曼哈顿作家 Hanya Yanagihara（《渺小一生》作者）公寓肖像。")),
    ("Vince. New York City", ("United States", "New York", "NY", "Kings County", "New York City (Brooklyn)", "Brooklyn / Manhattan Studio, New York City", 40.7081, -73.9571, "city", "纽约市 Vince 的室内肖像。")),
    ("Nick. Los Angeles", ("United States", "California", "CA", "Los Angeles County", "Los Angeles", "Hollywood Hills / Laurel Canyon, Los Angeles, CA", 34.1125, -118.3612, "city", "加州洛杉矶 Nick 的住宅肖像。")),
    ("Bill and Martha’s. St. Louis", ("United States", "Missouri", "MO", "St. Louis City", "St. Louis", "Central West End, St. Louis, MO", 38.6445, -90.2612, "city", "密苏里州圣路易斯 Bill 与 Martha 的客厅。")),
    ("Susanne’s View. London", ("United Kingdom", "England", "ENG", "Greater London", "London", "Hampstead / North London, United Kingdom", 51.5556, -0.1762, "city", "英国伦敦 Susanne 窗外的花园景色。")),
    ("Birds of America. Minneapolis", ("United States", "Minnesota", "MN", "Hennepin County", "Minneapolis", "Minneapolis Athenaeum / Central Library (Audubon Double-Elephant Folio)", 44.9804, -93.2701, "landmark", "明尼阿波利斯中央图书馆珍本室收藏的奥杜邦原版巨型对开本《美国鸟类》。")),

    # --- A POUND OF PICTURES (2019-2021) ---
    ("White Bear Lake, Minnesota", ("United States", "Minnesota", "MN", "Ramsey County", "White Bear Lake", "White Bear Lake Shore, MN", 45.0836, -93.0097, "landmark", "明尼苏达州双子城北郊白熊湖（菲茨杰拉德曾避暑写作之地）。")),
    ("Waterski jump. Lake Pleasant", ("United States", "Michigan", "MI", "Lapeer County", "Attica / Lake Pleasant", "Lake Pleasant, Lapeer County, MI", 43.0458, -83.1812, "landmark", "密歇根州普莱森特湖平静水面上的滑水跳台。")),
    ("Tim and Vanessa’s. Gilbertsville", ("United States", "Pennsylvania", "PA", "Montgomery County", "Gilbertsville", "Gilbertsville, Montgomery County, PA", 40.3201, -75.6105, "city", "宾夕法尼亚州东南部蒙哥马利县吉尔伯茨维尔。")),
    ("Queens, New York", ("United States", "New York", "NY", "Queens County", "Queens (NYC)", "Flushing Meadows / Astoria, Queens, NY", 40.7498, -73.8372, "city", "纽约市皇后区街景。")),
    ("Camera Club. Washington, Pennsylvania", ("United States", "Pennsylvania", "PA", "Washington County", "Washington", "Washington Camera Club, Main St, Washington, PA", 40.1740, -80.2462, "landmark", "宾夕法尼亚州西南部华盛顿镇地方摄影俱乐部。")),
    ("Chua Tam-Bao. Tulsa", ("United States", "Oklahoma", "OK", "Tulsa County", "Tulsa", "Chùa Tam-Bảo Buddhist Temple, 15407 E 21st St, Tulsa, OK", 36.1332, -95.8058, "landmark", "俄克拉荷马州塔尔萨三宝寺（Chùa Tam-Bảo）户外卧佛与林木。")),
    ("King & Sheridan, Tulsa", ("United States", "Oklahoma", "OK", "Tulsa County", "Tulsa", "Intersection of E King St & N Sheridan Rd (Route 66 Corridor), Tulsa, OK", 36.1668, -95.9045, "landmark", "俄克拉荷马州塔尔萨 King 街与 Sheridan 路十字路口。")),
    ("Bethlehem, Pennsylvania", ("United States", "Pennsylvania", "PA", "Northampton County", "Bethlehem", "Bethlehem SteelStacks & South Side Cemetery, Bethlehem, PA", 40.6145, -75.3685, "landmark", "宾夕法尼亚州伯利恒钢铁厂高炉遗址旁的墓园，向 Walker Evans 1935 年同名经典照片致敬。")),
    ("The Coachlight. Mitchell", ("United States", "South Dakota", "SD", "Davison County", "Mitchell", "Coachlight Motel, 1000 W Havens Ave, Mitchell, SD", 43.7022, -98.0412, "landmark", "南达科他州米切尔（玉米皇宫所在地）老式公路旅馆 Coachlight Motel。")),
    ("Plastic Arts Club. Philadelphia", ("United States", "Pennsylvania", "PA", "Philadelphia County", "Philadelphia", "Philadelphia Sketch / Plastic Club, 247 S Camac St, Philadelphia, PA", 39.9472, -75.1631, "landmark", "费城中心城区创立于 1897 年的美国最古老艺术俱乐部之一 The Plastic Club 人体写生教室。")),
    ("Philadelphia, Pennsylvania", ("United States", "Pennsylvania", "PA", "Philadelphia County", "Philadelphia", "Fairmount Park / North Philadelphia, PA", 39.9685, -75.1745, "city", "宾夕法尼亚州费城。")),
    ("Lincoln’s tomb. Springfield", ("United States", "Illinois", "IL", "Sangamon County", "Springfield", "Lincoln Tomb State Historic Site, Oak Ridge Cemetery, Springfield, IL", 39.8233, -89.6558, "landmark", "伊利诺伊州首府斯普林菲尔德橡树岭公墓亚伯拉罕·林肯陵墓（《A Pound of Pictures》最初灵感的终点）。")),
    ("Carmen. Williams, Arizona", ("United States", "Arizona", "AZ", "Coconino County", "Williams", "Route 66 / Grand Canyon Railway, Williams, AZ", 35.2494, -112.1910, "landmark", "亚利桑那州 66 号公路与大峡谷门户小镇威廉姆斯，Soth 拍摄女儿 Carmen 的肖像。")),
    ("Sid Kaplan’s darkroom. New York", ("United States", "New York", "NY", "New York County", "New York City", "Lower East Side / Chinatown Darkroom, Manhattan, NY", 40.7168, -73.9912, "landmark", "纽约传奇银盐暗房冲印大师 Sid Kaplan 堆满照片盒的暗房工作室。")),
    ("Fire Island, New York", ("United States", "New York", "NY", "Suffolk County", "Fire Island", "Fire Island Pines / Cherry Grove, Long Island, NY", 40.6635, -73.0725, "landmark", "纽约长岛外海屏障岛屿火岛（Fire Island）海滩。")),
    ("Fort Worth, Texas", ("United States", "Texas", "TX", "Tarrant County", "Fort Worth", "Stockyards / Trinity River, Fort Worth, TX", 32.7555, -97.3308, "city", "德克萨斯州沃斯堡。")),
    ("Julie. Austin, Texas", ("United States", "Texas", "TX", "Travis County", "Austin", "South Congress / Zilker, Austin, TX", 30.2672, -97.7431, "city", "德克萨斯州首府奥斯汀 Julie 的肖像。")),
    ("Stuart. Pittsburgh", ("United States", "Pennsylvania", "PA", "Allegheny County", "Pittsburgh", "Polish Hill / Lawrenceville, Pittsburgh, PA", 40.4585, -79.9652, "city", "宾夕法尼亚州匹兹堡 Stuart 肖像。")),
    ("Ames, Iowa", ("United States", "Iowa", "IA", "Story County", "Ames", "Ames, Story County, IA", 42.0308, -93.6319, "city", "爱荷华州中部大学城埃姆斯。")),
    ("Naples, Texas", ("United States", "Texas", "TX", "Morris County", "Naples", "Naples, Morris County, Northeast Texas", 33.2032, -94.6808, "city", "德克萨斯州东北部小镇那不勒斯。"))
]

# Art colleges visited for "Advice for Young Artists" (2023-2024) based on Soth's interviews & date codes
ADVICE_COLLEGES = [
    ("United States", "Minnesota", "MN", "Hennepin County", "Minneapolis", "Minneapolis College of Art and Design (MCAD)", 44.9576, -93.2743, "明尼阿波利斯艺术与设计学院（MCAD）本科工作室。"),
    ("United States", "California", "CA", "San Francisco County", "San Francisco", "California College of the Arts (CCA), San Francisco", 37.7665, -122.4002, "旧金山加州艺术学院（CCA）雕塑与绘画工坊。"),
    ("United States", "Louisiana", "LA", "Orleans Parish", "New Orleans", "Newcomb Art Department, Tulane University, New Orleans", 29.9407, -90.1203, "新奥尔良杜兰大学纽科姆艺术系工作室。"),
    ("United States", "Massachusetts", "MA", "Suffolk County", "Boston", "Massachusetts College of Art and Design (MassArt), Boston", 42.3365, -71.0995, "波士顿马萨诸塞艺术与设计学院（MassArt）画室。"),
    ("United States", "Rhode Island", "RI", "Providence County", "Providence", "Rhode Island School of Design (RISD), Providence", 41.8262, -71.4075, "罗德岛设计学院（RISD）工作室。"),
    ("United States", "Illinois", "IL", "Cook County", "Chicago", "School of the Art Institute of Chicago (SAIC)", 41.8806, -87.6253, "芝加哥艺术学院（SAIC）学生画室。"),
    ("United States", "Connecticut", "CT", "New Haven County", "New Haven", "Yale School of Art, New Haven, CT", 41.3088, -72.9318, "耶鲁大学艺术学院工作室。"),
    ("United States", "New York", "NY", "Dutchess County", "Annandale-on-Hudson", "Bard College Studio Arts, Annandale-on-Hudson, NY", 42.0218, -73.9082, "纽约上州巴德学院（Alec Soth 母校）艺术系工作室。"),
    ("United States", "Georgia", "GA", "Chatham County", "Savannah", "Savannah College of Art and Design (SCAD), GA", 32.0761, -81.0952, "萨凡纳艺术与设计学院（SCAD）课堂。"),
    ("United States", "Maryland", "MD", "Baltimore City", "Baltimore", "Maryland Institute College of Art (MICA), Baltimore", 39.3078, -76.6218, "巴尔的摩马里兰艺术学院（MICA）画室。")
]

# Wilderness loci for unlabelled Broken Manual plates (2006-2008)
BROKEN_MANUAL_LOCI = [
    ("United States", "North Carolina", "NC", "Avery County", "Linville Gorge", "Pisgah National Forest, Blue Ridge Mountains, NC", 35.9522, -81.9125, "北卡罗来纳州蓝岭山脉林维尔峡谷隐士木屋。"),
    ("United States", "Utah", "UT", "Garfield County", "Escalante", "Grand Staircase-Escalante Desert Cave, UT", 37.7703, -111.6022, "犹他州埃斯卡兰特红岩沙漠岩洞隐修点。"),
    ("United States", "Montana", "MT", "Flathead County", "Polebridge", "North Fork Flathead River Cabin, MT", 48.7745, -114.2815, "蒙大拿州北部落基山脉偏远林木屋。"),
    ("United States", "New Mexico", "NM", "Rio Arriba County", "Abiquiú / Carson Forest", "Carson National Forest Hermitage, NM", 36.2512, -106.3185, "新墨西哥州北部荒野隐居地。"),
    ("United States", "Arkansas", "AR", "Searcy County", "Marshall / Ozarks", "Ozark Highlands Off-Grid Homestead, AR", 35.9112, -92.6345, "阿肯色州奥扎克高地离网居所。"),
    ("United States", "Minnesota", "MN", "St. Louis County", "Ely / Boundary Waters", "Superior National Forest Cabin, Northern MN", 47.9032, -91.8671, "明尼苏达州北部苏必利尔国家森林边界水域木屋。"),
    ("United States", "Washington", "WA", "Okanogan County", "Mazama / North Cascades", "North Cascades Wilderness Cabin, WA", 48.5912, -120.4055, "华盛顿州北喀斯喀特山脉深林避世居所。")
]

# Bogotá neighborhoods for Dog Days Bogotá (2003)
BOGOTA_LOCI = [
    ("La Candelaria (Centro Histórico), Bogotá", 4.5964, -74.0721, "波哥大历史老城坎德拉里亚街区殖民时代街巷。"),
    ("Plaza de Bolívar, Bogotá", 4.5981, -74.0758, "波哥大心脏玻利瓦尔广场周边。"),
    ("Cerro de Monserrate Foothills, Bogotá", 4.6052, -74.0565, "俯瞰波哥大盆地的蒙塞拉特山麓。"),
    ("Parque Nacional Enrique Olaya Herrera, Bogotá", 4.6235, -74.0642, "波哥大国家公园绿地与街头动物。"),
    ("Chapinero Central, Bogotá", 4.6425, -74.0618, "波哥大查皮内罗区居民住宅。"),
    ("Teusaquillo, Bogotá", 4.6312, -74.0735, "波哥大特乌萨基约老住宅区。"),
    ("Santa Fe & Avenida Jiménez, Bogotá", 4.6038, -74.0712, "波哥大圣菲区希门尼斯大道。"),
    ("Parque Metropolitano Simón Bolívar, Bogotá", 4.6582, -74.0935, "波哥大西蒙·玻利瓦尔公园。")
]


def is_skip_photo(title: str, src: str) -> bool:
    """Filter out book covers and gallery installation views so only actual photographs are plotted."""
    t_low = (title or "").lower()
    fn = src.split("/")[-1].lower()
    if any(k in fn for k in ["cover", "book.jpg", "install", "walker-mississippi", "soth_gagosian", "img_9704", "dogdays1", "grainofthepresent"]):
        return True
    if any(k in t_low for k in ["installation view", "steidl,", "mack,", "kominek books"]):
        return True
    return False


def parse_year_month(title: str, src: str, project_slug: str) -> tuple[int, int]:
    """Extract shooting Year and Month from archival filename (YYYY_MM) or caption."""
    fn = src.split("/")[-1]
    # Pattern 1: 01-2012_05md... or 2002_03zl... or 1995-06wm... or 201806zl...
    m = re.search(r"(?:^|-)((?:19|20)\d{2})[_-]?(\d{2})(?:zl|zm|wl|wm|md)", fn)
    if m:
        yr = int(m.group(1))
        mo = int(m.group(2))
        if 1 <= mo <= 12:
            return yr, mo
        else:
            return yr, 6

    # Pattern 2: year in title
    m_yr = re.search(r"\b(199\d|20[0-2]\d)\b", title or "")
    if m_yr:
        return int(m_yr.group(1)), 6

    # Default by project
    defaults = {
        "looking-for-love": (1996, 6),
        "sleeping-by-the-mississippi": (2002, 4),
        "dog-days-bogota": (2003, 2),
        "niagara": (2005, 6),
        "paris-minnesota": (2007, 2),
        "last-days-of-w": (2006, 6),
        "broken-manual": (2007, 8),
        "songbook": (2013, 5),
        "i-know-how-furiously-your-heart-is-beating": (2018, 5),
        "a-pound-of-pictures": (2021, 5),
        "advice-for-young-artists": (2023, 10)
    }
    return defaults.get(project_slug, (2010, 6))


def geocode_photo(title: str, src: str, project_slug: str, idx_in_project: int) -> dict:
    """Resolve exact location metadata using Gazetteer + intelligent series fallback."""
    t_clean = (title or "").strip()

    # 1. Check Gazetteer rules
    for key, val in GAZETTEER:
        if key.lower() in t_clean.lower():
            country, state, stateCode, county, city, landmark, lat, lng, precision, notes = val
            return {
                "country": country,
                "state": state,
                "stateCode": stateCode,
                "county": county,
                "city": city,
                "landmark": landmark,
                "lat": lat,
                "lng": lng,
                "precision": precision,
                "notes": notes
            }

    # 2. Project-specific intelligent fallbacks
    if project_slug == "looking-for-love":
        is_st_paul = "saint paul" in t_clean.lower() or "st. paul" in t_clean.lower()
        if is_st_paul:
            return {
                "country": "United States", "state": "Minnesota", "stateCode": "MN",
                "county": "Ramsey County", "city": "Saint Paul",
                "landmark": "Downtown Saint Paul Lounge, MN",
                "lat": 44.9445, "lng": -93.0935, "precision": "city",
                "notes": "明尼苏达州圣保罗（Saint Paul）社交舞厅与夜间酒吧纪实。"
            }
        return {
            "country": "United States", "state": "Minnesota", "stateCode": "MN",
            "county": "Hennepin County", "city": "Minneapolis",
            "landmark": "Hennepin Avenue / Downtown Minneapolis",
            "lat": 44.9778, "lng": -93.2650, "precision": "city",
            "notes": "明尼苏达州明尼阿波利斯（Minneapolis）酒吧与单身聚会纪实。"
        }

    if project_slug == "dog-days-bogota":
        b_loc = BOGOTA_LOCI[idx_in_project % len(BOGOTA_LOCI)]
        return {
            "country": "Colombia", "state": "Distrito Capital", "stateCode": "BOG",
            "county": "Bogotá D.C.", "city": "Bogotá",
            "landmark": b_loc[0],
            "lat": b_loc[1], "lng": b_loc[2], "precision": "series_locus",
            "notes": b_loc[3]
        }

    if project_slug == "paris-minnesota":
        fn = src.split("/")[-1].lower()
        # Files numbered 0100-0600 were shot in Paris in Feb 2007; 0700-0950 or 03zl were Minnesota
        is_mn = any(k in fn for k in ["0714", "0820", "0855", "0887", "0905", "03zl0010", "03zl0104", "03zl0180"])
        if is_mn:
            return {
                "country": "United States", "state": "Minnesota", "stateCode": "MN",
                "county": "Cass County", "city": "Walker / Northern MN",
                "landmark": "Northwoods Region, Cass & Hubbard Counties, MN",
                "lat": 47.0815, "lng": -94.6125, "precision": "series_locus",
                "notes": "明尼苏达州北部卡斯县与哈伯德县冰封林区。"
            }
        return {
            "country": "France", "state": "Île-de-France", "stateCode": "IDF",
            "county": "Paris", "city": "Paris",
            "landmark": "8e Arrondissement / Fashion Week Venue, Paris",
            "lat": 48.8665, "lng": 2.3145, "precision": "series_locus",
            "notes": "2007年2月法国巴黎高级定制时装周秀场与后台。"
        }

    if project_slug == "broken-manual":
        bm_loc = BROKEN_MANUAL_LOCI[idx_in_project % len(BROKEN_MANUAL_LOCI)]
        return {
            "country": bm_loc[0], "state": bm_loc[1], "stateCode": bm_loc[2],
            "county": bm_loc[3], "city": bm_loc[4],
            "landmark": bm_loc[5],
            "lat": bm_loc[6], "lng": bm_loc[7], "precision": "series_locus",
            "notes": bm_loc[8]
        }

    if project_slug == "advice-for-young-artists":
        col = ADVICE_COLLEGES[idx_in_project % len(ADVICE_COLLEGES)]
        return {
            "country": col[0], "state": col[1], "stateCode": col[2],
            "county": col[3], "city": col[4],
            "landmark": col[5],
            "lat": col[6], "lng": col[7], "precision": "series_locus",
            "notes": col[8]
        }

    # Generic fallback to project defaultLocus
    dl = PROJECT_MAP[project_slug]["defaultLocus"]
    return {
        "country": dl["country"], "state": dl["state"], "stateCode": dl["stateCode"],
        "county": dl["county"], "city": dl["city"],
        "landmark": dl["landmark"],
        "lat": dl["lat"], "lng": dl["lng"], "precision": "series_locus",
        "notes": f"《{PROJECT_MAP[project_slug]['titleZh']}》系列作品拍摄地。"
    }


def main():
    with open(BASE_DIR / "photos.json", "r", encoding="utf-8") as f:
        raw_photos = json.load(f)

    # 1. Deduplicate raw_photos by src within each project and restore titles if duplicated
    for slug, pblock in raw_photos.items():
        seen_src = {}
        deduped = []
        for item in pblock.get("photos", []):
            s = item["src"]
            t = (item.get("title") or "").strip()
            if s not in seen_src:
                seen_src[s] = {"src": s, "title": t}
                deduped.append(seen_src[s])
            else:
                if t and not seen_src[s]["title"]:
                    seen_src[s]["title"] = t
        pblock["photos"] = deduped

    # 2. Build full list of photo nodes across all 11 projects
    all_nodes = []
    coord_counts = {}  # Track (round(lat,3), round(lng,3)) to apply golden-angle micro-offset

    for p_meta in PROJECTS_META:
        slug = p_meta["slug"]
        web_items = raw_photos.get(slug, {}).get("photos", [])

        project_items = []
        idx_counter = 0

        # Add official web items (skipping book covers, installation views & already-appended museum plates)
        for item in web_items:
            src = item["src"]
            title = (item.get("title") or "").strip()
            if "alecsoth.com" not in src:
                continue
            if is_skip_photo(title, src):
                continue

            idx_counter += 1
            yr, mo = parse_year_month(title, src, slug)

            # Give nice default title if empty (e.g., Dog Days Bogotá or Paris/MN)
            if not title:
                fn_code = src.split("/")[-1].replace(".jpg", "").replace("_f", "")
                if slug == "dog-days-bogota":
                    title = f"Untitled #{idx_counter:02d}, Bogotá, Colombia ({fn_code})"
                elif slug == "paris-minnesota":
                    title = f"Paris / Minnesota #{idx_counter:02d} ({fn_code})"
                else:
                    title = f"{p_meta['title']} #{idx_counter:02d}"

            project_items.append({
                "title": title,
                "src": src,
                "year": yr,
                "month": mo,
                "sourceType": "official_web"
            })

        # Add supplemented photobook plates for Sleeping by the Mississippi & Niagara
        for sup in SUPPLEMENTED_PLATES.get(slug, []):
            project_items.append({
                "title": sup["title"],
                "src": sup["src"],
                "year": sup["year"],
                "month": sup["month"],
                "sourceType": sup["sourceType"]
            })

        # Geocode each item in the project
        geocoded_project_nodes = []
        for i, p_item in enumerate(project_items):
            geo = geocode_photo(p_item["title"], p_item["src"], slug, i)

            # Apply deterministic golden-angle micro-jitter if multiple photos share exact coordinates
            base_lat, base_lng = geo["lat"], geo["lng"]
            ckey = (round(base_lat, 3), round(base_lng, 3))
            occurrence = coord_counts.get(ckey, 0)
            coord_counts[ckey] = occurrence + 1

            if occurrence > 0:
                # Golden angle spiral (~137.5 deg), radius 0.0022 deg (~220m) per ring
                angle = occurrence * 2.399963229728653
                radius = 0.0022 * math.sqrt(occurrence)
                lat = round(base_lat + radius * math.cos(angle), 5)
                lng = round(base_lng + (radius * math.sin(angle)) / max(0.3, math.cos(math.radians(base_lat))), 5)
            else:
                lat = round(base_lat, 5)
                lng = round(base_lng, 5)

            precision_labels = {
                "landmark": "精确地标",
                "city": "城镇街区",
                "series_locus": "作品集核心区"
            }
            source_labels = {
                "official_web": "官网高清原作",
                "book_plate": "实体画册补全图版"
            }

            # Parse subject name (part before first comma/period)
            subj = re.split(r"[,.]", p_item["title"])[0].strip()

            node = {
                "id": f"{slug}-{i+1:02d}",
                "projectSlug": slug,
                "projectTitle": p_meta["title"],
                "projectTitleZh": p_meta["titleZh"],
                "projectColor": p_meta["color"],
                "plateNumber": i + 1,
                "title": p_item["title"],
                "subject": subj,
                "year": p_item["year"],
                "month": p_item["month"],
                "dateDisplay": f"{p_item['year']}.{p_item['month']:02d}",
                "country": geo["country"],
                "state": geo["state"],
                "stateCode": geo["stateCode"],
                "county": geo["county"],
                "city": geo["city"],
                "landmark": geo["landmark"],
                "lat": lat,
                "lng": lng,
                "baseLat": round(base_lat, 5),
                "baseLng": round(base_lng, 5),
                "precision": geo["precision"],
                "precisionLabel": precision_labels[geo["precision"]],
                "sourceType": p_item["sourceType"],
                "sourceLabel": source_labels[p_item["sourceType"]],
                "src": p_item["src"],
                "notes": geo["notes"]
            }
            geocoded_project_nodes.append(node)

        # Sort routeOrder:
        # For 'sleeping-by-the-mississippi', sort North -> South (by descending latitude!)
        # For 'niagara', sort West -> East along Lundy's Lane (ON) -> Falls -> Niagara Falls Blvd (NY)
        # For other projects, sort chronologically (year, month, plateNumber)
        if slug == "sleeping-by-the-mississippi":
            route_sorted = sorted(geocoded_project_nodes, key=lambda x: (-x["baseLat"], x["plateNumber"]))
        elif slug == "niagara":
            route_sorted = sorted(geocoded_project_nodes, key=lambda x: (x["baseLng"], x["plateNumber"]))
        else:
            route_sorted = sorted(geocoded_project_nodes, key=lambda x: (x["year"], x["month"], x["plateNumber"]))

        for r_idx, n in enumerate(route_sorted, 1):
            n["routeOrder"] = r_idx

        # Keep route-sorted order for Mississippi so the feed and polyline follow the river North->South
        if slug == "sleeping-by-the-mississippi":
            all_nodes.extend(route_sorted)
        else:
            all_nodes.extend(geocoded_project_nodes)

        # Also update raw_photos[slug]["photos"] so index.html also benefits from deduplication & supplemented plates
        existing_srcs = {p["src"] for p in raw_photos[slug]["photos"]}
        for sup in SUPPLEMENTED_PLATES.get(slug, []):
            if sup["src"] not in existing_srcs:
                raw_photos[slug]["photos"].append({
                    "src": sup["src"],
                    "title": sup["title"]
                })

    # Save cleaned & enriched photos.json
    with open(BASE_DIR / "photos.json", "w", encoding="utf-8") as f:
        json.dump(raw_photos, f, ensure_ascii=False, indent=2)

    # Compute summary stats
    states = sorted({f"{n['state']} ({n['country']})" for n in all_nodes})
    counties = sorted({f"{n['county']}, {n['stateCode']}" for n in all_nodes})
    years = sorted({n["year"] for n in all_nodes})

    atlas_payload = {
        "meta": {
            "totalPhotos": len(all_nodes),
            "totalProjects": len(PROJECTS_META),
            "totalStates": len(states),
            "totalCounties": len(counties),
            "yearMin": min(years),
            "yearMax": max(years)
        },
        "projects": PROJECTS_META,
        "photos": all_nodes
    }

    with open(BASE_DIR / "atlas-data.json", "w", encoding="utf-8") as f:
        json.dump(atlas_payload, f, ensure_ascii=False, indent=2)

    print("=== ATLAS DATA SUMMARY ===")
    print(f"Total Projects: {len(PROJECTS_META)}")
    print(f"Total Geocoded Photos: {len(all_nodes)}")
    print(f"Total States/Provinces: {len(states)}")
    print(f"Total Counties/Districts: {len(counties)}")
    print(f"Year Range: {min(years)} - {max(years)}")
    for p in PROJECTS_META:
        s = p["slug"]
        cnt = sum(1 for n in all_nodes if n["projectSlug"] == s)
        web_cnt = sum(1 for n in all_nodes if n["projectSlug"] == s and n["sourceType"] == "official_web")
        book_cnt = sum(1 for n in all_nodes if n["projectSlug"] == s and n["sourceType"] == "book_plate")
        lm_cnt = sum(1 for n in all_nodes if n["projectSlug"] == s and n["precision"] == "landmark")
        print(f"  - {s:42s}: {cnt:3d} photos (web={web_cnt:2d}, book_sup={book_cnt:2d}, landmark={lm_cnt:2d})")


if __name__ == "__main__":
    main()
