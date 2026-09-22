#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rail-doubao 阶段4 · 补采站点坐标
遍历 routes_pilot 全部经停站，对坐标库缺失/未定位的站用 Nominatim 地理编码补齐。
严格校验：标签首段 == 站名 或 站名+站 / 站名+火车站；逐站 1.1s 节流。
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

UA = "rail-doubao-pilot/1.0 (personal research; nominatim usage)"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
QUERIES = [lambda n: n + "火车站 中国", lambda n: n + "站 中国", lambda n: n + " 中国"]


def strict_ok(label, name):
    if not label:
        return False
    p = label.split(",")[0].strip()
    return p == name or p == name + "站" or p == name + "火车站" or p.startswith(name + "站")


def geocode(name, query):
    url = "https://nominatim.openstreetmap.org/search?q=%s&format=json&limit=5" % urllib.parse.quote(query)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Accept-Language", "zh-CN,zh;q=0.9")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            j = json.load(r)
    except Exception as exc:
        return None, str(exc)
    for hit in j:
        label = hit.get("display_name") or ""
        if strict_ok(label, name):
            return {"lat": float(hit["lat"]), "lon": float(hit["lon"]), "label": label[:90]}, None
    return None, "无严格匹配"


def main():
    routes = json.load(open(os.path.join(DATA_DIR, "routes_pilot.json"), encoding="utf-8"))
    coords = json.load(open(os.path.join(DATA_DIR, "station_coords.json"), encoding="utf-8"))
    names = set()
    for r in routes:
        for st in r["stops"]:
            names.add(st["name"])
    todo = sorted(n for n in names if not (coords.get(n) or {}).get("lat"))
    print("坐标库现有=%d 需补=%d" % (len(coords), len(todo)))
    ok_cnt = 0
    for i, nm in enumerate(todo, 1):
        got = None
        for qf in QUERIES:
            got, err = geocode(nm, qf(nm))
            time.sleep(1.1)
            if got:
                break
        if got:
            got["src"] = "nominatim"; got["verified"] = True
            coords[nm] = got
            ok_cnt += 1
            print("  [%d/%d] OK %s -> %.4f,%.4f" % (i, len(todo), nm, got["lat"], got["lon"]))
        else:
            coords[nm] = {"lat": None, "lon": None, "src": "missing", "verified": False, "note": "严格校验未通过"}
            print("  [%d/%d] MISS %s" % (i, len(todo), nm))
    with open(os.path.join(DATA_DIR, "station_coords.json"), "w", encoding="utf-8") as f:
        json.dump(coords, f, ensure_ascii=False, indent=1)
    still = [k for k, v in coords.items() if v.get("lat") is None]
    print("完成：新增定位=%d 坐标库=%d 仍缺失=%d" % (ok_cnt, len(coords), len(still)))
    print("缺失列表:", sorted(still))


if __name__ == "__main__":
    sys.exit(main())
