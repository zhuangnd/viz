#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rail-doubao 阶段2 · 站点坐标严格校验 v2
规则：标签首段（第一个逗号前）必须 == 站名 或 站名+"站" 或 站名+"火车站"；否则判定错位，
     以 站名+"火车站" 等限定词重查；仍不符则 lat=None（页面将按“未定位”处理，不绘制错点）。
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

QUERY_POOL = [
    lambda n: n + "火车站", lambda n: n + "站", lambda n: n + "火车站 中国",
]


def strict_ok(label, name):
    if not label:
        return False
    primary = label.split(",")[0].strip()
    if primary == name or primary == name + "站" or primary == name + "火车站":
        return True
    if primary.startswith(name + "站"):
        return True
    return False


def geocode(name, query):
    url = "https://nominatim.openstreetmap.org/search?q=%s&format=json&limit=4" % urllib.parse.quote(query)
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
    path = os.path.join(DATA_DIR, "station_coords.json")
    coords = json.load(open(path, encoding="utf-8"))
    fixed = ok = 0
    requery = []
    for nm, v in coords.items():
        if v.get("lat") is None:
            requery.append(nm)
            continue
        if strict_ok(v.get("label") or "", nm):
            v["verified"] = True
            ok += 1
            continue
        v["verified"] = False
        requery.append(nm)
    print("严格通过=%d 需重查=%d" % (ok, len(requery)))
    for i, nm in enumerate(requery, 1):
        got = None
        for qf in QUERY_POOL:
            got, err = geocode(nm, qf(nm))
            time.sleep(1.1)
            if got:
                break
        if got:
            got["src"] = "nominatim"; got["verified"] = True
            coords[nm] = got
            fixed += 1
            print("  [%d/%d] 重查成功 %s -> %.4f,%.4f | %s" % (
                i, len(requery), nm, got["lat"], got["lon"], got["label"][:44]))
        else:
            coords[nm] = {"lat": None, "lon": None, "src": "missing", "verified": False,
                          "note": "严格校验未通过"}
            print("  [%d/%d] 未定位 %s" % (i, len(requery), nm))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(coords, f, ensure_ascii=False, indent=1)
    missing = {k: v for k, v in coords.items() if v.get("lat") is None}
    print("总计=%d 通过=%d 重查修复=%d 缺失=%d：%s" % (
        len(coords), ok, fixed, len(missing), list(missing)))


if __name__ == "__main__":
    sys.exit(main())
