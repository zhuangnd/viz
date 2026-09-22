#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rail-doubao 阶段3 · 构建地图可视化页面
- 读取 data/web_data.json，为每条线路补充 stop_count
- 将数据 JSON 注入模板 __DATA_JSON__ 占位
- 输出 web/高铁动车路线图-厦门北试点.html
"""
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")
TPL = os.path.join(WEB_DIR, "高铁动车路线图.template.html")
OUT = os.path.join(WEB_DIR, "rail-map.html")


def main():
    data = json.load(open(os.path.join(BASE_DIR, "data", "web_data.json"), encoding="utf-8"))
    for hub, rs in data["by_hub"].items():
        for r in rs:
            r["stop_count"] = len(r["stops"])
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    html = open(TPL, encoding="utf-8").read()
    assert "__DATA_JSON__" in html, "模板缺少数据占位"
    html = html.replace("__DATA_JSON__", payload)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK ->", OUT, "%.1f KB" % (os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    sys.exit(main())
