#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rail-doubao 阶段5 · 四枢纽方向覆盖扩采
- 厦门北(XKS)：30 出向 + 30 入向（华北/华东/华南/西南/西北主要城市）
- 厦门(XMS)：16 出向 + 16 入向
- 冠豸山(GPS)/冠豸山南(GSS)：各 6 出向 + 6 入向
- 途经补充（经厦门北/厦门的跨区长线）：南昌西/长沙南/武汉/杭州东/上海虹桥/北京南 → 深圳北
统一日期 2026-09-23；queryG 取该方向全部车次；经停按 train_no 缓存复用；
合并进 data/routes_pilot.json（按 train_no+seg_to 去重）。
原则：低频节流（复用 collect_pilot 的 3s+随机），仅个人/内部研究。
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import collect_pilot as cp

# 阶段4 实测 1.1-1.2s 节流可用；为控制总时长，覆盖模块默认 3s 节流
cp.SLEEP_BASE = 1.2

DATE = "2026-09-23"

XKS = "厦门北"; XMS = "厦门"; GPS = "冠豸山"; GSS = "冠豸山南"

# 代表方向（电报码）
DIRS_BIG = ["VNP", "AOH", "IZQ", "IOQ", "HGH", "NKG", "ENH", "JGK", "QHK",
            "NXG", "CWQ", "WHN", "ZAF", "EAY", "ICW", "CXW", "KQW", "KOM",
            "NFZ", "FZS", "LYS", "GZG", "QYS", "ZUS", "VRH", "NGH", "OHH",
            "WGH", "ITH", "LAJ"]
DIRS_MID = ["VNP", "AOH", "IZQ", "IOQ", "HGH", "NXG", "CWQ", "WHN", "ZAF",
            "EAY", "ICW", "CXW", "KQW", "KOM", "NFZ", "FZS"]
DIRS_SMALL = ["IZQ", "IOQ", "NXG", "LYS", "GZG", "XKS"]
# 途经补充：跨区 OD 经停厦门北/厦门
DIRS_PASS = [("NXG", "IOQ"), ("CWQ", "IOQ"), ("WHN", "IOQ"), ("HGH", "IOQ"),
             ("AOH", "IOQ"), ("VNP", "IOQ")]


def build_ods():
    ods = []
    for hub_code, hub_name, dirs in ((cp.D2 and "XKS", XKS, DIRS_BIG),
                                     ("XMS", XMS, DIRS_MID),
                                     ("GPS", GPS, DIRS_SMALL),
                                     ("GSS", GSS, DIRS_SMALL)):
        for to in dirs:
            if to == hub_code:
                continue
            ods.append((hub_code, to, DATE, "%s→%s" % (hub_name, cp.D2.get(to, to))))
            ods.append((to, hub_code, DATE, "%s→%s" % (cp.D2.get(to, to), hub_name)))
    for frm, to in DIRS_PASS:
        ods.append((frm, to, DATE, "途经补充 %s→%s" % (cp.D2.get(frm, frm), cp.D2.get(to, to))))
    return ods


def main():
    cp.log("=== 阶段5 方向覆盖扩采（OD=%d，%s）===" % (len(build_ods()), DATE))
    opener, _cj = cp.make_opener()
    cp.fetch(opener, "%s/otn/czxx/init?station_code=XKS&station_name=%s" % (
        cp.ROOT, cp.urllib.parse.quote("厦门北")), is_json=False)
    cp.pause()

    existing = json.load(open(os.path.join(cp.DATA_DIR, "routes_pilot.json"), encoding="utf-8"))
    seen = {(r["train_no"], r["seg_to"]) for r in existing}
    added = 0
    skipped_dup = 0
    for frm, to, date, note in build_ods():
        cp.log("OD %s→%s（%s）" % (cp.D2.get(frm, frm), cp.D2.get(to, to), note))
        rows = cp.queryG(opener, frm, to, date)
        if not rows:
            continue
        for line in rows:
            r = cp.parse_row(line)
            if not r:
                continue
            key = (r["train_no"], r["seg_to"])
            if key in seen:
                skipped_dup += 1
                continue
            stops = cp.schedule(opener, r)
            if not stops:
                continue
            f_name = cp.D2.get(r["seg_from"], r["seg_from"])
            t_name = cp.D2.get(r["seg_to"], r["seg_to"])
            f = next((s for s in stops if s["name"] == f_name), None)
            t = next((s for s in stops if s["name"] == t_name), None)
            existing.append({
                "code": r["code"], "train_no": r["train_no"], "date": date,
                "origin": cp.D2.get(r["start_telecode"]), "dest": cp.D2.get(r["end_telecode"]),
                "origin_code": r["start_telecode"], "dest_code": r["end_telecode"],
                "station": cp.D2.get(frm, frm), "station_code": frm,
                "role": cp.role_of(r, frm),
                "seg_from": f_name, "seg_to": t_name,
                "seg_depart": (f or {}).get("depart"), "seg_arrive": (t or {}).get("arrive"),
                "lishi": r["lishi"], "stop_count": len(stops),
                "stops": stops,
            })
            seen.add(key)
            added += 1
        cp.pause()

    cp.save("routes_pilot.json", existing)
    cp.log("=== 完成：新增=%d 累计=%d 跳过重复=%d ===" % (added, len(existing), skipped_dup))
    hubs = {}
    for r in existing:
        hubs.setdefault(r["origin"], 0)
    from collections import Counter
    by_origin = Counter(r["origin"] for r in existing)
    for k in ("厦门北", "厦门", "冠豸山", "冠豸山南"):
        cp.log("  起点=%s 线路=%d" % (k, by_origin.get(k, 0)))


if __name__ == "__main__":
    sys.exit(main())
