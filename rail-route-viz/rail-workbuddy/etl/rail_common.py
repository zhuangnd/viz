# -*- coding: utf-8 -*-
"""公共工具：会话、站名索引、时间解析。"""
import json
import os
import random
import time

import requests

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
RAW = os.path.join(BASE, "raw")

UA_POOL = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]


def new_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": random.choice(UA_POOL),
        "Referer": "https://kyfw.12306.cn/otn/leftTicket/init",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
    })
    s.get("https://kyfw.12306.cn/otn/leftTicket/init", timeout=20)
    return s


def polite_sleep(lo=0.35, hi=0.9):
    time.sleep(random.uniform(lo, hi))


def norm_name(s):
    """12306 部分接口返回的站名会插入全角/半角空格用于对齐（如 '南 昌'、'深  圳'），
    匹配电报码前必须归一化，否则会静默匹配失败。"""
    return (s or "").replace(" ", "").replace("\u3000", "").strip()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


def parse_hhmm(v):
    """'14:32' -> 872；'----'/None -> None"""
    if not v or v == "----":
        return None
    try:
        h, m = v.split(":")
        return int(h) * 60 + int(m)
    except Exception:
        return None


def parse_stopover(v):
    """'3分钟' -> 3；'----'/None -> 0"""
    if not v or v == "----":
        return 0
    digits = "".join(ch for ch in v if ch.isdigit())
    return int(digits) if digits else 0


def haversine_km(lng1, lat1, lng2, lat2):
    from math import asin, cos, radians, sin, sqrt
    r = 6371.0
    p1, p2 = radians(lat1), radians(lat2)
    dp = p2 - p1
    dl = radians(lng2 - lng1)
    a = sin(dp / 2) ** 2 + cos(p1) * cos(p2) * sin(dl / 2) ** 2
    return 2 * r * asin(sqrt(a))
