name: doubao-search
description: 豆包搜索 (Doubao Search) API 封装 Skill。当用户想搜索网络信息、查资料、找最新资讯、搜文档、搜论文、查产品、找教程、核实事实、查学术资料、或者任何需要"上网查一下"的时候使用。支持中英文混合搜索，可返回结构化结果（标题/链接/摘要/来源/发布时间）。适用于日常查询、技术调研、行业研究、新闻追踪等场景。**不要 undertrigger**——用户说"搜一下"、"查一下"、"帮我找"、"有没有"、"最新消息"、"什么情况"等任何暗示需要获取外部信息的请求，都应该优先考虑使用本 Skill。

---

# Doubao Search Skill

通过豆包搜索 API (`https://open.feedcoopapi.com/search_api/web_search`) 进行网络搜索，返回结构化搜索结果。Skill 会直接调用 REST API 拉取结果，不需要用户配置 MCP server，只需要提供 API Key。

## 先决条件

环境变量中已配置豆包搜索 API Key：

```bash
# ~/.bashrc / ~/.zshrc / ~/.profile 中已设置
export DOUBAO_SEARCH_API_KEY="gbOTyw4keeY7nwv8ly1p6ur2IYb6DmIa"
```

脚本路径：

```bash
/home/ubuntu/.hermes/skills/doubao-search/scripts/doubao_search.py
```

## 什么时候用

| 用户意图 | 应该调用 |
|---|---|
| 查资料 / 找信息 / 搜教程 | 直接调用 |
| "最新消息" / "最近发生了什么" | 直接调用，建议带 `time_range` |
| 核实事实 / 查证说法 | 直接调用 |
| 学术 / 论文 / 技术调研 | 直接调用 |
| 产品 / 公司 / 行业研究 | 直接调用 |
| 找链接 / 找文档 / 找资源 | 直接调用 |
| 用户只说了"搜一下" / "帮我查查" | 直接调用 |
| 训练数据可能过时的领域知识 | **优先调用**，不要凭记忆回答 |

## 调用方式

```bash
python3 /home/ubuntu/.hermes/skills/doubao-search/scripts/doubao_search.py "搜索关键词" [返回条数] [--参数]
```

## 参数说明

| 参数 | 说明 | 默认值 | 示例 |
|---|---|---|---|
| `query` (位置参数) | 搜索关键词，中英文均可 | 必填 | `"Python 异步编程 best practice"` |
| `count` (位置参数) | 返回结果数量 | `10` | `5` |
| `--search_type` | 搜索类型 | `web` | `web` / `image` |
| `--time_range` | 时间范围 | 无 | `OneWeek` / `OneMonth` / `OneYear` / `NoLimit` |
| `--sites` | 限定站点 | 无 | `github.com,stackoverflow.com` |
| `--block_hosts` | 屏蔽站点 | 无 | `example.com` |

### time_range 可选值

- `NoLimit`：不限时间
- `OneWeek`：最近一周
- `OneMonth`：最近一月
- `ThreeMonths`：最近三月
- `OneYear`：最近一年

## 返回数据形态

### 成功响应

```json
{
  "ok": true,
  "query": "搜索关键词",
  "search_type": "web",
  "count": 3,
  "time_cost_ms": 955,
  "items": [
    {
      "title": "结果标题",
      "url": "https://...",
      "snippet": "搜索结果的摘要片段...",
      "summary": "更详细的内容摘要（LLM 生成）...",
      "site": "来源网站",
      "published": "2026-07-28",
      "rank": 1
    }
  ]
}
```

### 字段说明

| 字段 | 说明 |
|---|---|
| `ok` | 请求是否成功 |
| `query` | 实际搜索的关键词 |
| `search_type` | 搜索类型 |
| `count` | 实际返回条数 |
| `time_cost_ms` | 接口耗时（毫秒） |
| `items[].title` | 结果标题 |
| `items[].url` | 结果链接 |
| `items[].snippet` | 搜索片段摘要 |
| `items[].summary` | 详细内容摘要（AI 生成） |
| `items[].site` | 来源域名/网站 |
| `items[].published` | 发布日期（YYYY-MM-DD） |
| `items[].rank` | 排名 |

### 错误响应

```json
{
  "ok": false,
  "error": "错误描述"
}
```

## 工作流示例

### 基础搜索

```bash
# 基础搜索，默认 10 条
python3 /home/ubuntu/.hermes/skills/doubao-search/scripts/doubao_search.py "豆包搜索怎么用"

# 指定返回 3 条
python3 /home/ubuntu/.hermes/skills/doubao-search/scripts/doubao_search.py "Python 异步编程 best practice" 3

# 限定站点搜索
python3 /home/ubuntu/.hermes/skills/doubao-search/scripts/doubao_search.py "React hooks tutorial" 5 --sites react.dev,developer.mozilla.org
```

### 时间范围搜索（适合新闻/最新动态）

```bash
# 最近一周
python3 /home/ubuntu/.hermes/skills/doubao-search/scripts/doubao_search.py "OpenAI GPT-5 发布" 5 --time_range OneWeek

# 最近一月
python3 /home/ubuntu/.hermes/skills/doubao-search/scripts/doubao_search.py "2025年AI Agent最新进展" 10 --time_range OneMonth

# 不限时间（适合历史资料）
python3 /home/ubuntu/.hermes/skills/doubao-search/scripts/doubao_search.py "Unix哲学" 5 --time_range NoLimit
```

### 程序化调用（Python 代码中使用）

```python
import subprocess
import json

def doubao_search(query, count=10, **kwargs):
    cmd = ["python3", "/home/ubuntu/.hermes/skills/doubao-search/scripts/doubao_search.py", query, str(count)]
    for k, v in kwargs.items():
        cmd.append(f"--{k}")
        cmd.append(v)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

# 使用
results = doubao_search("Python asyncio", count=5)
for item in results.get("items", []):
    print(f"- {item['title']} ({item['published']})")
    print(f"  {item['url']}")
    print(f"  {item['snippet']}")
```

## 给用户的输出格式

搜索结果应整理成清晰的中文列表，包含标题、链接、摘要和时间信息。

```markdown
**豆包搜索结果：<查询关键词>**（共 N 条，耗时 Xms）

1. **<标题>** — <来源网站>
   <摘要>
   <链接>

2. ...
```

**要点**：
- 保留原始链接，方便用户点击
- 优先展示 `summary`（更详细），若为空则展示 `snippet`
- `published` 转人话时间（如"2026-07-28" → "7月28日"）
- 按 `rank` 排序展示

## 注意事项

- **免费额度**：每月 500 次（火山账号维度），请合理使用
- **限流**：默认 5 QPS，串行调用即可
- **不要并发猛拉**：避免触发限流
- **训练数据优先搜索**：当用户问的问题可能依赖实时信息时，优先调用本 Skill 而非凭记忆回答
- **不要编造结果**：若 API 返回错误或空结果，如实告知用户
- **搜索词优化**：中英文混合搜索效果更好；复杂查询可拆分为多个简单查询

## 常见错误

- HTTP 401：API Key 无效或未配置环境变量
- HTTP 429：超出 QPS 限制，稍后重试
- HTTP 500：服务端错误，重试或换关键词
- `ok: false`：查询参数错误，检查参数格式
