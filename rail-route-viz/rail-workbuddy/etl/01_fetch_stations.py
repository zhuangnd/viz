# -*- coding: utf-8 -*-
"""P1 车站主数据：12306 电报码 + GCJ-02 经纬度 合并为 stations.json"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rail_common import DATA, RAW, dump_json, new_session  # noqa: E402

TARGETS = ["厦门", "厦门北", "冠豸山", "冠豸山南"]
STATION_JS_URL = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"


def main():
    s = new_session()
    cache = os.path.join(RAW, "station_name.js")
    if os.path.exists(cache):
        txt = open(cache, encoding="utf-8").read()
    else:
        r = s.get(STATION_JS_URL, timeout=25)
        r.encoding = "utf-8"
        txt = r.text
        open(cache, "w", encoding="utf-8").write(txt)
    print("station_name.js 字节:", len(txt))

    entries = txt.rstrip(";").split("'")[1].split("@")[1:]
    stations = {}
    for e in entries:
        p = e.split("|")
        if len(p) < 3:
            continue
        name, telecode = p[1], p[2]
        if not telecode or telecode in stations.values():
            continue
        stations[name] = telecode
    print("12306 车站数:", len(stations))

    geo = json.load(open(os.path.join(RAW, "station_geo_gcj02.json"), encoding="utf-8"))
    print("坐标表车站数:", len(geo))

    out = {}
    missing = []
    for name, telecode in stations.items():
        g = geo.get(name)
        rec = {"telecode": telecode, "name": name}
        if g and len(g) == 2:
            rec["lng"], rec["lat"] = float(g[0]), float(g[1])
            rec["coord_source"] = "dataset"
        else:
            rec["lng"] = rec["lat"] = None
            rec["coord_source"] = "missing"
            missing.append(name)
        out[telecode] = rec

    dump_json(os.path.join(DATA, "stations.json"), out)
    print(f"\n合并完成: {len(out)} 站, 缺坐标 {len(missing)} 站")

    print("\n--- 目标站 ---")
    for t in TARGETS:
        rec = next((v for v in out.values() if v["name"] == t), None)
        print(f"  {t:<6} {rec}")

    print("\n--- 缺坐标的站（前 40） ---")
    print("  " + ", ".join(missing[:40]))
    if len(missing) > 40:
        print(f"  ... 共 {len(missing)} 个")


if __name__ == "__main__":
    main()
