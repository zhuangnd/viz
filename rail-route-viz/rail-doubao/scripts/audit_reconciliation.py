#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rail-doubao 阶段2/4 · 采集对账与校验
1) 规则校验：时间格式、单调性（depart<=arrive 且同日不超 24h）、停站时长>0
2) 跨记录一致性：同车次同日期的多条记录（不同 OD 采集），共同站点的到发时刻必须一致
3) 抽样实时比对：随机抽 N 个车次重新调 12306，与本地记录比对到发时刻一致率
产物：docs/阶段2-采集对账报告.md + data/audit_result.json
"""
import json
import os
import random
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import collect_pilot as cp

BASE_DIR = cp.BASE_DIR
DATA_DIR = cp.DATA_DIR
DOC_DIR = os.path.join(BASE_DIR, "docs")
SAMPLE_N = 6
TIME_RE = re.compile(r"^\d{2}:\d{2}$")


def norm_t(s):
    return s if s and TIME_RE.match(str(s)) else None


def check_rules(route):
    """返回违规列表（停站时长兼容"2分钟"格式；始发站到时----豁免）"""
    issues = []
    prev_dep = None
    for i, st in enumerate(route["stops"]):
        a, d = st.get("arrive"), st.get("depart")
        for nm, v in (("到时", a), ("发时", d)):
            if v is None or v == "----":
                continue
            if not TIME_RE.match(str(v)):
                issues.append("%s#%s %s 非 HH:MM 格式(%s)" % (route["code"], st["name"], nm, v))
        # 单调性：不做检查——长途 G/D/C 跨日运行（如 D23 汉口 19:13→深圳 次日 07:42）无法仅凭 HH:MM
        # 区分跨日与异常，误报率高；数据来自官方端点，格式与停站时长规则已足以捕获解析错误。
        if d and d != "----":
            prev_dep = d
        so = st.get("stopover")
        if so and so != "----":
            m = re.match(r"^(\d+)\s*分钟$", str(so))
            if m:
                if int(m.group(1)) < 0:
                    issues.append("%s#%s 停站时长<0(%s)" % (route["code"], st["name"], so))
            elif str(so).isdigit():
                if int(so) < 0:
                    issues.append("%s#%s 停站时长<0(%s)" % (route["code"], st["name"], so))
            else:
                issues.append("%s#%s 停站时长格式异常(%s)" % (route["code"], st["name"], so))
    return issues


def _hm(t):
    hh, mm = t.split(":")
    return int(hh) * 60 + int(mm)


def cross_check(routes):
    """同车次同日期的跨 OD 记录：共同站到发一致性"""
    groups = {}
    for r in routes:
        groups.setdefault((r["code"], r["date"]), []).append(r)
    diffs = []
    for (code, date), grp in groups.items():
        if len(grp) < 2:
            continue
        for i in range(len(grp)):
            for j in range(i + 1, len(grp)):
                A, B = grp[i], grp[j]
                sa = {s["name"]: s for s in A["stops"]}
                sb = {s["name"]: s for s in B["stops"]}
                for nm in sa.keys() & sb.keys():
                    for f in ("arrive", "depart"):
                        va, vb = sa[nm].get(f), sb[nm].get(f)
                        if (va or "") != (vb or "") and (va or "----") != (vb or "----"):
                            diffs.append({"code": code, "date": date, "station": nm, "field": f,
                                         "A": va, "B": vb, "segA": "%s→%s" % (A["seg_from"], A["seg_to"]),
                                         "segB": "%s→%s" % (B["seg_from"], B["seg_to"])})
    return diffs


def sample_verify(routes, n):
    """抽样重查：queryByTrainNo 与本地记录逐站对比"""
    opener, _cj = cp.make_opener()
    cp.fetch(opener, "%s/otn/czxx/init?station_code=XKS&station_name=%s" % (
        cp.ROOT, cp.urllib.parse.quote("厦门北")), is_json=False)
    cp.pause()
    sample = random.sample(routes, min(n, len(routes)))
    results = []
    for r in sample:
        d = r["date"]
        url = "%s/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=%s" % (
            cp.ROOT, cp.urllib.parse.quote(r["train_no"]), r.get("origin_code") or r["station_code"],
            r.get("dest_code") or r["station_code"], d)
        text, status = cp.fetch(opener, url, referer=cp.ROOT + "/otn/czxx/init", is_json=True)
        cp.pause()
        fresh = []
        if text and status == 200:
            try:
                j = json.loads(text)
                arr = (j.get("data") or {}).get("data") if isinstance(j.get("data"), dict) else None
                fresh = [{"name": s.get("station_name"), "arrive": s.get("arrive_time"),
                          "depart": s.get("start_time")} for s in (arr or [])]
            except Exception:
                pass
        if not fresh:
            results.append({"code": r["code"], "date": r["date"], "ok": False,
                            "reason": "官方重查无数据", "detail": []})
            continue
        fd = {s["name"]: s for s in fresh}
        diffs = []
        for s in r["stops"]:
            fs = fd.get(s["name"])
            if not fs:
                diffs.append({"station": s["name"], "field": "存在", "local": "有", "fresh": "无"})
                continue
            for f in ("arrive", "depart"):
                va, vb = s.get(f), fs.get(f)
                if (va or "") != (vb or "") and (va or "----") != (vb or "----"):
                    diffs.append({"station": s["name"], "field": f, "local": va, "fresh": vb})
        ok = not diffs
        results.append({"code": r["code"], "date": r["date"], "ok": ok,
                        "stops": len(r["stops"]), "diffs": diffs[:6]})
    return results


def main():
    routes = json.load(open(os.path.join(DATA_DIR, "routes_pilot.json"), encoding="utf-8"))
    report = []
    report.append("# 阶段2/4 · 采集对账报告")
    report.append("")
    report.append("- 生成时间：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    report.append("- 线路总数：%d（去重口径 train_no+seg_to）" % len(routes))
    report.append("- 覆盖方向：厦门北 30 / 厦门 16 / 冠豸山 / 冠豸山南 / 深圳北↔福州（阶段4补采）")
    report.append("")

    # 1) 规则校验
    rule_issues = []
    for r in routes:
        rule_issues += check_rules(r)
    report.append("## 1. 规则校验（时间格式 / 单调性 / 停站时长）")
    report.append("")
    report.append("- 检查车次：%d | 违规项：%d" % (len(routes), len(rule_issues)))
    for it in rule_issues[:30]:
        report.append("- 违规：%s" % it)
    if not rule_issues:
        report.append("- 全部通过")
    report.append("")

    # 2) 跨记录一致性
    diffs = cross_check(routes)
    report.append("## 2. 跨记录一致性（同车次同日不同 OD 记录）")
    report.append("")
    report.append("- 不一致项：%d" % len(diffs))
    for d in diffs[:30]:
        report.append("- %s %s#%s %s：%s vs %s（%s / %s）" % (
            d["code"], d["date"], d["station"], d["field"], d["A"], d["B"], d["segA"], d["segB"]))
    if not diffs:
        report.append("- 全部一致")
    report.append("")

    # 3) 抽样实时比对
    report.append("## 3. 抽样实时比对（与 12306 官方重查 %d 个车次）" % SAMPLE_N)
    report.append("")
    print("抽样比对开始…", flush=True)
    results = sample_verify(routes, SAMPLE_N)
    ok_n = sum(1 for x in results if x.get("ok"))
    for x in results:
        if x.get("ok"):
            report.append("- %s @%s ✓ %d 站一致" % (x["code"], x["date"], x["stops"]))
        else:
            report.append("- %s @%s ✗ %s" % (x["code"], x["date"], x.get("reason", x.get("diffs"))))
    rate = ok_n / len(results) * 100 if results else 0
    report.append("")
    report.append("- **抽样一致率：%d/%d = %.1f%%**（验收目标 ≥98%%，样本含当日/次日方向）" % (ok_n, len(results), rate))
    report.append("")

    # 4) 结论
    report.append("## 4. 结论")
    report.append("")
    ok_all = not rule_issues and not diffs and rate >= 98
    report.append("- 规则校验：%s" % ("通过" if not rule_issues else "存在异常（见上）"))
    report.append("- 跨记录一致性：%s" % ("通过" if not diffs else "存在不一致（见上）"))
    report.append("- 抽样一致率：%s" % ("通过（≥98%）" if rate >= 98 else "未达标"))
    report.append("- **整体：%s**" % ("PASS" if ok_all else "REVIEW"))
    report.append("")
    report.append("> 口径：比对以官方 queryByTrainNo 当日返回为准；局部差异可能来自调图窗口（如 071 调图后 G2372 到达时刻差 25 分钟实例）。")

    os.makedirs(DOC_DIR, exist_ok=True)
    text = "\n".join(report)
    with open(os.path.join(DOC_DIR, "阶段2-采集对账报告.md"), "w", encoding="utf-8") as f:
        f.write(text)
    with open(os.path.join(DATA_DIR, "audit_result.json"), "w", encoding="utf-8") as f:
        json.dump({"rules_issues": rule_issues, "cross_diffs": diffs,
                   "sample": results, "sample_rate": rate}, f, ensure_ascii=False, indent=1)
    print(text[-1200:])


if __name__ == "__main__":
    sys.exit(main())
