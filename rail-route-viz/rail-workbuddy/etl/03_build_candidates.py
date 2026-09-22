# -*- coding: utf-8 -*-
"""P2.5 坐标修正 + 几何剪枝：从 7004 个 G/D 车次里筛出可能经过目标站的候选。

剪枝依据：车次起终点连线若离目标站过远，其线路不可能经停该站。
坐标缺失的车次一律保守保留。
"""
import json
import os
import sys
from math import cos, radians

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rail_common import DATA, dump_json, load_json, norm_name  # noqa: E402

# 经核实的手工补录坐标（GCJ-02）。数据集里的「冠豸山」是 2021 年更名前的旧站，
# 实为今天的冠豸山南站，直接套用会让冠豸山站错位约 24km。
MANUAL_FIX = {
    # --- 2021 年更名导致的坐标错位，必须修正 ---
    "GPS": (116.722755, 25.740146, "manual_verified"),   # 冠豸山（原冠豸山北站，隔川镇）
    "GSS": (116.680051, 25.524282, "manual_verified"),   # 冠豸山南（原冠豸山站，朋口镇）
    # --- 坐标快照缺失的近年新线站点 ---
    "NHS": (116.728203, 26.246911, "manual_verified"),   # 宁化（兴泉/建化）
    "QLS": (116.814880, 26.214148, "manual_verified"),   # 清流（兴泉/清冠）
    "AYS": (116.799730, 25.842658, "manual_verified"),   # 杨源（清冠）
    "SDG": (116.349715, 26.297699, "manual_verified"),   # 石城东（兴泉）
    "NIG": (115.975172, 26.399972, "manual_verified"),   # 宁都（兴泉）
    "WPS": (116.218883, 24.992495, "manual_verified"),   # 武平（龙龙高铁）
    "FVS": (119.304148, 25.697761, "manual_verified"),   # 福清西（福厦高铁）
    "QGS": (118.880032, 25.174856, "manual_verified"),   # 泉港（福厦高铁）
    "QNS": (118.584166, 24.737787, "manual_verified"),   # 泉州南（福厦高铁）
    # --- 更名站：老数据集里是旧名，需要按现名重新指定 ---
    "KNQ": (114.492415, 22.785531, "manual_verified"),   # 惠阳（原惠州南）
    "YPS": (118.272406, 26.590924, "manual_verified"),   # 延平（原南平北）
    # --- 其他高频新建站 ---
    "WYG": (117.877704, 29.239096, "manual_verified"),   # 婺源（合福/衢九）
    "HVU": (119.986586, 30.298937, "manual_verified"),   # 杭州西（合杭/杭温）
    # --- 数据集错配到同名地点：坐标看似有效但位置完全不对 ---
    # 数据集给的是宁德古田县的位置（同名误配），与上杭县古田镇实址相差约 237km。
    # 抽核 G2294：龙岩→古田会址 16 分钟，旧坐标换算隐含直线均速 895km/h，新坐标 96km/h。
    "STS": (116.773087, 25.184694, "manual_verified"),   # 古田会址（赣瑞龙，上杭县古田镇）
}
TARGETS = {"厦门": "XMS", "厦门北": "XKS", "冠豸山": "GPS", "冠豸山南": "GSS"}
THRESHOLD_KM = float(os.environ.get("RAIL_PRUNE_KM", "600"))


def point_to_segment_km(px, py, ax, ay, bx, by):
    """点到线段最短距离（公里）。输入为投影平面坐标。"""
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    cx, cy = ax + t * dx, ay + t * dy
    return ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5


def project(lng, lat, lat0):
    return lng * cos(radians(lat0)), lat


def main():
    stations = load_json(os.path.join(DATA, "stations.json"))

    for tc, (lng, lat, src) in MANUAL_FIX.items():
        if tc in stations:
            stations[tc].update(lng=lng, lat=lat, coord_source=src)
            print(f"修正 {stations[tc]['name']}({tc}) -> {lng}, {lat}")
    dump_json(os.path.join(DATA, "stations.json"), stations)

    name_to_tc = {norm_name(v["name"]): k for k, v in stations.items()}
    print("\n目标站:")
    for nm, tc in TARGETS.items():
        s = stations[tc]
        print(f"  {nm:<6} {tc} ({s['lng']}, {s['lat']}) src={s['coord_source']}")

    trains = load_json(os.path.join(DATA, "train_list_raw.json"))
    print("\n车次总数:", len(trains))

    lat0 = 25.0
    tpos = []
    for nm, tc in TARGETS.items():
        s = stations[tc]
        tpos.append(project(s["lng"], s["lat"], lat0))

    kept, dropped, nocoord = [], 0, 0
    for t in trains:
        a = stations.get(name_to_tc.get(norm_name(t["start_station"]), ""))
        b = stations.get(name_to_tc.get(norm_name(t["end_station"]), ""))
        if not a or not b or a.get("lng") is None or b.get("lng") is None:
            t["prune_reason"] = "coord_missing"
            kept.append(t)
            nocoord += 1
            continue
        ax, ay = project(a["lng"], a["lat"], lat0)
        bx, by = project(b["lng"], b["lat"], lat0)
        best = min(point_to_segment_km(px, py, ax, ay, bx, by) * 111.0
                   for px, py in tpos)
        if best <= THRESHOLD_KM:
            t["prune_km"] = round(best, 1)
            kept.append(t)
        else:
            dropped += 1

    print(f"\n剪枝阈值 {THRESHOLD_KM}km")
    print(f"  保留候选: {len(kept)}  (其中缺坐标保守保留 {nocoord})")
    print(f"  剪掉:     {dropped}")
    dump_json(os.path.join(DATA, "candidates.json"), kept)


if __name__ == "__main__":
    main()
