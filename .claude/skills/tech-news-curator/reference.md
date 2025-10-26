# Tech News Curator - MCP Tools Reference

Complete reference for the engblogs MCP server tools with parameters, examples, and usage patterns.

## Table of Contents
- [get_sources](#get_sources)
- [get_content](#get_content)
- [get_article_full](#get_article_full)
- [search_articles](#search_articles)
- [semantic_search](#semantic_search)
- [get_daily_digest](#get_daily_digest)
- [set_tag](#set_tag)

---

## get_sources

List all RSS feed sources with pagination and filtering.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | Integer | 50 | Number of sources to return (recommended max: 100) |
| `offset` | Integer | 0 | Pagination offset (e.g., 50 for page 2, 100 for page 3) |
| `category` | String | null | Filter by category (case-insensitive partial match) |
| `favoritesOnly` | Boolean | false | Only show favorite blogs |

### Returns

```json
{
  "sources": [
    {
      "id": 123,
      "title": "OpenAI Blog",
      "url": "https://openai.com/blog/rss.xml",
      "category": "AI Research",
      "isFavorite": true
    }
  ],
  "total": 518,
  "success": true
}
```

### Examples

**List first 50 sources:**
```
mcp__engblogs__get_sources(limit: 50, offset: 0)
```

**Browse favorites only:**
```
mcp__engblogs__get_sources(favoritesOnly: true)
```

**Filter by category:**
```
mcp__engblogs__get_sources(category: "AI", limit: 50)
```

**Pagination example:**
```
# Page 1
mcp__engblogs__get_sources(limit: 50, offset: 0)

# Page 2
mcp__engblogs__get_sources(limit: 50, offset: 50)
```

### Use Cases
- Discover available RSS feeds before filtering
- Find exact source names for `get_content` filtering
- Browse feeds by category
- Identify which feeds to mark as favorites

---

## get_content

Browse recent articles with filtering and pagination. Token-efficient by default (returns titles and metadata only).

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | Integer | 10 | Number of articles to return |
| `offset` | Integer | 0 | Pagination offset |
| `statuses` | Array | null | Filter by ["unread", "read", "favorite", "archived"] |
| `source` | String | null | Filter by specific blog name (exact match) |
| `favoriteBlogsOnly` | Boolean | false | Only show articles from favorite blogs |
| `prioritizeFavoriteBlogs` | Boolean | false | Show favorite blog articles first, then others |
| `startDate` | String | null | Start date for filtering (ISO format: YYYY-MM-DD) |
| `endDate` | String | null | End date for filtering (ISO format: YYYY-MM-DD) |
| `includeContent` | Boolean | false | Include full article content (avoid for token efficiency) |
| `includeExcerpt` | Boolean | false | Include article excerpt/preview |

### Returns

```json
{
  "articles": [
    {
      "id": 15910,
      "title": "Clojure Runs ONNX AI Models Now",
      "link": "http://example.com/article",
      "pubDate": "2025-10-26T15:56:00.000Z",
      "fetchDate": "2025-10-26T22:06:57.822Z",
      "status": "unread",
      "feedTitle": "Dragan Djuric",
      "feedCategory": "Engineering Blogs",
      "excerpt": "Article preview text..." // if includeExcerpt: true
    }
  ],
  "total": 15910,
  "success": true
}
```

### Examples

**Token-efficient browsing (recommended):**
```
mcp__engblogs__get_content(limit: 50, includeContent: false, favoriteBlogsOnly: true)
```

**Browse unread articles:**
```
mcp__engblogs__get_content(limit: 20, statuses: ["unread"])
```

**Filter by date range:**
```
mcp__engblogs__get_content(
  limit: 50,
  startDate: "2025-10-20",
  endDate: "2025-10-26"
)
```

**Filter by specific source:**
```
mcp__engblogs__get_content(limit: 10, source: "OpenAI Blog")
```

**Prioritize favorites:**
```
mcp__engblogs__get_content(limit: 30, prioritizeFavoriteBlogs: true)
```

**Pagination example:**
```
# Browse first 50 titles
mcp__engblogs__get_content(limit: 50, offset: 0, includeContent: false)

# Continue browsing next 50
mcp__engblogs__get_content(limit: 50, offset: 50, includeContent: false)
```

### Use Cases
- Token-efficient browsing of titles before selecting articles
- Daily morning scan of new articles
- Filtering articles by reading status
- Finding articles from specific blogs or date ranges

### Token Efficiency

| Mode | Tokens per Article | Total for 50 Articles |
|------|-------------------|----------------------|
| Titles only (includeContent: false) | ~50 tokens | ~2,500 tokens |
| With excerpts (includeExcerpt: true) | ~200 tokens | ~10,000 tokens |
| Full content (includeContent: true) | ~2,000 tokens | ~100,000 tokens |

**Recommendation:** Always use `includeContent: false` for initial browsing, then fetch full content selectively with `get_article_full`.

---

## get_article_full

Fetch complete content for a specific article. Use sparingly after filtering.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `articleId` | Integer | Yes | Unique article identifier from `get_content` or `search_articles` |

### Returns

```json
{
  "articles": [
    {
      "id": 15910,
      "title": "Clojure Runs ONNX AI Models Now - Join the AI fun!",
      "content": "<p>Full HTML content of the article...</p>",
      "link": "http://dragan.rocks/articles/25/Clojure-Runs-ONNX-AI-Models-Now",
      "pubDate": "2025-10-26T15:56:00.000Z",
      "fetchDate": "2025-10-26T22:06:57.822Z",
      "status": "unread",
      "feedTitle": "Dragan Djuric",
      "feedCategory": "Engineering Blogs",
      "excerpt": "Article summary..."
    }
  ],
  "success": true
}
```

### Examples

**Fetch single article:**
```
mcp__engblogs__get_article_full(articleId: 15910)
```

**Typical workflow:**
```
# Step 1: Browse titles
articles = mcp__engblogs__get_content(limit: 50, includeContent: false)

# Step 2: Filter to interesting articles (locally)
selected_ids = [15910, 15744, 15830]

# Step 3: Fetch full content for selected articles only
for article_id in selected_ids:
    full_article = mcp__engblogs__get_article_full(articleId: article_id)
```

### Use Cases
- Selective deep-dive after filtering titles/excerpts
- Reading full article for detailed analysis
- Extracting technical details, code examples, benchmarks

### Token Considerations
- Single article: ~2,000-5,000 tokens depending on length
- Use only after filtering to maintain token efficiency
- Fetching 10 full articles: ~20,000-50,000 tokens
- Fetching 50 full articles: ~100,000-250,000 tokens (avoid this!)

---

## search_articles

Keyword search across article titles and content with advanced filtering.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `keyword` | String | **required** | Search term (case-insensitive, searches both title and content) |
| `limit` | Integer | 20 | Number of results to return |
| `offset` | Integer | 0 | Pagination offset |
| `category` | String | null | Filter by feed category (e.g., "Engineering", "AI") |
| `statuses` | Array | null | Filter by reading status |
| `startDate` | String | null | Start date for filtering (YYYY-MM-DD) |
| `endDate` | String | null | End date for filtering (YYYY-MM-DD) |
| `favoriteBlogsOnly` | Boolean | false | Only search favorite blogs |
| `prioritizeFavoriteBlogs` | Boolean | false | Prioritize favorite blog results |
| `includeContent` | Boolean | false | Include full article content in results |

### Returns

```json
{
  "articles": [
    {
      "id": 15910,
      "title": "Clojure Runs ONNX AI Models Now - Join the AI fun!",
      "excerpt": "Article preview with search term highlighted...",
      "link": "http://example.com/article",
      "pubDate": "2025-10-26T15:56:00.000Z",
      "status": "unread",
      "feedTitle": "Dragan Djuric",
      "feedCategory": "Engineering Blogs"
    }
  ],
  "total": 7939,
  "success": true
}
```

### Examples

**Basic keyword search:**
```
mcp__engblogs__search_articles(keyword: "GraphQL", limit: 10)
```

**Search with date range:**
```
mcp__engblogs__search_articles(
  keyword: "Kubernetes",
  startDate: "2025-10-01",
  endDate: "2025-10-26",
  limit: 20
)
```

**Search within category:**
```
mcp__engblogs__search_articles(
  keyword: "React",
  category: "Frontend",
  limit: 15
)
```

**Search favorites only:**
```
mcp__engblogs__search_articles(
  keyword: "performance",
  favoriteBlogsOnly: true,
  limit: 10
)
```

**Pagination for large result sets:**
```
# First 20 results
mcp__engblogs__search_articles(keyword: "AI", limit: 20, offset: 0)

# Next 20 results
mcp__engblogs__search_articles(keyword: "AI", limit: 20, offset: 20)
```

### Use Cases
- Topic-specific research ("GraphQL performance", "Rust async")
- Finding articles by technology or framework
- Discovering content by keywords
- Building reading lists on specific topics

---

## semantic_search

AI-powered natural language search using vector embeddings. Finds conceptually similar articles without exact keyword matches.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | String | **required** | Natural language description of desired content |
| `limit` | Integer | 10 | Number of results to return |
| `category` | String | null | Filter by feed category |
| `statuses` | Array | null | Filter by reading status |
| `includeContent` | Boolean | false | Include full article content |

### Requirements
- **OpenAI API key** must be configured in MCP server environment
- Works for articles from 2020+ (with generated embeddings)

### Returns

```json
{
  "articles": [
    {
      "id": 15910,
      "title": "Clojure Runs ONNX AI Models Now",
      "excerpt": "Article preview...",
      "similarity": 0.85,
      "link": "http://example.com/article",
      "pubDate": "2025-10-26T15:56:00.000Z",
      "status": "unread",
      "feedTitle": "Dragan Djuric",
      "feedCategory": "Engineering Blogs"
    }
  ],
  "success": true
}
```

### Examples

**Natural language concept search:**
```
mcp__engblogs__semantic_search(
  query: "articles about kubernetes performance optimization techniques",
  limit: 10
)
```

**Find similar implementation patterns:**
```
mcp__engblogs__semantic_search(
  query: "real-world examples of implementing GraphQL federation at scale",
  limit: 15
)
```

**Explore related concepts:**
```
mcp__engblogs__semantic_search(
  query: "how companies approach microservices monitoring and observability",
  limit: 10
)
```

### Use Cases
- Concept exploration without knowing exact keywords
- Finding related articles on similar topics
- Discovering implementation patterns and case studies
- Research when exact terminology is unclear

### Fallback Strategy
If semantic search is unavailable (missing API key):
```
# Fallback to keyword search with extracted keywords
mcp__engblogs__search_articles(keyword: "kubernetes performance", limit: 10)
```

---

## get_daily_digest

Fetch today's unread articles grouped by category. Perfect for morning briefings.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | Integer | 5 | Max articles per category |
| `includeContent` | Boolean | false | Include full article content |

### Returns

```json
{
  "articles": [
    {
      "id": 15748,
      "title": "Motion Highlights #14",
      "excerpt": "Freshly cherry-picked motion moments...",
      "link": "https://example.com/article",
      "pubDate": "2025-10-26T21:27:21.000Z",
      "status": "unread",
      "feedTitle": "Codrops",
      "feedCategory": "Engineering Blogs"
    }
  ],
  "total": 2,
  "success": true
}
```

### Examples

**Daily briefing (default):**
```
mcp__engblogs__get_daily_digest(limit: 3)
```

**Comprehensive briefing:**
```
mcp__engblogs__get_daily_digest(limit: 5)
```

### Use Cases
- Morning tech news briefing
- Daily catchup on unread articles
- Quick scan of today's publications
- Staying current without overwhelming detail

### Typical Workflow
```
# 1. Get today's digest
digest = mcp__engblogs__get_daily_digest(limit: 3)

# 2. Filter to interesting articles
selected = filter_by_relevance(digest.articles)

# 3. Fetch full content for promising articles
for article in selected:
    full = mcp__engblogs__get_article_full(articleId: article.id)

# 4. Mark articles as read after presentation
for article in digest.articles:
    mcp__engblogs__set_tag(articleId: article.id, status: "read")
```

---

## set_tag

Update article reading status for workflow management.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `articleId` | Integer | Yes | Article ID to update |
| `status` | String | Yes | New status: "unread" \| "read" \| "favorite" \| "archived" |

### Status Workflow

```
unread (default) → read (consumed) → favorite (bookmarked) → archived (hidden)
                      ↓
                   archived (skip)
```

### Returns

```json
{
  "success": true,
  "message": "Article 15910 status updated to favorite"
}
```

### Examples

**Mark article as read:**
```
mcp__engblogs__set_tag(articleId: 15910, status: "read")
```

**Bookmark as favorite:**
```
mcp__engblogs__set_tag(articleId: 15910, status: "favorite")
```

**Archive irrelevant article:**
```
mcp__engblogs__set_tag(articleId: 15910, status: "archived")
```

**Reset to unread:**
```
mcp__engblogs__set_tag(articleId: 15910, status: "unread")
```

### Use Cases
- Mark articles as read after consuming
- Bookmark reference material as favorites
- Archive noise or irrelevant content
- Build reading lists with favorites

### When to Tag Favorites

Tag as favorite when article:
- Contains reference material worth revisiting
- Presents comprehensive framework or methodology
- Includes detailed implementation guides
- Offers unique insights from experienced practitioners
- Contains valuable data/benchmarks for future reference

### Batch Tagging Example
```
# After presenting daily briefing, mark all as read
for article in presented_articles:
    mcp__engblogs__set_tag(articleId: article.id, status: "read")

# Tag high-value articles as favorites
for article in high_value_articles:
    mcp__engblogs__set_tag(articleId: article.id, status: "favorite")
```

---

## Token Efficiency Comparison

| Operation | Approach | Tokens Used | Savings |
|-----------|----------|-------------|---------|
| Browse 50 articles | Full content | ~100,000 | 0% |
| Browse 50 articles | Titles only | ~2,500 | 97.5% |
| Browse + selective (10 full) | Hybrid | ~22,500 | 77.5% |
| Browse + selective (5 full) | Hybrid | ~12,500 | 87.5% |

**Recommendation:** Use the hybrid approach (browse titles → filter → selective deep-dive) to achieve 70-90% token savings while maintaining content quality.

---

## Pagination Best Practices

All listing tools support pagination:

**1. Initial browse with pagination:**
```
# Browse first 50
page1 = mcp__engblogs__get_content(limit: 50, offset: 0)

# If user wants more, fetch next page
page2 = mcp__engblogs__get_content(limit: 50, offset: 50)
```

**2. Search with pagination:**
```
# First 20 results
results = mcp__engblogs__search_articles(keyword: "GraphQL", limit: 20, offset: 0)

# Next 20 results
more_results = mcp__engblogs__search_articles(keyword: "GraphQL", limit: 20, offset: 20)
```

**3. Source discovery:**
```
# Browse first 50 sources
sources = mcp__engblogs__get_sources(limit: 50, offset: 0)

# Continue browsing
more_sources = mcp__engblogs__get_sources(limit: 50, offset: 50)
```

**When to use pagination:**
- User asks to "see more" or "show more articles"
- Building comprehensive topic research
- Browsing specific categories or sources
- Initial results don't satisfy user's query

---

## Error Handling

### Common Errors

**1. MCP Server Offline**
```
Error: Unable to connect to engblogs MCP server
Solution: Check server status, restart if needed
```

**2. Database Connection Failed**
```
Error: Database connection error
Solution: Verify PostgreSQL running on port 5433
```

**3. Invalid Article ID**
```
Error: Article not found
Solution: Use valid article ID from get_content/search_articles
```

**4. Semantic Search Unavailable**
```
Error: Semantic search requires OpenAI API key
Solution: Configure API key or fallback to keyword search
```

### Graceful Degradation

```
# Try semantic search first
try:
    results = mcp__engblogs__semantic_search(query: "kubernetes optimization")
except:
    # Fallback to keyword search
    results = mcp__engblogs__search_articles(keyword: "kubernetes optimization")
```

---

## Quick Reference Cheat Sheet

| Task | Tool | Example |
|------|------|---------|
| Browse recent articles | get_content | `get_content(limit: 50, includeContent: false)` |
| Get full article | get_article_full | `get_article_full(articleId: 15910)` |
| Keyword search | search_articles | `search_articles(keyword: "GraphQL", limit: 10)` |
| Concept search | semantic_search | `semantic_search(query: "k8s performance", limit: 10)` |
| Daily briefing | get_daily_digest | `get_daily_digest(limit: 3)` |
| List sources | get_sources | `get_sources(limit: 50, offset: 0)` |
| Mark as read | set_tag | `set_tag(articleId: 15910, status: "read")` |
| Mark as favorite | set_tag | `set_tag(articleId: 15910, status: "favorite")` |

---

## Database Statistics

- **Total Articles:** 15,910+ (as of 2025-10-26)
- **Total Sources:** 518+ RSS feeds
- **Categories:** Engineering Blogs, AI Research, Frontend, Backend, Cloud, etc.
- **Update Frequency:** Every 60 minutes (configurable)
- **Article Retention:** All historical articles available
