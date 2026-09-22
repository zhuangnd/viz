# -*- coding: utf-8 -*-
"""P3 逐车次拉取完整经停时刻表（czxx/queryByTrainNo）。
支持断点续传：已抓过的 train_no 自动跳过；每 100 条写入一次。
"""
import json
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rail_common import DATA, dump_json, load_json, norm_name  # noqa: E402

CZXX = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo"
DATE = os.environ.get("RAIL_DATE", "2026-09-22")
WORKERS = 3
OUT = os.path.join(DATA, "schedules_raw.json")

UA_POOL = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]
_local = threading.local()
lock = threading.Lock()
stats = {"ok": 0, "empty": 0, "fail": 0, "done": 0}


def session():
    if not hasattr(_local, "s"):
        s = requests.Session()
        s.headers.update({
            "User-Agent": random.choice(UA_POOL),
            "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
            "Accept": "*/*",
        })
        try:
            s.get("https://kyfw.12306.cn/otn/leftTicket/init", timeout=20)
        except Exception:
            pass
        _local.s = s
    return _local.s


def fetch(train):
    tc_a, tc_b = train.get("_tc_from"), train.get("_tc_to")
    if not tc_a or not tc_b:
        with lock:
            stats["fail"] += 1
        return train["train_no"], None
    for attempt in range(3):
        try:
            r = session().get(CZXX, params={
                "train_no": train["train_no"],
                "from_station_telecode": tc_a,
                "to_station_telecode": tc_b,
                "depart_date": DATE,
            }, timeout=25)
            if r.status_code != 200:
                raise RuntimeError("http %s" % r.status_code)
            rows = (r.json().get("data") or {}).get("data") or []
            time.sleep(random.uniform(0.35, 0.8))
            return train["train_no"], rows
        except Exception:
            if attempt == 2:
                with lock:
                    stats["fail"] += 1
                return train["train_no"], None
            time.sleep(1.5 * (attempt + 1))
    return train["train_no"], None


def main():
    stations = load_json(os.path.join(DATA, "stations.json"))
    name_to_tc = {norm_name(v["name"]): k for k, v in stations.items()}
    cands = load_json(os.path.join(DATA, "candidates.json"))

    for t in cands:
        t["_tc_from"] = name_to_tc.get(norm_name(t.get("start_station")))
        t["_tc_to"] = name_to_tc.get(norm_name(t.get("end_station")))

    results = {}
    if os.path.exists(OUT):
        results = load_json(OUT)
        print("断点续传: 已有", len(results), "条")

    todo = [t for t in cands if t["train_no"] not in results]
    total_todo = len(todo)
    print(f"待抓取: {total_todo} 条, 并发 {WORKERS}")
    sys.stdout.flush()

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(fetch, t): t for t in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            tn, rows = fut.result()
            if rows:
                results[tn] = rows
                with lock:
                    stats["ok"] += 1
            elif rows == []:
                results[tn] = []
                with lock:
                    stats["empty"] += 1
            if i % 100 == 0:
                dump_json(OUT, results)
                el = time.time() - t0
                print(f"  {i}/{total_todo} ok={stats['ok']} empty={stats['empty']} "
                      f"fail={stats['fail']} {el:.0f}s 预计剩余 "
                      f"{el/i*(total_todo-i):.0f}s")
                sys.stdout.flush()

    dump_json(OUT, results)
    print(f"\n完成: 总计 {len(results)} 条 | ok={stats['ok']} "
          f"empty={stats['empty']} fail={stats['fail']} | {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
