#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rail-doubao 阶段2 · 试点数据采集脚本（厦门北/厦门/冠豸山/冠豸山南 四站 + 途经/终到补验）

链路（复用阶段1已验证端点）：
  - leftTicket/queryG：站到站车次列表（含 train_no / 始发终到 / 到发时刻 / 历时）
  - czxx/queryByTrainNo：车次完整经停序列（depart_date 需 YYYY-MM-DD）
方向设计：
  - 出向：厦门北→杭州东、厦门北→成都东（阶段1已采，复用缓存）
  - 入向：杭州东→厦门北、成都东→厦门北（补验「终到/途经」判定：终到站=厦门北 → 终到；否则途经）
  - 示例站：厦门(XMS)、冠豸山(GPS)、冠豸山南(GSS) 各一条 O-D（厦门→冠豸山、厦门→冠豸山南）
产物：data/station_od_*.json（车次行）、data/schedules/*.json（经停，缓存复用）、data/routes_pilot.json（线路汇总）
原则：低频节流、仅个人/内部研究；仅 Python 标准库。
"""
import json
import os
import random
import ssl
import sys
import time
import urllib.parse
import urllib.request
import http.cookiejar

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
ROOT = "https://kyfw.12306.cn"
SLEEP_BASE = 3.0
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCHED_DIR = os.path.join(DATA_DIR, "schedules")
os.makedirs(SCHED_DIR, exist_ok=True)
LOG = []

# 方向清单：(起点站, 终点站, 日期, 说明)
ODS = [
    ("XKS", "HGH", "2026-09-22", "厦门北→杭州东（出向样例）"),
    ("XKS", "CDW", "2026-09-23", "厦门北→成都东（出向样例）"),
    ("HGH", "XKS", "2026-09-22", "杭州东→厦门北（入向，补验终到/途经）"),
    ("CDW", "XKS", "2026-09-23", "成都东→厦门北（入向，补验终到/途经）"),
    ("XKS", "XMS", "2026-09-22", "厦门北→厦门（示例站·厦门）"),
    ("XMS", "GPS", "2026-09-22", "厦门→冠豸山（示例站·冠豸山）"),
    ("XMS", "GSS", "2026-09-22", "厦门→冠豸山南（示例站·冠豸山南）"),
]

D2 = {v["code"]: k for k, v in json.load(
    open(os.path.join(DATA_DIR, "station_dict.json"), encoding="utf-8")).items() if v.get("code")}


def log(msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    LOG.append(line)
    print(line, flush=True)


def pause():
    time.sleep(SLEEP_BASE + random.uniform(0, 1.5))


def make_opener():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj),
        urllib.request.HTTPSHandler(context=ctx),
    ), cj


def fetch(opener, url, referer=None, is_json=False):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Accept", "application/json, text/javascript, */*; q=0.01" if is_json
                   else "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8")
    req.add_header("Accept-Language", "zh-CN,zh;q=0.9")
    req.add_header("If-Modified-Since", "0")
    req.add_header("Cache-Control", "no-cache")
    if referer:
        req.add_header("Referer", referer)
    try:
        with opener.open(req, timeout=20) as resp:
            raw = resp.read()
            status = getattr(resp, "status", 200)
    except Exception as exc:
        log("  ! 请求失败: %r" % exc)
        return None, 0
    return raw.decode("utf-8", "replace"), status


def save(name, obj, subdir=None):
    d = os.path.join(DATA_DIR, subdir) if subdir else DATA_DIR
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def queryG(opener, frm, to, date):
    url = "%s/otn/leftTicket/queryG?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT" % (
        ROOT, date, frm, to)
    text, status = fetch(opener, url, referer=ROOT + "/otn/leftTicket/init", is_json=True)
    rows = []
    if text and status == 200:
        try:
            j = json.loads(text)
            rows = (j.get("data") or {}).get("result") or []
            log("  车次数=%d" % len(rows))
        except Exception as exc:
            log("  ! 解析失败: %r" % exc)
    pause()
    return rows


