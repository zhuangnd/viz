/**
 * 全球科技与前沿创新企业研发数据集
 * 维度说明:
 * - name: 企业/机构名称
 * - sector: 赛道/领域
 * - rdSpend: 研发投入 (十亿美元)
 * - rdRatio: 研发投入占营收比 (%)
 * - growthRate: 年度营收增长率 (%)
 * - marketCap: 估值/市值 (十亿美元)
 * - employees: 员工规模 (千人)
 * - region: 所在区域
 */
window.VIZ_TECH_DATA = [
  // 人工智能与算力
  { name: "Nvidia", sector: "人工智能与算力", rdSpend: 8.7, rdRatio: 14.3, growthRate: 122.4, marketCap: 2850, employees: 29, region: "北美" },
  { name: "OpenAI", sector: "人工智能与算力", rdSpend: 3.2, rdRatio: 45.8, growthRate: 156.0, marketCap: 86, employees: 1.2, region: "北美" },
  { name: "Anthropic", sector: "人工智能与算力", rdSpend: 1.8, rdRatio: 52.0, growthRate: 180.5, marketCap: 18, employees: 0.5, region: "北美" },
  { name: "TSMC (台积电)", sector: "人工智能与算力", rdSpend: 5.8, rdRatio: 8.5, growthRate: 16.5, marketCap: 780, employees: 76, region: "亚太" },
  { name: "ASML (阿斯麦)", sector: "人工智能与算力", rdSpend: 4.3, rdRatio: 14.8, growthRate: 28.2, marketCap: 370, employees: 42, region: "欧洲" },
  { name: "Broadcom", sector: "人工智能与算力", rdSpend: 5.3, rdRatio: 15.1, growthRate: 34.0, marketCap: 640, employees: 20, region: "北美" },
  { name: "AMD", sector: "人工智能与算力", rdSpend: 5.9, rdRatio: 25.8, growthRate: 12.0, marketCap: 240, employees: 26, region: "北美" },
  { name: "Intel", sector: "人工智能与算力", rdSpend: 16.5, rdRatio: 30.4, growthRate: -14.2, marketCap: 130, employees: 124, region: "北美" },
  { name: "ARM", sector: "人工智能与算力", rdSpend: 1.1, rdRatio: 34.0, growthRate: 21.0, marketCap: 120, employees: 6.5, region: "欧洲" },

  // 生物医药与健康
  { name: "Novo Nordisk (诺和诺德)", sector: "生物医药与健康", rdSpend: 4.8, rdRatio: 14.5, growthRate: 31.2, marketCap: 560, employees: 64, region: "欧洲" },
  { name: "Eli Lilly (礼来)", sector: "生物医药与健康", rdSpend: 9.3, rdRatio: 27.2, growthRate: 29.8, marketCap: 720, employees: 44, region: "北美" },
  { name: "Moderna", sector: "生物医药与健康", rdSpend: 4.8, rdRatio: 71.0, growthRate: -64.0, marketCap: 45, employees: 5.6, region: "北美" },
  { name: "BioNTech", sector: "生物医药与健康", rdSpend: 1.9, rdRatio: 48.0, growthRate: -52.0, marketCap: 22, employees: 4.8, region: "欧洲" },
  { name: "AstraZeneca (阿斯利康)", sector: "生物医药与健康", rdSpend: 10.9, rdRatio: 23.8, growthRate: 15.0, marketCap: 230, employees: 89, region: "欧洲" },
  { name: "Novartis (诺华)", sector: "生物医药与健康", rdSpend: 11.4, rdRatio: 24.6, growthRate: 10.2, marketCap: 210, employees: 78, region: "欧洲" },
  { name: "Roche (罗氏)", sector: "生物医药与健康", rdSpend: 14.8, rdRatio: 22.8, growthRate: 6.5, marketCap: 220, employees: 103, region: "欧洲" },
  { name: "BeiGene (百济神州)", sector: "生物医药与健康", rdSpend: 1.8, rdRatio: 73.5, growthRate: 74.0, marketCap: 16, employees: 10, region: "亚太" },

  // 清洁能源与智能车
  { name: "Tesla", sector: "清洁能源与智能车", rdSpend: 3.9, rdRatio: 4.1, growthRate: 18.8, marketCap: 620, employees: 140, region: "北美" },
  { name: "BYD (比亚迪)", sector: "清洁能源与智能车", rdSpend: 5.5, rdRatio: 6.5, growthRate: 42.0, marketCap: 95, employees: 700, region: "亚太" },
  { name: "CATL (宁德时代)", sector: "清洁能源与智能车", rdSpend: 2.6, rdRatio: 4.6, growthRate: 22.5, marketCap: 110, employees: 116, region: "亚太" },
  { name: "Li Auto (理想汽车)", sector: "清洁能源与智能车", rdSpend: 1.5, rdRatio: 8.6, growthRate: 173.0, marketCap: 32, employees: 31, region: "亚太" },
  { name: "NIO (蔚来)", sector: "清洁能源与智能车", rdSpend: 1.9, rdRatio: 24.5, growthRate: 12.9, marketCap: 9, employees: 32, region: "亚太" },
  { name: "XPeng (小鹏)", sector: "清洁能源与智能车", rdSpend: 0.7, rdRatio: 17.2, growthRate: 14.2, marketCap: 8, employees: 15, region: "亚太" },
  { name: "Enphase Energy", sector: "清洁能源与智能车", rdSpend: 0.2, rdRatio: 8.8, growthRate: -26.0, marketCap: 14, employees: 3.1, region: "北美" },
  { name: "Northvolt", sector: "清洁能源与智能车", rdSpend: 0.6, rdRatio: 58.0, growthRate: 68.0, marketCap: 12, employees: 5.5, region: "欧洲" },

  // 商业航天与前沿制造
  { name: "SpaceX", sector: "商业航天与前沿制造", rdSpend: 3.1, rdRatio: 32.0, growthRate: 85.0, marketCap: 180, employees: 13, region: "北美" },
  { name: "Rocket Lab", sector: "商业航天与前沿制造", rdSpend: 0.12, rdRatio: 42.5, growthRate: 16.0, marketCap: 2.8, employees: 1.8, region: "北美" },
  { name: "Boston Dynamics", sector: "商业航天与前沿制造", rdSpend: 0.35, rdRatio: 65.0, growthRate: 35.0, marketCap: 4.5, employees: 0.9, region: "北美" },
  { name: "Intuitive Machines", sector: "商业航天与前沿制造", rdSpend: 0.08, rdRatio: 38.0, growthRate: 110.0, marketCap: 0.9, employees: 0.4, region: "北美" },
  { name: "DJI (大疆)", sector: "商业航天与前沿制造", rdSpend: 1.4, rdRatio: 25.0, growthRate: 20.0, marketCap: 26, employees: 14, region: "亚太" },

  // 消费科技与数字云
  { name: "Microsoft", sector: "消费科技与数字云", rdSpend: 27.2, rdRatio: 12.8, growthRate: 15.7, marketCap: 3100, employees: 221, region: "北美" },
  { name: "Apple", sector: "消费科技与数字云", rdSpend: 29.9, rdRatio: 7.8, growthRate: -2.8, marketCap: 3300, employees: 161, region: "北美" },
  { name: "Alphabet (Google)", sector: "消费科技与数字云", rdSpend: 45.4, rdRatio: 14.8, growthRate: 13.5, marketCap: 2150, employees: 182, region: "北美" },
  { name: "Meta", sector: "消费科技与数字云", rdSpend: 38.5, rdRatio: 28.5, growthRate: 16.0, marketCap: 1250, employees: 67, region: "北美" },
  { name: "Amazon", sector: "消费科技与数字云", rdSpend: 85.6, rdRatio: 14.9, growthRate: 11.8, marketCap: 1920, employees: 1525, region: "北美" },
  { name: "Tencent (腾讯)", sector: "消费科技与数字云", rdSpend: 9.1, rdRatio: 10.4, growthRate: 9.8, marketCap: 450, employees: 105, region: "亚太" },
  { name: "Alibaba (阿里巴巴)", sector: "消费科技与数字云", rdSpend: 7.4, rdRatio: 5.7, growthRate: 5.2, marketCap: 190, employees: 219, region: "亚太" },
  { name: "Huawei (华为)", sector: "消费科技与数字云", rdSpend: 22.8, rdRatio: 23.4, growthRate: 9.6, marketCap: 160, employees: 207, region: "亚太" },
  { name: "Spotify", sector: "消费科技与数字云", rdSpend: 1.8, rdRatio: 13.0, growthRate: 13.0, marketCap: 65, employees: 8.5, region: "欧洲" },
  { name: "SAP", sector: "消费科技与数字云", rdSpend: 6.8, rdRatio: 21.0, growthRate: 6.0, marketCap: 230, employees: 107, region: "欧洲" }
];

window.VIZ_SECTORS = [
  "人工智能与算力",
  "生物医药与健康",
  "清洁能源与智能车",
  "商业航天与前沿制造",
  "消费科技与数字云"
];

window.VIZ_SECTOR_COLORS = {
  "人工智能与算力": "#2563EB",
  "生物医药与健康": "#059669",
  "清洁能源与智能车": "#D97706",
  "商业航天与前沿制造": "#7C3AED",
  "消费科技与数字云": "#DB2777"
};
