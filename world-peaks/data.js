const peaksData = [
  {
    id: "everest",
    nameZh: "珠穆朗玛峰",
    nameEn: "Mount Everest",
    elevation: 8848,
    country: "尼泊尔 / 中国",
    firstAscentTime: "1953年5月29日",
    firstAscenders: "埃德蒙·希拉里(新西兰), 丹增·诺盖(尼泊尔)",
    categories: ["top10", "seven"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/e/e7/Everest_North_Face_toward_Base_Camp_Tibet_Luca_Galuzzi_2006.jpg"
  },
  {
    id: "k2",
    nameZh: "乔戈里峰",
    nameEn: "K2",
    elevation: 8611,
    country: "巴基斯坦 / 中国",
    firstAscentTime: "1954年7月31日",
    firstAscenders: "阿基莱·孔帕尼奥尼(意大利), 里诺·拉切德利(意大利)",
    categories: ["top10"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/1/12/K2_2006b.jpg"
  },
  {
    id: "kangchenjunga",
    nameZh: "干城章嘉峰",
    nameEn: "Kangchenjunga",
    elevation: 8586,
    country: "尼泊尔 / 印度",
    firstAscentTime: "1955年5月25日",
    firstAscenders: "乔·布朗(英国), 乔治·班德(英国)",
    categories: ["top10"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/3/35/Kangchenjunga.JPG"
  },
  {
    id: "lhotse",
    nameZh: "洛子峰",
    nameEn: "Lhotse",
    elevation: 8516,
    country: "尼泊尔 / 中国",
    firstAscentTime: "1956年5月18日",
    firstAscenders: "恩斯特·赖斯(瑞士), 弗里茨·卢赫辛格(瑞士)",
    categories: ["top10"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/3/38/LhotseMountain.jpg"
  },
  {
    id: "makalu",
    nameZh: "马卡鲁峰",
    nameEn: "Makalu",
    elevation: 8485,
    country: "尼泊尔 / 中国",
    firstAscentTime: "1955年5月15日",
    firstAscenders: "莱昂内尔·泰瑞(法国), 让·库齐(法国)",
    categories: ["top10"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/1/19/Makalu.jpg"
  },
  {
    id: "cho-oyu",
    nameZh: "卓奥友峰",
    nameEn: "Cho Oyu",
    elevation: 8188,
    country: "尼泊尔 / 中国",
    firstAscentTime: "1954年10月19日",
    firstAscenders: "赫伯特·蒂奇(奥地利), 约瑟夫·约赫勒(奥地利), 帕桑·达瓦·喇嘛(尼泊尔)",
    categories: ["top10"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/1/1c/ChoOyu-fromGokyo.jpg"
  },
  {
    id: "dhaulagiri",
    nameZh: "道拉吉里峰",
    nameEn: "Dhaulagiri",
    elevation: 8167,
    country: "尼泊尔",
    firstAscentTime: "1960年5月13日",
    firstAscenders: "库尔特·丁伯格(奥地利) 等",
    categories: ["top10"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/4/46/Dhaulagiri_mountain.jpg"
  },
  {
    id: "manaslu",
    nameZh: "马纳斯鲁峰",
    nameEn: "Manaslu",
    elevation: 8163,
    country: "尼泊尔",
    firstAscentTime: "1956年5月9日",
    firstAscenders: "今西寿雄(日本), 嘉增诺布(尼泊尔)",
    categories: ["top10"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/e/e0/Sunrise%2C_Manaslu.jpg"
  },
  {
    id: "nanga-parbat",
    nameZh: "南迦帕尔巴特峰",
    nameEn: "Nanga Parbat",
    elevation: 8126,
    country: "巴基斯坦",
    firstAscentTime: "1953年7月3日",
    firstAscenders: "赫尔曼·布尔(奥地利)",
    categories: ["top10"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/c/c5/Nanga_Parbat_View_from_Fairy_Meadow_Rupal_Valley.jpg"
  },
  {
    id: "annapurna",
    nameZh: "安纳布尔纳峰",
    nameEn: "Annapurna I",
    elevation: 8091,
    country: "尼泊尔",
    firstAscentTime: "1950年6月3日",
    firstAscenders: "莫里斯·埃尔佐格(法国), 路易·拉什纳尔(法国)",
    categories: ["top10"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/3/30/Annapurna_South_Face_Nepal.jpg"
  },
  {
    id: "aconcagua",
    nameZh: "阿空加瓜峰",
    nameEn: "Aconcagua",
    elevation: 6960,
    country: "阿根廷",
    firstAscentTime: "1897年1月14日",
    firstAscenders: "马蒂亚斯·楚尔布里根(瑞士)",
    categories: ["seven"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/4/4e/Aconcagua2016.jpg"
  },
  {
    id: "denali",
    nameZh: "迪纳利峰",
    nameEn: "Denali",
    elevation: 6190,
    country: "美国",
    firstAscentTime: "1913年6月7日",
    firstAscenders: "哈德森·斯塔克(美国) 等",
    categories: ["seven"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/9/91/Wonder_Lake_and_Denali.jpg"
  },
  {
    id: "kilimanjaro",
    nameZh: "乞力马扎罗山",
    nameEn: "Mount Kilimanjaro",
    elevation: 5895,
    country: "坦桑尼亚",
    firstAscentTime: "1889年10月6日",
    firstAscenders: "汉斯·迈耶(德国), 路德维希·普尔切勒(奥地利)",
    categories: ["seven"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/6/6b/Mt._Kilimanjaro_12.2006.JPG"
  },
  {
    id: "elbrus",
    nameZh: "厄尔布鲁士峰",
    nameEn: "Mount Elbrus",
    elevation: 5642,
    country: "俄罗斯",
    firstAscentTime: "1874年",
    firstAscenders: "弗洛伦斯·克劳福德·格罗夫(英国) 等",
    categories: ["seven"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/d/d4/Elbrus_from_Cheget_over_Donguz_Orun_lake.jpg"
  },
  {
    id: "vinson",
    nameZh: "文森峰",
    nameEn: "Vinson Massif",
    elevation: 4892,
    country: "南极洲",
    firstAscentTime: "1966年12月18日",
    firstAscenders: "尼古拉斯·克林奇(美国) 等",
    categories: ["seven"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/c/c6/Mount_Vinson_from_camp_3.jpg"
  },
  {
    id: "puncak-jaya",
    nameZh: "查亚峰",
    nameEn: "Puncak Jaya",
    elevation: 4884,
    country: "印度尼西亚",
    firstAscentTime: "1962年2月13日",
    firstAscenders: "海因里希·哈勒(奥地利) 等",
    categories: ["seven"],
    photoUrl: "https://upload.wikimedia.org/wikipedia/commons/2/29/Puncak_Jaya.jpg"
  }
];

window.peaksData = peaksData;
