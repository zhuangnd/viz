#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rail-doubao 阶段2 · 生成页面数据 web_data.json（v2）

- 坐标过滤：孤立点规则——某站坐标若与同线路任一已定位站距离 > 300km 视为错位剔除（防同名误配，且不会级联误删）
- 已知误配站（裸名查询产物）显式剔除：龙山镇/横店/永泰/鄱阳/尤溪/仙居
- 角色重算：按枢纽站（四示例站之一）判定 始发/终到/途经
- 按枢纽分组：by_hub[S] = 途经/始发/终到该站的全部线路（hub ∈ 起讫或经停）
"""
import json
import math
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MAX_ISO_KM = 300.0

# 裸名查询产物中确认错位（与线路地理区域不符）的站
KNOWN_WRONG = {"龙山镇", "横店", "永泰", "鄱阳", "尤溪", "仙居", "涵江"}


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def main():
    routes = json.load(open(os.path.join(DATA_DIR, "routes_pilot.json"), encoding="utf-8"))
    coords = json.load(open(os.path.join(DATA_DIR, "station_coords.json"), encoding="utf-8"))
    sdict = json.load(open(os.path.join(DATA_DIR, "station_dict.json"), encoding="utf-8"))

    # 1) 显式剔除已知误配
    for nm in KNOWN_WRONG:
        if nm in coords:
            coords[nm] = {"lat": None, "lon": None, "src": "excluded", "verified": False,
                          "note": "地理编码错位（已知误配，显式剔除）"}

    # 2) 孤立点过滤：错位坐标与同线路任何已定位站距离均 > 300km → 剔除
    located = {n for n, v in coords.items() if v.get("lat") is not None}
    for r in routes:
        pts = [(st["name"], (coords.get(st["name"]) or {}).get("lat"),
                (coords.get(st["name"]) or {}).get("lon")) for st in r["stops"]]
        for nm, lat, lon in pts:
            if lat is None:
                continue
            dmin = min((haversine(lat, lon, l2, o2) for n2, l2, o2 in pts
                        if n2 != nm and l2 is not None), default=None)
            if dmin is not None and dmin > MAX_ISO_KM:
                coords[nm] = {"lat": None, "lon": None, "src": "excluded", "verified": False,
                              "note": "与同线路最近定位站 %.0fkm，孤立点剔除" % dmin}
                located.discard(nm)

    stations = {n: {"lat": v["lat"], "lon": v["lon"], "label": (v.get("label") or "")[:60]}
                for n, v in coords.items() if v.get("lat") is not None}

    examples = ["厦门北", "厦门", "冠豸山", "冠豸山南"]
    ex_codes = {}
    for s in examples:
        ent = sdict.get(s)
        ex_codes[s] = ent["code"] if ent else None

    # 3) 精简线路数据（含折线），同一车次多条 OD 记录按车次去重（保留首见）
    slim, seen_code = [], set()
    for r in routes:
        if r["code"] in seen_code:
            continue
        seen_code.add(r["code"])
        stops = r["stops"]
        poly = [{"name": st["name"],
                 "lat": (coords.get(st["name"]) or {}).get("lat"),
                 "lon": (coords.get(st["name"]) or {}).get("lon")} for st in stops]
        slim.append({
            "code": r["code"], "train_no": r["train_no"], "date": r["date"],
            "origin": r["origin"], "dest": r["dest"],
            "origin_code": r.get("origin_code"), "dest_code": r.get("dest_code"),
            "seg_from": r["seg_from"], "seg_to": r["seg_to"],
            "seg_depart": r["seg_depart"], "seg_arrive": r["seg_arrive"],
            "lishi": r["lishi"], "stops": stops, "polyline": poly,
        })

    # 4) 按枢纽分组 + 角色重算 + 组内车次去重（优先保留本段含枢纽的记录）
    by_hub, hub_stats = {}, {}
    for s in examples:
        code = ex_codes[s]
        items, seen_hub = [], set()
        for r in slim:
            names = {st["name"] for st in r["stops"]}
            if not (s in names or r["origin"] == s or r["dest"] == s):
                continue
            if r["code"] in seen_hub:
                continue
            # 角色：以枢纽站电报码为准
            oc, dc = r.get("origin_code"), r.get("dest_code")
            if code and oc == code:
                role = "始发"
            elif code and dc == code:
                role = "终到"
            else:
                role = "途经"
            # 若本段记录不覆盖枢纽，换一条同车次覆盖枢纽的记录（保持列表时刻口径）
            cur = {**r, "role": role}
            if cur["seg_from"] != s and cur["seg_to"] != s:
                for r2 in slim:
                    if r2["code"] != r["code"]:
                        continue
                    names2 = {st["name"] for st in r2["stops"]}
                    if not (s in names2 or r2["origin"] == s or r2["dest"] == s):
                        continue
                    oc2, dc2 = r2.get("origin_code"), r2.get("dest_code")
                    role2 = "始发" if (code and oc2 == code) else ("终到" if (code and dc2 == code) else "途经")
                    cur = {**r2, "role": role2}
                    break
            items.append(cur)
            seen_hub.add(r["code"])
        items.sort(key=lambda x: (x["seg_depart"] or "99:99"))
        by_hub[s] = items
        hub_stats[s] = {"count": len(items),
                        "始发": sum(1 for x in items if x["role"] == "始发"),
                        "终到": sum(1 for x in items if x["role"] == "终到"),
                        "途经": sum(1 for x in items if x["role"] == "途经")}

    meta = {
        "title": "高铁动车路线图",
        "hub_default": "厦门北",
        "examples": examples,
        "data_time": "2026-09-22 / 2026-09-23（多方向实测）",
        "source": "12306 leftTicket/queryG + czxx/queryByTrainNo 实时",
        "coord_source": "OSM Nominatim 按站地理编码，经孤立点距离校验；未定位站不绘制坐标",
        "disclaimer": "演示数据：线路为相邻已定位站点连线示意；未定位中间站显示于经停表但不落图。",
        "coverage": "厦门北/厦门 ⇄ 京沪广深杭宁济青昌长武郑西成渝昆筑邕福泉漳龙赣 等主要方向；冠豸山(南)⇄ 广深赣龙厦；途经补充 长线经停样本",
    }
    web = {"meta": meta, "stations": stations, "by_hub": by_hub,
           "hub_stats": hub_stats, "codes": ex_codes}
    with open(os.path.join(DATA_DIR, "web_data.json"), "w", encoding="utf-8") as f:
        json.dump(web, f, ensure_ascii=False, indent=1)

    allnames = {st["name"] for r in slim for st in r["stops"]}
    missing = sorted(allnames - set(stations))
    print("站点(已定位)=%d | 线路=%d | 未定位=%d" % (len(stations), len(slim), len(missing)))
    print("枢纽统计:", json.dumps(hub_stats, ensure_ascii=False))
    print("未定位站:", missing[:60])


if __name__ == "__main__":
    sys.exit(main())
