# -*- coding: utf-8 -*-
"""P6 召回率验证：用一条独立于剪枝的路径核对是否漏车次。

做法：对 4 个目标站，与一批主要车站双向做 leftTicket/query，
收集所有出现的 train_no（这些车次必然经过/始发/终到目标站），
再核对它们是否都已出现在最终数据集里。有遗漏说明几何剪枝阈值过小。
"""
import json
import os
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rail_common import DATA, load_json, new_session  # noqa: E402

TARGETS = {"厦门": "XMS", "厦门北": "XKS", "冠豸山": "GPS", "冠豸山南": "GSS"}
DATE = os.environ.get("RAIL_DATE", "2026-09-22")

# 覆盖干线方向的主要车站，用于双向对查
HUBS = ["北京南", "上海虹桥", "广州南", "深圳北", "杭州东", "南京南", "武汉",
        "长沙南", "成都东", "西安北", "郑州东", "福州", "福州南", "南昌西",
        "赣州", "龙岩", "漳州", "泉州", "莆田", "三明北", "合肥南", "济南西",
        "天津西", "重庆西", "昆明南", "贵阳东", "南宁东", "潮汕", "汕头",
        "宁波", "温州南", "黄山北", "上饶", "武夷山东"]


def main():
    stations = load_json(os.path.join(DATA, "stations.json"))
    name_to_tc = {v["name"]: k for k, v in stations.items()}
    s = new_session()

    found = {}          # train_no -> (目标站, 方向)
    req = 0
    for tname, ttc in TARGETS.items():
        for hub in HUBS:
            htc = name_to_tc.get(hub)
            if not htc:
                continue
            for a, b in ((ttc, htc), (htc, ttc)):
                try:
                    r = s.get("https://kyfw.12306.cn/otn/leftTicket/query",
                              params={"leftTicketDTO.train_date": DATE,
                                      "leftTicketDTO.from_station": a,
                                      "leftTicketDTO.to_station": b,
                                      "purpose_codes": "ADULT"}, timeout=20)
                    req += 1
                    rows = (r.json().get("data") or {}).get("result") or []
                    for row in rows:
                        f = row.split("|")
                        tn, code = f[2], f[3]
                        if not code.startswith(("G", "D")):
                            continue
                        found.setdefault(tn, set()).add((tname, f"{a}->{b}"))
                except Exception:
                    pass
                time.sleep(0.15)
        print(f"  {tname}: 已查 {req} 次, 累计发现车次 {len(found)}")

    print(f"\n验证集车次（去重）: {len(found)}, 查询 {req} 次")

    app = load_json(os.path.join(DATA, "app_data.json"))
    have = {t["train_no"] for t in app["trains"]}
    cands = {c["train_no"] for c in load_json(os.path.join(DATA, "candidates.json"))}
    sched = load_json(os.path.join(DATA, "schedules_raw.json"))

    missing = [tn for tn in found if tn not in have]
    print(f"最终数据集车次: {len(have)}")
    print(f"验证集中缺失: {len(missing)}")

    if missing:
        print("\n缺失明细（前 30）:")
        sched_empty = 0
        not_cand = 0
        for tn in missing[:30]:
            in_cand = tn in cands
            rows = sched.get(tn)
            print(f"  {tn}  候选集内={in_cand}  详情={'有' if rows else '无/空'}")
        for tn in missing:
            if tn not in cands:
                not_cand += 1
            elif not sched.get(tn):
                sched_empty += 1
        print(f"\n缺失原因: 未进候选集 {not_cand} 个, 已抓但详情为空 {sched_empty} 个")
        print("=> 若「未进候选集」占多数，说明剪枝阈值过小，请调大 RAIL_PRUNE_KM 重跑 03-05")
    else:
        print("\n通过：验证集车次全部被覆盖，剪枝未造成可观测遗漏")


if __name__ == "__main__":
    main()
