#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rail-doubao 阶段2 · 站点坐标库构建（OSM Nominatim 按站单点地理编码）

输入：data/routes_pilot.json 与 data/station_dict.json（四示例站兜底）
输出：data/station_coords.json（{站名: {lat, lon, label, src}}）
原则：按站 1.1s 节流（符合 Nominatim 公共实例使用规范）；失败留空并标记。
"""
import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request

UA = ("rail-doubao-pilot/1.0 (personal research; nominatim usage)")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def geocode(name, query=None):
    q = query or (name + "站")
    url = "https://nominatim.openstreetmap.org/search?q=%s&format=json&limit=1" % urllib.parse.quote(q)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Accept-Language", "zh-CN,zh;q=0.9")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            j = json.load(r)
    except Exception as exc:
        return {"err": str(exc)}
    if j:
        return {"lat": float(j[0]["lat"]), "lon": float(j[0]["lon"]),
                "label": (j[0].get("display_name") or "")[:80]}
    return None


def collect_stations():
    routes = json.load(open(os.path.join(DATA_DIR, "routes_pilot.json"), encoding="utf-8"))
    names = set()
    for r in routes:
        names.add(r["origin"]); names.add(r["dest"])
        names.add(r["station"])
        for st in r["stops"]:
            names.add(st["name"])
    return names, routes


def main():
    names, routes = collect_stations()
    out_path = os.path.join(DATA_DIR, "station_coords.json")
    coords = {}
    if os.path.exists(out_path):
        coords = json.load(open(out_path, encoding="utf-8"))
    print("总站点=%d 已缓存=%d" % (len(names), len(coords)))
    pending = [n for n in names if n not in coords]
    # 冠豸山/冠豸山南 消歧：带市域限定再查
    disambig = {"冠豸山": ["龙岩市冠豸山火车站", "连城县冠豸山站"],
                "冠豸山南": ["连城县冠豸山南站"]}
    for i, nm in enumerate(pending, 1):
        got = None
        for q in (disambig.get(nm) or [nm + "站", nm + "火车站"]):
            got = geocode(nm, q)
            time.sleep(1.1)
            if got and "lat" in got:
                break
        if got and "lat" in got:
            got["src"] = "nominatim"
            coords[nm] = got
            print("  [%d/%d] %s -> (%.4f, %.4f) %s" % (
                i, len(pending), nm, got["lat"], got["lon"], got["label"][:36]))
        else:
            coords[nm] = {"lat": None, "lon": None, "src": "missing",
                          "note": got.get("err") if isinstance(got, dict) and got.get("err") else "未定位"}
            print("  [%d/%d] %s -> 未定位" % (i, len(pending), nm))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(coords, f, ensure_ascii=False, indent=1)
    missing = {k: v for k, v in coords.items() if v.get("lat") is None}
    print("坐标库=%d 条，缺失=%d：%s" % (len(coords), len(missing), list(missing)[:20]))


if __name__ == "__main__":
    sys.exit(main())