def parse_row(line):
    p = line.split("|")
    if len(p) < 14:
        return None
    return {"train_no": p[2], "code": p[3], "start_telecode": p[4], "end_telecode": p[5],
            "seg_from": p[6], "seg_to": p[7], "depart": p[8], "arrive": p[9],
            "lishi": p[10], "date": p[13]}


def schedule(opener, row):
    key = "%s_%s" % (row["train_no"], row["date"])
    cache = os.path.join(SCHED_DIR, key + ".json")
    if os.path.exists(cache):
        log("  经停补齐 %s（缓存）" % row["code"])
        return json.load(open(cache, encoding="utf-8"))["stops"]
    d = "%s-%s-%s" % (row["date"][:4], row["date"][4:6], row["date"][6:8])
    url = "%s/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=%s" % (
        ROOT, urllib.parse.quote(row["train_no"]), row["seg_from"], row["seg_to"], d)
    text, status = fetch(opener, url, referer=ROOT + "/otn/czxx/init", is_json=True)
    stops = []
    if text and status == 200:
        try:
            j = json.loads(text)
            arr = (j.get("data") or {}).get("data") if isinstance(j.get("data"), dict) else None
            for st in arr or []:
                stops.append({"no": st.get("station_no"), "name": st.get("station_name"),
                              "arrive": st.get("arrive_time"), "depart": st.get("start_time"),
                              "stopover": st.get("stopover_time"), "run_time": st.get("run_time")})
            log("  经停补齐 %s → %d 站" % (row["code"], len(stops)))
        except Exception as exc:
            log("  ! 解析失败: %r" % exc)
    if stops:
        save("%s.json" % key, {"train_no": row["train_no"], "code": row["code"], "date": row["date"],
                               "seg_from": row["seg_from"], "seg_to": row["seg_to"],
                               "origin": D2.get(row["start_telecode"]), "dest": D2.get(row["end_telecode"]),
                               "stops": stops}, subdir="schedules")
    pause()
    return stops


def role_of(row, station_code):
    if row["start_telecode"] == station_code:
        return "始发"
    if row["end_telecode"] == station_code:
        return "终到"
    return "途经"


def main():
    log("=== 阶段2 试点数据采集 | 四站+途经/终到补验 ===")
    opener, cj = make_opener()
    # 会话预热
    fetch(opener, "%s/otn/czxx/init?station_code=XKS&station_name=%s" % (
        ROOT, urllib.parse.quote("厦门北")), is_json=False)
    pause()

    all_routes = []
    seen = set()
    for frm, to, date, note in ODS:
        log("OD %s→%s @%s（%s）" % (D2.get(frm, frm), D2.get(to, to), date, note))
        rows = queryG(opener, frm, to, date)
        for line in rows:
            r = parse_row(line)
            if not r:
                continue
            key = (r["train_no"], r["seg_to"])
            if key in seen:
                continue
            seen.add(key)
            stops = schedule(opener, r)
            if not stops:
                continue
            f_name = D2.get(r["seg_from"], r["seg_from"])
            t_name = D2.get(r["seg_to"], r["seg_to"])
            f = next((s for s in stops if s["name"] == f_name), None)
            t = next((s for s in stops if s["name"] == t_name), None)
            all_routes.append({
                "code": r["code"], "train_no": r["train_no"], "date": date,
                "origin": D2.get(r["start_telecode"]), "dest": D2.get(r["end_telecode"]),
                "origin_code": r["start_telecode"], "dest_code": r["end_telecode"],
                "station": D2.get(frm, frm), "station_code": frm,
                "role": role_of(r, frm),
                "seg_from": f_name, "seg_to": t_name,
                "seg_depart": (f or {}).get("depart"), "seg_arrive": (t or {}).get("arrive"),
                "lishi": r["lishi"], "stop_count": len(stops),
                "stops": stops,
            })
        pause()

    save("routes_pilot.json", all_routes)
    log("=== 完成：线路数=%d ===" % len(all_routes))
    for r in all_routes:
        log("  [%s] %s %s→%s 经停%d站" % (r["role"], r["code"], r["origin"], r["dest"], r["stop_count"]))


if __name__ == "__main__":
    sys.exit(main())
