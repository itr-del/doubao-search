#!/usr/bin/env python3
"""
豆包搜索 Custom 版直连封装
文档: https://www.volcengine.com/docs/87772/2272949
认证: API Key 接入 (Bearer)
Endpoint: https://open.feedcoopapi.com/search_api/web_search
"""

import os
import sys
import json
import requests

API_KEY = os.environ.get("DOUBAO_SEARCH_API_KEY", "gbOTyw4keeY7nwv8ly1p6ur2IYb6DmIa")
BASE_URL = "https://open.feedcoopapi.com/search_api/web_search"

session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
})


def search(query: str, count: int = 10, search_type: str = "web", time_range: str = "", sites: str = "", block_hosts: str = ""):
    """
    豆包搜索
    :param query: 搜索关键词，1~100字符
    :param count: 返回条数，最多50，默认10
    :param search_type: web / image，当前 endpoint 仅支持 web
    :param time_range: OneDay / OneWeek / OneMonth / OneYear / YYYY-MM-DD..YYYY-MM-DD
    :param sites: 指定站点，|分隔，最多20个
    :param block_hosts: 屏蔽站点，|分隔，最多5个
    :return: dict
    """
    if not query or not query.strip():
        raise ValueError("query 不能为空")

    body = {
        "Query": query.strip()[:100],
        "SearchType": search_type,
        "Count": min(max(int(count), 1), 50)
    }

    filt = {}
    if sites:
        filt["Sites"] = sites
    if block_hosts:
        filt["BlockHosts"] = block_hosts
    if filt:
        body["Filter"] = filt

    if time_range:
        body["TimeRange"] = time_range

    try:
        resp = session.post(BASE_URL, json=body, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        return {"ok": False, "error": str(e)}

    rm = data.get("ResponseMetadata", {})
    err = rm.get("Error")
    if err:
        return {
            "ok": False,
            "code": err.get("Code"),
            "message": err.get("Message"),
            "request_id": rm.get("RequestId")
        }

    result = data.get("Result") or {}
    web_results = result.get("WebResults") or []
    items = []
    for item in web_results:
        items.append({
            "title": item.get("Title"),
            "url": item.get("Url"),
            "snippet": item.get("Snippet"),
            "summary": item.get("Summary"),
            "site": item.get("SiteName"),
            "published": item.get("PublishTime"),
            "rank": item.get("RankScore")
        })

    return {
        "ok": True,
        "query": result.get("SearchContext", {}).get("OriginQuery"),
        "search_type": result.get("SearchContext", {}).get("SearchType"),
        "count": result.get("ResultCount"),
        "time_cost_ms": result.get("TimeCost"),
        "items": items
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python doubao_search.py <搜索词> [条数]")
        sys.exit(1)

    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    result = search(query, count=count)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
