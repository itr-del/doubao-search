# 🔍 doubao-search

> 豆包搜索 (Doubao Search) API 封装 Skill — 提供豆包 AI 搜索的统一接口。

## ✨ 功能

- 🔍 **网页搜索**：调用豆包 AI 搜索接口
- 📰 **新闻聚合**：实时新闻搜索
- 🌐 **多语言**：支持中英文搜索
- ⚡ **流式响应**：SSE 流式返回

## 🚀 使用

```python
from doubao_search import search

result = search("今天的 AI 新闻", top_k=10)
for item in result.items:
    print(item.title, item.url)
```

## 📁 文件

- `SKILL.md` — Skill 完整定义
- `doubao_search.py` — 搜索封装
- `requirements.txt` — 依赖

## ⚙️ 配置

环境变量：
- `DOUBAO_API_KEY` — 豆包 API Key
- `DOUBAO_ENDPOINT` — API 端点

## 📜 License

MIT

## 🙏 致谢

字节跳动豆包 (Doubao) AI 平台。
