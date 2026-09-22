#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rail-doubao 阶段2 · 站点坐标校正（同名消歧）
规则：地理编码结果的 display_name 必须包含站名（或站名+“站”），否则判定错位并用地级市/县限定重查。
输出：data/station_coords.json（修正后）；无法定位者 lat=None 并注明。
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

UA = "rail-doubao-pilot/1.0 (personal research; nominatim usage)"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# 错位站 → 消歧查询（地级市/县限定；地理常识依据公开区划，仅作检索限定词）
HINTS = {
    "长汀南": ["长汀南站 龙岩市"], "瑞金": ["瑞金站 赣州市"], "于都": ["于都站 赣州市"],
    "会昌北": ["会昌北站 赣州市"], "尤溪": ["尤溪站 三明市"], "将乐": ["将乐站 三明市"],
    "诸暨": ["诸暨站 绍兴市"], "横店": ["横店站 东阳市"], "泰安": ["泰安站 泰安市"],
    "南靖": ["南靖站 漳州市"], "永泰": ["永泰站 福州市"], "利川": ["利川站 恩施土家族苗族自治州"],
    "醴陵东": ["醴陵东站 株洲市"], "凯里南": ["凯里南站 凯里市"], "邵阳北": ["邵阳北站 邵阳市"],
    "孝感北": ["孝感北站 孝感市"], "息县": ["息县站 信阳市"], "光山": ["光山站 信阳市"],
    "新县": ["新县站 信阳市"], "潢川": ["潢川站 信阳市"], "商南": ["商南站 商洛市"],
    "西峡": ["西峡站 南阳市"], "桐柏": ["桐柏站 南阳市"], "龙山镇": ["龙山镇站 漳平市"],
    "德兴": ["德兴站 上饶市"], "婺源": ["婺源站 上饶市"], "鄱阳": ["鄱阳站 上饶市"],
    "余干": ["余干站 上饶市"], "荆州": ["荆州站 荆州市"], "南平市": ["南平市站 南平市"],
    "千岛湖": ["千岛湖站 淳安县"], "宜兴": ["宜兴站 宜兴市"], "长兴": ["长兴站 长兴县"],
    "罗山": ["罗山站 信阳市"], "晋江": ["晋江站 晋江市"], "涵江": ["涵江站 莆田市"],
    "仙居": ["仙居站 台州市"], "长兴": ["长兴站 湖州市"], "冠豸山": ["冠豸山站 连城县", "冠豸山站 龙岩市"],
    "娄底南": ["娄底南站 娄底市"], "遵义": ["遵义站 遵义市"], "驻马店西": ["驻马店西站 驻马店市"],
    "涡阳": ["涡阳站 亳州市"], "渑池": ["渑池南站 三门峡市"], "临汾西": ["临汾西站 临汾市"],
}


def geocode(name, query):
    url = "https://nominatim.openstreetmap.org/search?q=%s&format=json&limit=3" % urllib.parse.quote(query)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Accept-Language", "zh-CN,zh;q=0.9")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            j = json.load(r)
    except Exception as exc:
        return None, str(exc)
    for hit in j:
        label = hit.get("display_name") or ""
        if name in label:
            return {"lat": float(hit["lat"]), "lon": float(hit["lon"]), "label": label[:80]}, None
    return None, "标签不含站名"


def main():
    path = os.path.join(DATA_DIR, "station_coords.json")
    coords = json.load(open(path, encoding="utf-8"))
    fixed = repaired = 0
    for nm, v in coords.items():
        label = v.get("label") or ""
        ok = nm in label
        if ok:
            v["verified"] = True
            fixed += 1
            continue
        # 需消歧
        v["verified"] = False
        got = None
        for q in HINTS.get(nm, [nm + "站", nm + "火车站"]):
            got, err = geocode(nm, q)
            time.sleep(1.1)
            if got:
                break
        if got:
            v.update(got); v["src"] = "nominatim"; v["verified"] = True
            repaired += 1
            print("修复 %s -> (%.4f, %.4f) %s" % (nm, got["lat"], got["lon"], got["label"][:44]))
        else:
            v["lat"] = None; v["lon"] = None
            v["note"] = "未定位（%s）" % (err or "多次尝试无结果")
            print("未定位 %s" % nm)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(coords, f, ensure_ascii=False, indent=1)
    missing = {k: v for k, v in coords.items() if v.get("lat") is None}
    print("总计=%d 已验证=%d 修复=%d 缺失=%d：%s" % (
        len(coords), fixed, repaired, len(missing), list(missing)[:30]))


if __name__ == "__main__":
    sys.exit(main())
