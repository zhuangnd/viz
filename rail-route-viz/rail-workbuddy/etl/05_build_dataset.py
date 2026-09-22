# -*- coding: utf-8 -*-
"""P4/P5 派生计算 + 生成前端数据集。

输入: data/schedules_raw.json (原始 czxx 返回), data/stations.json, data/candidates.json
输出: data/app_data.json
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rail_common import DATA, dump_json, haversine_km, load_json, parse_hhmm, parse_stopover  # noqa: E402

TARGETS = {"厦门": "XMS", "厦门北": "XKS", "冠豸山": "GPS", "冠豸山南": "GSS"}
TARGET_TC = set(TARGETS.values())
DATE = os.environ.get("RAIL_DATE", "2026-09-22")


def norm(name):
    return (name or "").replace(" ", "").strip()


def compute_abs(stops):
    """为每站补 arrive_abs/depart_abs（自始发日 0 点起的分钟），保证单调递增。"""
    cur_day = 0
    prev = None
    for st in stops:
        a = st["_a"]
        d = st["_d"]
        if a is not None:
            cand = cur_day * 1440 + a
            guard = 0
            while prev is not None and cand < prev and guard < 5:
                cur_day += 1
                cand = cur_day * 1440 + a
                guard += 1
            st["a_abs"] = cand
            prev = cand
        if d is not None:
            cand = cur_day * 1440 + d
            guard = 0
            while prev is not None and cand < prev and guard < 5:
                cur_day += 1
                cand = cur_day * 1440 + d
                guard += 1
            st["d_abs"] = cand
            prev = cand
        st["day"] = cur_day
    return stops


def main():
    stations = load_json(os.path.join(DATA, "stations.json"))
    name_to_tc = {norm(v["name"]): k for k, v in stations.items()}
    raw = load_json(os.path.join(DATA, "schedules_raw.json"))
    cands = {c["train_no"]: c for c in load_json(os.path.join(DATA, "candidates.json"))}

    print("原始车次:", len(raw))
    hit_trains = []
    involved = Counter()
    missing_coord = Counter()

    for tn, rows in raw.items():
        if not rows:
            continue
        stops = []
        for r in rows:
            nm = norm(r.get("station_name"))
            if not nm:
                continue
            tc = name_to_tc.get(nm)
            st = stations.get(tc, {}) if tc else {}
            stops.append({
                "no": r.get("station_no"),
                "name": nm,
                "tc": tc,
                "a": r.get("arrive_time") if r.get("arrive_time") != "----" else None,
                "d": r.get("start_time") if r.get("start_time") != "----" else None,
                "s": parse_stopover(r.get("stopover_time")),
                "_a": parse_hhmm(r.get("arrive_time")),
                "_d": parse_hhmm(r.get("start_time")),
                "lng": st.get("lng"),
                "lat": st.get("lat"),
            })
        if not stops:
            continue

        tcs = {s["tc"] for s in stops if s["tc"]}
        hits_tc = tcs & TARGET_TC
        if not hits_tc:
            continue

        for s in stops:
            involved[s["name"]] += 1
            if s["lng"] is None:
                missing_coord[s["name"]] += 1

        compute_abs(stops)
        base = stops[0].get("d_abs") or stops[0].get("a_abs") or 0

        out_stops = []
        cum_km = 0.0
        for i, s in enumerate(stops):
            seg_min = None
            if s.get("a_abs") is not None and i > 0:
                pd = stops[i - 1].get("d_abs")
                if pd is not None:
                    seg_min = s["a_abs"] - pd
            seg_km = 0.0
            if i > 0 and s["lng"] is not None and stops[i - 1]["lng"] is not None:
                seg_km = haversine_km(stops[i - 1]["lng"], stops[i - 1]["lat"],
                                      s["lng"], s["lat"])
            cum_km += seg_km
            ref = s.get("a_abs") if s.get("a_abs") is not None else s.get("d_abs")
            out_stops.append({
                "no": s["no"], "name": s["name"],
                "arrive": s["a"], "depart": s["d"], "stopover_min": s["s"],
                "seg_min": seg_min,
                "cum_min": (ref - base) if ref is not None else None,
                "seg_km": round(seg_km, 1),
                "cum_km": round(cum_km, 1),
                "day": s.get("day", 0),
                "lng": s["lng"], "lat": s["lat"],
            })

        hits = []
        for s in stops:
            if s["tc"] in TARGET_TC:
                idx = stops.index(s)
                last = len(stops) - 1
                if idx == 0:
                    role = "origin"
                elif idx == last:
                    role = "terminus"
                else:
                    role = "pass"
                hits.append({
                    "target": s["tc"], "role": role,
                    "arrive": s["a"], "depart": s["d"],
                    "stopover_min": s["s"], "no": s["no"],
                    "cum_min": out_stops[idx]["cum_min"],
                })

        cand = cands.get(tn, {})
        code = (rows[0].get("station_train_code") or cand.get("train_code") or "?")
        cls_name = rows[0].get("train_class_name") or ""
        total_ref = out_stops[-1]["cum_min"]
        hit_trains.append({
            "train_no": tn,
            "code": code,
            "cls": code[:1] if code else "?",
            "cls_name": cls_name,
            "origin": stops[0]["name"],
            "terminus": stops[-1]["name"],
            "total_min": total_ref,
            "total_km": round(cum_km, 1),
            "stop_count": len(stops),
            "hits": hits,
            "stops": out_stops,
        })

    print("命中目标站的车次:", len(hit_trains))
    by_target = Counter()
    by_role = Counter()
    for t in hit_trains:
        for h in t["hits"]:
            by_target[h["target"]] += 1
            by_role[(h["target"], h["role"])] += 1
    for tc in TARGET_TC:
        nm = stations[tc]["name"]
        print(f"  {nm}({tc}): 共 {by_target[tc]} | "
              f"始发 {by_role[(tc,'origin')]} 到达 {by_role[(tc,'terminus')]} "
              f"经过 {by_role[(tc,'pass')]}")

    used = set()
    for t in hit_trains:
        for s in t["stops"]:
            if s["name"] in name_to_tc:
                used.add(name_to_tc[s["name"]])
    station_out = {}
    for tc in used:
        v = stations[tc]
        station_out[tc] = {"name": v["name"], "lng": v["lng"], "lat": v["lat"],
                           "src": v.get("coord_source")}
    print("涉及站点:", len(station_out))
    print("其中缺坐标:", sum(1 for v in station_out.values() if v["lng"] is None))
    if missing_coord:
        print("  缺坐标站(按出现次数):",
              ", ".join(f"{k}x{v}" for k, v in missing_coord.most_common(25)))

    hit_trains.sort(key=lambda t: (t["cls"], t["code"]))
    meta = {
        "capture_date": DATE,
        "source": "12306 (kyfw.12306.cn)",
        "coord_type": "GCJ-02",
        "targets": [{"name": stations[tc]["name"], "telecode": tc}
                    for tc in TARGET_TC],
        "distance_note": "cum_km 为相邻站直线距离累加，非铁路运营里程",
        "note": "直线连线仅表示站点拓扑走向，非真实线位",
    }
    payload = {"meta": meta, "stations": station_out, "trains": hit_trains}
    dump_json(os.path.join(DATA, "app_data.json"), payload)

    # file:// 下 fetch 本地 json 会被 CORS 拦截，额外输出一份 js 供 <script src> 直接加载
    with open(os.path.join(DATA, "app_data.js"), "w", encoding="utf-8") as f:
        f.write("window.RAIL_DATA=")
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";")
    size = os.path.getsize(os.path.join(DATA, "app_data.js"))
    print(f"\n已写出 data/app_data.json / app_data.js ({size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
