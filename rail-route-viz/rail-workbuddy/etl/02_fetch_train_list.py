# -*- coding: utf-8 -*-
"""P2 全量 G/D 车次枚举：search.12306.cn 按车次号前缀 BFS 递归。
单次返回 >=200 视为被截断并细分一层（最多到 3 位数字）。
BFS 分层并行，避免线程池内嵌套 submit 造成死锁。
"""
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rail_common import DATA, dump_json  # noqa: E402

SEARCH_URL = "https://search.12306.cn/search/v1/train/search"
DATE = "20260922"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
LIMIT = 200
MAX_DIGITS = 3          # 前缀最多 3 位数字，如 G123
WORKERS = 5

collected = {}
stats = {"req": 0, "fail": 0, "truncated_at_max": 0}


def make_session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Referer": "https://www.12306.cn/index/"})
    return s


_local = __import__("threading").local()


def get_session():
    if not hasattr(_local, "s"):
        _local.s = make_session()
    return _local.s


def query(prefix, retries=3):
    for attempt in range(retries):
        try:
            r = get_session().get(SEARCH_URL, params={"keyword": prefix, "date": DATE},
                                  timeout=20)
            stats["req"] += 1
            if r.status_code != 200:
                raise RuntimeError("http %s" % r.status_code)
            return r.json().get("data") or []
        except Exception:
            if attempt == retries - 1:
                stats["fail"] += 1
                return None
            time.sleep(1.2 * (attempt + 1))
    return None


def absorb(rows):
    for row in rows:
        tn = row.get("train_no")
        code = row.get("station_train_code") or ""
        if not tn or not code:
            continue
        if not (code.startswith("G") or code.startswith("D")):
            continue
        collected[tn] = {
            "train_no": tn,
            "train_code": code,
            "start_station": row.get("from_station"),
            "end_station": row.get("to_station"),
        }


def bfs(letter):
    frontier = [letter]
    while frontier:
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            results = list(pool.map(query, frontier))
        nxt = []
        for prefix, rows in zip(frontier, results):
            if rows is None:
                continue
            digits = len(prefix) - 1
            if len(rows) >= LIMIT and digits < MAX_DIGITS:
                # 子前缀覆盖不到 prefix 自身的精确匹配，先收下
                absorb([r for r in rows if r.get("station_train_code") == prefix])
                nxt.extend(prefix + d for d in "0123456789")
            else:
                if len(rows) >= LIMIT:
                    stats["truncated_at_max"] += 1
                absorb(rows)
        print(f"  [{letter}] 层宽 {len(frontier)} -> 下一层 {len(nxt)} "
              f"| 累计车次 {len(collected)} | 请求 {stats['req']}")
        sys.stdout.flush()
        frontier = nxt


def main():
    t0 = time.time()
    for letter in ("G", "D"):
        bfs(letter)

    print(f"\n请求 {stats['req']} 次, 失败 {stats['fail']} 次, "
          f"最大深度仍截断 {stats['truncated_at_max']} 次, 耗时 {time.time()-t0:.0f}s")
    print("去重后 G/D 车次:", len(collected))

    by_class = {}
    for v in collected.values():
        by_class.setdefault(v["train_code"][0], []).append(v)
    for k in sorted(by_class):
        print(f"  {k}: {len(by_class[k])}")

    dump_json(os.path.join(DATA, "train_list_raw.json"), list(collected.values()))


if __name__ == "__main__":
    main()
