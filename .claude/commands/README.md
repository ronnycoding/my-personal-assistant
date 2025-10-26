# Slash Commands

Quick utility commands for faster access to tech news curator and productivity features.

## Tech News Commands

### `/ai`
Get latest AI and machine learning news.

**Usage:**
```
/ai
```

**What it does:** Shows recent AI/ML developments from authoritative sources

---

### `/tech`
Get today's general tech news across all categories.

**Usage:**
```
/tech
```

**What it does:** Shows tech news from AI/ML, backend, frontend, cloud, and devtools

---

### `/briefing`
Get comprehensive morning tech briefing.

**Usage:**
```
/briefing
```

**What it does:** Organized daily digest with top articles by category and action items

---

### `/backend`
Get recent backend engineering news.

**Usage:**
```
/backend
```

**What it does:** Shows articles about databases, APIs, microservices, distributed systems

---

### `/frontend`
Get recent frontend development news.

**Usage:**
```
/frontend
```

**What it does:** Shows articles about React, Vue, performance, UX, build tools

---

### `/cloud`
Get recent cloud and infrastructure news.

**Usage:**
```
/cloud
```

**What it does:** Shows articles about Kubernetes, AWS, serverless, DevOps

---

### `/search [topic]`
Search for articles about a specific topic.

**Usage:**
```
/search "GraphQL performance"
/search "Kubernetes security"
/search "React hooks"
```

**What it does:** Searches engineering blogs for specific topics with semantic and keyword search

---

### `/weekly`
Get comprehensive weekly tech digest.

**Usage:**
```
/weekly
```

**What it does:** Summary of the most important tech developments from the last 7 days

---

## Productivity Commands

### `/inbox`
Check email inbox status.

**Usage:**
```
/inbox
```

**What it does:** Shows unread, actionable, and priority messages from the last 24-48 hours

---

### `/calendar`
View today's schedule and upcoming events.

**Usage:**
```
/calendar
```

**What it does:** Shows calendar events with times, locations, and attendees

---

### `/tasks`
View tasks and reminders.

**Usage:**
```
/tasks
```

**What it does:** Shows tasks organized by priority and due date from Reminders app

---

### `/morning`
Get complete morning briefing.

**Usage:**
```
/morning
```

**What it does:** Comprehensive briefing combining calendar events, email status, and reminders for the day

---

## How Slash Commands Work

Slash commands are shortcuts that expand into full prompts. When you type `/ai`, Claude Code automatically expands it to "What's new in AI? Show me the latest AI and machine learning developments."

### Creating Your Own Commands

Add new commands by creating `.md` files in `.claude/commands/`:

```markdown
# My Command

[Your prompt here]
```

**File:** `.claude/commands/mycommand.md`
**Usage:** `/mycommand`

### Command Parameters

Use `$1`, `$2`, etc. for parameters:

```markdown
# Search Command

Search for articles about: $1
```

**Usage:** `/search "topic"`

---

## Tips

1. **Chain commands:** You can run multiple commands in sequence
   ```
   /ai
   /backend
   ```

2. **Combine with questions:** Add follow-up questions after commands
   ```
   /briefing

   Then tell me more about the Netflix article
   ```

3. **Customize prompts:** Edit the `.md` files to adjust what each command does

---

## Available Skills

These commands leverage the following skills:

- **tech-news-curator** - AI & Tech Trends Intelligence Assistant
- **daily-briefing** - Morning productivity briefing (calendar + email + reminders)
- **scan-inbox** - Email triage
- **read-calendar** - Calendar events
- **list-reminders** - Task management

---

## Examples

### Quick AI Check
```
/ai
```
→ Get latest AI news in <10 seconds

### Morning Routine
```
/briefing
```
→ Complete tech briefing with action items

### Deep Research
```
/search "microservices patterns"
```
→ Find relevant articles with full analysis

### Category Focus
```
/frontend
```
→ Just frontend news, filtered and analyzed

### Check Email
```
/inbox
```
→ Quick inbox triage in seconds

### Plan Your Day
```
/morning
```
→ Complete briefing: calendar + email + tasks

---

## Keyboard Shortcuts

- Type `/` to see available commands
- Press `Tab` to autocomplete command names
- Use `↑` and `↓` to browse command history

---

For more information, see:
- [Tech News Curator Skill](../skills/tech-news-curator/SKILL.md)
- [Skills README](../skills/README.md)
- [Claude Code Commands Documentation](https://docs.claude.com/en/docs/claude-code/slash-commands)
