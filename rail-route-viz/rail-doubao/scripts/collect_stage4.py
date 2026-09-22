#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rail-doubao 阶段4 · 四示例站数据覆盖补采
- 冠豸山(GPS)/冠豸山南(GSS) 方向：GPS→龙岩/厦门北、GSS→龙岩/赣州/厦门北
- 厦门(XMS) 途经样本：深圳北→福州、福州→深圳北（途经厦门/厦门北）
- 厦门始发样本：厦门→福州
每 OD 最多取 8 个车次，节流 3s+随机；产物并入 data/routes_pilot.json（按 train_no+seg_to 去重）。
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import collect_pilot as cp

ODS = [
    ("GPS", "LYS", "2026-09-23", "冠豸山→龙岩（GPS 直查验证）"),
    ("GPS", "XKS", "2026-09-23", "冠豸山→厦门北（GPS 直查验证）"),
    ("GSS", "LYS", "2026-09-23", "冠豸山南→龙岩"),
    ("GSS", "GZG", "2026-09-23", "冠豸山南→赣州"),
    ("GSS", "XKS", "2026-09-23", "冠豸山南→厦门北"),
    ("IOQ", "FZS", "2026-09-23", "深圳北→福州（厦门/厦门北 途经样本）"),
    ("FZS", "IOQ", "2026-09-23", "福州→深圳北（厦门/厦门北 途经样本）"),
    ("XMS", "FZS", "2026-09-23", "厦门→福州（厦门 始发样本）"),
]
MAX_PER_OD = 8


def main():
    cp.log("=== 阶段4 四示例站覆盖补采 ===")
    opener, _cj = cp.make_opener()
    cp.fetch(opener, "%s/otn/czxx/init?station_code=XKS&station_name=%s" % (
        cp.ROOT, cp.urllib.parse.quote("厦门北")), is_json=False)
    cp.pause()

    existing = json.load(open(os.path.join(cp.DATA_DIR, "routes_pilot.json"), encoding="utf-8"))
    seen = {(r["train_no"], r["seg_to"]) for r in existing}
    added = 0
    for frm, to, date, note in ODS:
        cp.log("OD %s→%s @%s（%s）" % (cp.D2.get(frm, frm), cp.D2.get(to, to), date, note))
        rows = cp.queryG(opener, frm, to, date)
        for line in rows[:MAX_PER_OD]:
            r = cp.parse_row(line)
            if not r:
                continue
            key = (r["train_no"], r["seg_to"])
            if key in seen:
                cp.log("  跳过重复 %s" % r["code"])
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
    cp.log("=== 完成：新增线路=%d 累计=%d ===" % (added, len(existing)))
    for r in existing:
        if r["date"] == "2026-09-23" and (r["station"] in ("冠豸山", "冠豸山南", "厦门")
                                          or r["seg_from"] in ("深圳北", "福州")):
            cp.log("  [%s] %s %s→%s 本段%s→%s 经停%d站" % (
                r["role"], r["code"], r["origin"], r["dest"], r["seg_from"], r["seg_to"], r["stop_count"]))


if __name__ == "__main__":
    sys.exit(main())
