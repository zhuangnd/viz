#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rail-doubao 阶段1 · 数据可行性验证脚本 v3（试点：厦门北站）

对应设计方案第 04 节「数据可行性验证」：
  STEP 01 会话初始化：访问车站车次页获取会话 cookie（openRandCodeCheck=N，无需验证码）
  STEP 02 站点字典：按页面实际引用解析 station_name.js，定位目标站电报码
  STEP 03 车站车次查询：czxx/query（记录服务端 404 = 端点当前失效，浏览器内同证）
          → 替代链路 leftTicket/queryZ→queryG（站到站车次列表，含内部 train_no）
  STEP 04 经停补齐：czxx/queryByTrainNo（每趟车完整经停序列：到发时刻/停站/历时）
  STEP 05 交叉校验：queryG 行 ↔ queryByTrainNo 行一致性；与公开第三方时刻（G2372）比对

结论口径（v3 实测）：
  - czxx/query 官方端点服务端 404（无头与真实浏览器均 404，前端包引用未同步）
  - queryG + queryByTrainNo 可无头访问 → 线路数据模型（车站-车次-经停-时刻）可完整构建
  - 始发/终到/途经 由整列车始发站(字段4)/终到站(字段5) 与查询站比对判定

原则：低频、节流、仅个人/内部研究演示；仅用 Python 标准库。
"""
import json
import os
import random
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
import http.cookiejar

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
ROOT = "https://kyfw.12306.cn"
QUERY_DATE = "2026-09-22"
SAMPLE_DATE2 = "2026-09-23"     # G2372 运行日（当日查询为空，次日存在）
PILOT = "厦门北"
SLEEP_BASE = 3.0

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCHED_DIR = os.path.join(DATA_DIR, "schedules")
os.makedirs(SCHED_DIR, exist_ok=True)
LOG = []


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
    t0 = time.time()
    try:
        with opener.open(req, timeout=20) as resp:
            raw = resp.read()
            status = getattr(resp, "status", 200)
            final = resp.geturl()
    except urllib.error.HTTPError as exc:
        log("  ! HTTP %s -> %s" % (exc.code, url.split("?")[0]))
        return None, exc.code, url
    except Exception as exc:
        log("  ! 请求失败: %r" % exc)
        return None, 0, url
    text = raw.decode("utf-8", "replace")
    log("  -> %s | status=%s | bytes=%d | %.1fs" % (final, status, len(raw), time.time() - t0))
    return text, status, final


def save(name, obj, subdir=None):
    d = os.path.join(DATA_DIR, subdir) if subdir else DATA_DIR
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    log("  [saved] data/%s%s" % (subdir + "/" if subdir else "", name))


def step1_session(opener):
    log("STEP 01 会话初始化（车站车次页）")
    url = "%s/otn/czxx/init?station_code=XKS&station_name=%s" % (
        ROOT, urllib.parse.quote(PILOT))
    html, status, _ = fetch(opener, url)
    pause()
    rc = re.search(r"openRandCodeCheck\s*=\s*'(\w)'", html or "")
    return status == 200, (rc.group(1) if rc else None)


def step2_station_dict(opener):
    log("STEP 02 站点代码字典")
    url = "%s/otn/resources/js/framework/station_name.js?station_version=1.9374" % ROOT
    text, status, _ = fetch(opener, url, referer=ROOT + "/otn/czxx/init")
    entries = {}
    if text and status == 200:
        for seg in text.split("@"):
            parts = seg.split("|")
            if len(parts) >= 6 and parts[1]:
                entries[parts[1]] = {"code": parts[2], "abbr": parts[0],
                                     "pinyin": parts[3], "idx": parts[5]}
    targets = ["厦门北", "厦门", "冠豸山", "冠豸山南"]
    save("station_dict.json", entries)
    save("station_4.json", {t: entries.get(t) for t in targets})
    log("  字典条目=%d | 目标站=%s" % (
        len(entries), {k: (entries[k]["code"] if k in entries else None) for k in targets}))
    pause()
    return entries, bool(entries)


def step3_czxx_probe(opener, code, name):
    """车站车次官方端点验证：预期记录 404 失效事实（含服务端证据）。"""
    log("STEP 03 车站车次查询 %s（%s）——官方端点 czxx/query" % (name, code))
    init_url = "%s/otn/czxx/init?station_code=%s&station_name=%s" % (
        ROOT, urllib.parse.quote(code), urllib.parse.quote(name))
    url = "%s/otn/czxx/query?train_start_date=%s&train_station_name=%s&train_station_code=%s&randCode=" % (
        ROOT, QUERY_DATE, urllib.parse.quote(name), code)
    text, status, _ = fetch(opener, url, referer=init_url, is_json=True)
    ok = bool(text and status == 200 and text.lstrip().startswith("{"))
    note = ""
    if status == 404:
        note = "服务端 404（Tomcat 资源不存在）；浏览器内实测同样 404 → 端点当前失效，前端包引用未同步"
    elif status == 405:
        note = "405（仅 GET；仍需指纹校验）"
    pause()
    return ok, note


def queryG(opener, frm, to, date):
    """leftTicket/queryG 站到站车次列表（当前有效端点，queryZ 302 指向它）。"""
    url = "%s/otn/leftTicket/queryG?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT" % (
        ROOT, date, frm, to)
    text, status, _ = fetch(opener, url, referer=ROOT + "/otn/leftTicket/init", is_json=True)
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


def parse_g_row(line):
    p = line.split("|")
    if len(p) < 14:
        return None
    return {"train_no": p[2], "code": p[3], "start_telecode": p[4], "end_telecode": p[5],
            "seg_from": p[6], "seg_to": p[7], "depart": p[8], "arrive": p[9],
            "lishi": p[10], "date": p[13]}


def step4_schedule(opener, row, code2name):
    log("STEP 04 经停补齐 %s（%s）" % (row["code"], row["train_no"]))
    d = "%s-%s-%s" % (row["date"][:4], row["date"][4:6], row["date"][6:8])  # 需 YYYY-MM-DD
    url = "%s/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=%s" % (
        ROOT, urllib.parse.quote(row["train_no"]), row["seg_from"], row["seg_to"], d)
    text, status, _ = fetch(opener, url, referer=ROOT + "/otn/czxx/init", is_json=True)
    stops = []
    if text and status == 200:
        try:
            j = json.loads(text)
            arr = (j.get("data") or {}).get("data") if isinstance(j.get("data"), dict) else None
            for st in arr or []:
                stops.append({
                    "no": st.get("station_no"), "name": st.get("station_name"),
                    "arrive": st.get("arrive_time"), "depart": st.get("start_time"),
                    "stopover": st.get("stopover_time"), "run_time": st.get("run_time"),
                })
            log("  经停=%d 站" % len(stops))
        except Exception as exc:
            log("  ! 解析失败: %r" % exc)
    pause()
    return stops


def role_of(row, pilot_code):
    if row["start_telecode"] == pilot_code:
        return "始发"
    if row["end_telecode"] == pilot_code:
        return "终到"
    return "途经"


def main():
    log("=== rail-doubao 阶段1 验证 v3 | 试点=%s | 日期=%s ===" % (PILOT, QUERY_DATE))
    opener, cj = make_opener()
    ok_session, captcha_flag = step1_session(opener)
    entries, ok_dict = step2_station_dict(opener)
    code = (entries.get(PILOT) or {}).get("code", "")
    code2name = {v["code"]: k for k, v in entries.items() if v.get("code")}

    # STEP 03 官方车站车次端点验证（记录失效事实）
    czxx_ok, czxx_note = step3_czxx_probe(opener, code, PILOT)

    # STEP 03B 替代链路：queryG 站到站列表（厦门北→杭州东 当日；G2372 成都东方向次日）
    log("STEP 03B 替代链路 leftTicket/queryG（站到站）")
    rows_hz = queryG(opener, code, "HGH", QUERY_DATE)          # 厦门北→杭州东 当日
    rows_cd = queryG(opener, code, "CDW", SAMPLE_DATE2)         # 厦门北→成都东 次日（G2372）
    g_rows = [parse_g_row(r) for r in rows_hz + rows_cd]
    g_rows = [r for r in g_rows if r]
    # 去重（同 train_no 取段终点为杭州东/成都东 的行优先）
    seen, uniq = set(), []
    for r in g_rows:
        key = (r["train_no"], r["seg_to"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)
    for r in uniq:
        r["origin_name"] = code2name.get(r["start_telecode"], r["start_telecode"])
        r["dest_name"] = code2name.get(r["end_telecode"], r["end_telecode"])
        r["role"] = role_of(r, code)
    save("xks_hz_cd_od.json", uniq)
    log("  有效车次行=%d（含去重）" % len(uniq))

    # STEP 04 经停补齐
    schedules, routes = [], []
    for r in uniq:
        stops = step4_schedule(opener, r, code2name)
        sche = {"train_no": r["train_no"], "code": r["code"], "date": r["date"],
                "origin": r["origin_name"], "dest": r["dest_name"],
                "seg_from": r["seg_from"], "seg_to": r["seg_to"], "stops": stops}
        schedules.append(sche)
        save("%s_%s.json" % (r["code"], r["date"]), sche, subdir="schedules")
        if stops:
            routes.append({
                "code": r["code"], "train_no": r["train_no"], "date": r["date"],
                "origin": r["origin_name"], "dest": r["dest_name"], "role": r["role"],
                "od_depart": r["depart"], "od_arrive": r["arrive"], "od_lishi": r["lishi"],
                "stop_count": len(stops),
                "first_stop": stops[0], "last_stop": stops[-1],
            })
    save("xiamenbei_routes.json", routes)

    # STEP 05 交叉校验
    log("STEP 05 交叉校验")
    cross = {"queryG_vs_stops": [], "g2372_vs_public": None}
    for r in uniq:
        sch = next((s for s in schedules if s["train_no"] == r["train_no"]), None)
        if not sch or not sch["stops"]:
            continue
        seg_from_name = code2name.get(r["seg_from"], r["seg_from"])
        seg_to_name = code2name.get(r["seg_to"], r["seg_to"])
        f = next((st for st in sch["stops"] if st["name"] == seg_from_name), None)
        t = next((st for st in sch["stops"] if st["name"] == seg_to_name), None)
        cross["queryG_vs_stops"].append({
            "code": r["code"], "seg": "%s→%s" % (seg_from_name, seg_to_name),
            "queryG_depart": r["depart"], "stops_depart": (f or {}).get("depart"),
            "queryG_arrive": r["arrive"], "stops_arrive": (t or {}).get("arrive"),
            "match": bool(f and t and f.get("depart") == r["depart"] and t.get("arrive") == r["arrive"]),
        })
    g = next((r for r in uniq if r["code"] == "G2372"), None)
    if g:
        sch = next((s for s in schedules if s["train_no"] == g["train_no"]), None)
        last = sch["stops"][-1] if sch and sch["stops"] else {}
        first = sch["stops"][0] if sch and sch["stops"] else {}
        cross["g2372_vs_public"] = {
            "live_queryG": {"depart": g["depart"], "arrive": g["arrive"], "lishi": g["lishi"]},
            "live_stops": {"depart": first.get("depart"), "arrive": last.get("arrive") if last else None,
                           "stops": len(sch["stops"]) if sch else None},
            "public_2026_07_reference": {"depart": "06:48", "arrive": "20:33", "note": "方案演示用公开资料，与实时 20:58 有差 → 数据时效风险示例"},
        }
    pause()

    summary = {
        "pilot": PILOT, "query_date": QUERY_DATE, "sample_date2": SAMPLE_DATE2,
        "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "steps": {
            "session_ok": ok_session, "captcha_required": captcha_flag == "Y",
            "station_dict_ok": ok_dict, "station_code": code,
            "czxx_ok": czxx_ok, "czxx_note": czxx_note,
            "queryG_ok": bool(uniq), "schedule_ok": bool(schedules),
            "crosscheck_ok": all(c["match"] for c in cross["queryG_vs_stops"]) if cross["queryG_vs_stops"] else False,
        },
        "summary": {
            "od_rows": len(uniq),
            "by_role": {r: sum(1 for x in uniq if x["role"] == r) for r in ("始发", "终到", "途经")},
            "schedules": len(schedules),
            "cross": cross,
        },
        "log": LOG,
    }
    save("probe_result.json", summary)
    log("=== 验证结束 | czxx=%s | queryG=%s | schedule=%s | crosscheck=%s ===" % (
        summary["steps"]["czxx_ok"], summary["steps"]["queryG_ok"],
        summary["steps"]["schedule_ok"], summary["steps"]["crosscheck_ok"]))


if __name__ == "__main__":
    sys.exit(main())
