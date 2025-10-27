# Tech Digest Formatting Standards

This document defines the standard format for presenting tech news digests using the `tech-news-curator` managed skill and the `engblogs` MCP server.

## Core Principle

**ALWAYS include article links as clickable sources.** The MCP provides links in all responses—use them.

## Standard Article Format

Every article mention must include:

1. **Title** (as clickable link)
2. **Source blog name**
3. **Publication date**
4. **Summary/excerpt** (optional, based on context)

### Basic Format

```markdown
**[Article Title](https://link-to-article.com)**
*Source Blog • Month DD, YYYY*
```

### With Summary

```markdown
**[Article Title](https://link-to-article.com)**
*Source Blog • Month DD, YYYY*

Brief summary or key points...
```

## Weekly Digest Format

### Section Headers

Group articles by topic/category with clear sections:

```markdown
## 🚀 Category Name

### **Subcategory or Company**

**[First Article Title](https://link1.com)**
*Blog Name • October 23, 2025*

**[Second Article Title](https://link2.com)**
*Blog Name • October 24, 2025*

Key insights:
- Point 1
- Point 2
- Point 3
```

### Example: Proper Weekly Digest Entry

```markdown
## 🤖 AI & Machine Learning

### **Vercel's Agent Platform Launch**

**[Built-in durability: Introducing Workflow Development Kit](https://vercel.com/blog/introducing-workflow)**
*Vercel • October 23, 2025*

**[Introducing Vercel Agent: Your new Vercel teammate](https://vercel.com/blog/introducing-vercel-agent)**
*Vercel • October 23, 2025*

**[You can just ship agents](https://vercel.com/blog/you-can-just-ship-agents)**
*Vercel • October 23, 2025*

Key developments:
- WDK makes durability a language-level concept
- Vercel Agent provides AI-powered code review and investigations
- Zero-config backends for AI workloads
```

## Deep Dive Format

When providing detailed analysis of specific articles:

### Article Reference Header

```markdown
## 📖 [Article Title](https://link-to-article.com)

**Source:** Blog Name
**Published:** October 23, 2025
**Topics:** AI, Agents, Infrastructure

### Summary
Brief overview...

### Key Technical Details
- Detail 1
- Detail 2

### Analysis
Your insights...

### Related Articles
- [Related Article 1](link1)
- [Related Article 2](link2)
```

### Example: Proper Deep Dive

```markdown
## 📖 [Built-in durability: Introducing Workflow Development Kit](https://vercel.com/blog/introducing-workflow)

**Source:** Vercel Blog
**Published:** October 23, 2025
**Topics:** Distributed Systems, AI Agents, Developer Tools

### Summary
Vercel introduces WDK, an open-source TypeScript framework that makes durability a language-level concept for async functions. Functions can pause for extended periods, survive crashes, and resume exactly where they stopped.

### The Problem
Building reliable async functions (AI agents, data pipelines) traditionally requires:
- Message queues (Kafka, RabbitMQ)
- Custom retry logic
- Persistence layers
- State management

Infrastructure setup often exceeds actual business logic development time.

### Key Innovation
**Durability as a first-class language feature:**
- Functions pause/resume transparently
- No manual state management
- Survives deployments and crashes
- Framework/platform agnostic

### Related Announcements
- [Introducing Vercel Agent](https://vercel.com/blog/introducing-vercel-agent)
- [Zero-config backends on Vercel AI Cloud](https://vercel.com/blog/zero-config-backends-on-vercel-ai-cloud)
```

## MCP Response Field Mapping

All MCP engblogs methods return these fields—**always use them**:

### Available Fields
```javascript
{
  id: number,              // Article ID
  title: string,           // Article title
  link: string,            // ⭐ ALWAYS INCLUDE THIS
  pubDate: string,         // ISO date
  feedTitle: string,       // Source blog name
  feedCategory: string,    // Category
  excerpt: string,         // Summary
  content: string,         // Full content (if requested)
  status: string          // read/unread/favorite/archived
}
```

### Format Link As

```markdown
**[{title}]({link})**
*{feedTitle} • {formatted_pubDate}*

{excerpt or analysis}
```

## Quick Reference Templates

### Single Article

```markdown
**[{title}]({link})**
*{feedTitle} • {date}*
```

### Article List

```markdown
1. **[Title 1](link1)** - *Source 1 • Date 1*
2. **[Title 2](link2)** - *Source 2 • Date 2*
3. **[Title 3](link3)** - *Source 3 • Date 3*
```

### Grouped by Source

```markdown
### Source Name

- **[Article 1](link1)** - *Oct 23, 2025*
- **[Article 2](link2)** - *Oct 24, 2025*
- **[Article 3](link3)** - *Oct 25, 2025*
```

### With Excerpts

```markdown
**[Article Title](link)**
*Source • Date*

> Excerpt or summary text here...
```

## Anti-Patterns (DON'T DO THIS)

### ❌ Missing Links
```markdown
**Vercel introduces WDK**
A new framework for durability...
```

### ❌ Link Without Context
```markdown
https://vercel.com/blog/introducing-workflow
```

### ❌ Generic "Read more"
```markdown
Check out this article about Vercel's new framework.
[Read more](link)
```

## Correct Patterns (DO THIS)

### ✅ Complete Attribution
```markdown
**[Built-in durability: Introducing Workflow Development Kit](https://vercel.com/blog/introducing-workflow)**
*Vercel • October 23, 2025*
```

### ✅ Descriptive Context
```markdown
Vercel's new Workflow Development Kit brings durability to async functions:
**[Introducing Workflow Development Kit](https://vercel.com/blog/introducing-workflow)**
*Vercel • October 23, 2025*
```

## Footer Recommendations

Always end digests with actionable follow-ups:

```markdown
---

**170 articles** tracked this week from engineering blogs.

**Explore more:**
- [Full article list](#) with all links
- Filter by: [AI/ML](#) • [Infrastructure](#) • [Frontend](#)
- Mark as [read](#) or [favorite](#)

**Want to dive deeper?**
Ask me to fetch full content from any article link above.
```

## Usage in Slash Commands

When creating slash commands that use the `engblogs` MCP:

```bash
# /weekly command should output:
## 🗓️ Weekly Tech Digest

[...grouped articles with links...]

**Total:** 170 unread articles
**Read full articles:** Click any link above
```

## Testing Your Format

Before presenting a digest, verify:

- [ ] Every article has a clickable link
- [ ] Source blog name is visible
- [ ] Publication date is formatted (not ISO string)
- [ ] Links use markdown format: `[title](url)`
- [ ] No broken or placeholder links
- [ ] Footer includes article count and next actions

## Version History

- **v1.0** (2025-10-26): Initial standards document
  - Defined link inclusion requirement
  - Created format templates
  - Added anti-patterns guide
