# Semantic Scholar API — 文献搜索参考

## 基本用法

```python
import urllib.request, json, time

def search_papers(query, limit=15):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query.replace(' ', '+')}&limit={limit}&fields=title,authors,year,journal,citationCount"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=15)
    return json.loads(resp.read())
```

## 速率限制

- 同一 IP 约 1 req/3s
- 触发 429 错误后需等待 30s+ 再重试
- 搜索 3-4 个关键词组时，每组间 `time.sleep(3)`

## 搜索策略

1. 用论文核心概念词搜索（如 "slurry flow battery"）
2. 按引用量排序找高影响力论文
3. 搜索 review/perspective 获取领域全景
4. 搜索开创性论文（如 "semi-solid lithium flow battery Chiang"）

## 去重

用论文标题作为唯一标识，避免重复收录。

## 返回字段

- `title`: 论文标题
- `authors`: 作者列表（取前3个）
- `year`: 发表年份
- `journal`: 期刊名称
- `citationCount`: 引用次数（用于排序）


