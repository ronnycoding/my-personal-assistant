# Gemini Agent Configuration

This directory contains Gemini-specific configurations for AI-powered personal productivity and tech news curation.

## Directory Structure

```
.gemini/
├── commands/          # TOML command definitions with embedded instructions
├── scripts/          # AppleScript utilities for macOS automation
└── README.md         # This file
```

## Architecture

Unlike Claude Code which supports a separate skills directory structure, Gemini requires **self-contained command files** that include:
- Script references (`.gemini/scripts/*.scpt`)
- Complete skill instructions embedded in `instruction` field
- Usage examples and parameters
- Error handling and requirements

**Key Principle:** Everything Gemini needs is in the command TOML file - no external skill files needed.

## Commands

Commands are TOML files that define prompts, skills, and execution instructions:

### Personal Productivity

- **`tasks.toml`** - List reminders from macOS Reminders app
- **`calendar.toml`** - Read calendar events with recurring event support
- **`inbox.toml`** - Scan and triage Apple Mail inbox
- **`morning.toml`** - Comprehensive daily briefing (calendar + email + tasks)

### Tech News & Learning

- **`tech.toml`** - Today's tech news across all categories
- **`tech-briefing.toml`** - Comprehensive tech digest
- **`ai.toml`** - Latest AI/ML developments
- **`backend.toml`** - Backend engineering articles
- **`frontend.toml`** - Frontend development news
- **`cloud.toml`** - Cloud & infrastructure updates
- **`search.toml`** - Search for specific technical topics
- **`weekly.toml`** - Weekly tech digest

## Scripts

AppleScript utilities for macOS automation (stored in `scripts/`):

### `list_tasks.scpt`
Lists tasks from macOS Reminders organized by priority and due date.

**Usage:**
```bash
osascript .gemini/scripts/list_tasks.scpt
```

**Returns:**
- Total task count
- Overdue tasks
- Today's tasks
- All incomplete tasks with metadata

**Associated Command:** `tasks.toml`

---

### `read_events.scpt`
Reads calendar events for a specified date range.

**Usage:**
```bash
osascript .gemini/scripts/read_events.scpt <start_date> <end_date>
```

**Example:**
```bash
osascript .gemini/scripts/read_events.scpt 2025-10-28 2025-10-29
```

**Parameters:**
- `start_date` - ISO format (YYYY-MM-DD)
- `end_date` - ISO format (YYYY-MM-DD)

**Returns:**
- Events with title, times, location, calendar name
- Recurring event detection

**Associated Command:** `calendar.toml`

**Note:** For better recurring event handling, use `icalBuddy`:
```bash
brew install ical-buddy
icalBuddy -n -iep "title,datetime,location" -df "%Y-%m-%d" -tf "%H:%M" eventsFrom:2025-10-28 to:2025-10-29
```

---

### `scan_inbox.scpt`
Scans Apple Mail inbox for unread, actionable, and priority messages.

**Usage:**
```bash
osascript .gemini/scripts/scan_inbox.scpt <hours> <priority_only>
```

**Example:**
```bash
osascript .gemini/scripts/scan_inbox.scpt 48 false
```

**Parameters:**
- `hours` - Lookback period (e.g., 24, 48, 72)
- `priority_only` - Boolean (true/false)

**Returns:**
- Unread message count
- Actionable items (keywords: deadline, urgent, meeting, etc.)
- Priority/flagged messages
- Message details (sender, subject, date)

**Associated Command:** `inbox.toml`

**Actionable Keywords Detected:**
- deadline, urgent, action required
- meeting, request, please review
- asap, todo, action item

## Command Structure

All command files follow this TOML format:

```toml
prompt = "User-facing prompt description"
skill = "skill-name"
instruction = """
# Skill Name

## When to Use
- Example queries...

## Requirements
- Dependencies...

## Instructions
### Step 1: Execute Script
```bash
osascript .gemini/scripts/script_name.scpt [args]
```

### Step 2: Process Results
- How to handle output...

### Step 3: Present to User
- Formatting guidelines...
"""
```

## Integration with MCP Tools

Tech news commands integrate with the `engblogs` MCP server for curated engineering content:

- `mcp__engblogs__get_daily_digest` - Today's unread articles by category
- `mcp__engblogs__search_articles` - Search by keyword/category
- `mcp__engblogs__semantic_search` - AI-powered semantic search
- `mcp__engblogs__get_weekly_favorites` - Favorite articles from last 7 days

## Usage Notes

1. **Script Paths:** All commands reference scripts using `.gemini/scripts/` prefix
2. **Self-Contained:** Commands include full instructions since Gemini doesn't support separate skill files
3. **Requirements:** Some skills require `icalBuddy` for enhanced calendar functionality
4. **Permissions:** Scripts require macOS automation permissions for Mail, Calendar, and Reminders

## Permissions Setup

Grant automation permissions in **System Settings → Privacy & Security → Automation**:

- **Terminal/Gemini** → Calendar
- **Terminal/Gemini** → Reminders
- **Terminal/Gemini** → Mail

## Comparison with Claude Code

| Feature | Claude Code | Gemini |
|---------|-------------|--------|
| Skill Structure | `.claude/skills/SKILL.md` | Embedded in `.gemini/commands/*.toml` |
| Script Location | `.claude/skills/*/scripts/` | `.gemini/scripts/` (centralized, flat) |
| Documentation | Separate SKILL.md files | Inline `instruction` field in commands |
| Command Invocation | Built-in skill system | Self-contained TOML commands |
| Skill Discovery | Automatic via SKILL.md frontmatter | Direct command files only |

**Why Different?**
- Claude Code has native skill support → separate documentation files
- Gemini requires everything in command files → embedded instructions
- Gemini's simpler, flatter structure → easier maintenance

## Development

When adding new capabilities:

1. Create AppleScript in `.gemini/scripts/`
2. Create command TOML in `.gemini/commands/` with complete embedded instructions
3. Test script execution and error handling
4. Update this README with script documentation

## Examples

### Morning Briefing
```bash
# Combines calendar, email, and tasks
.gemini/commands/morning.toml
```

### Check Email
```bash
# Scan inbox from last 48 hours
osascript .gemini/scripts/scan_inbox.scpt 48 false
```

### Today's Schedule
```bash
# Using icalBuddy (recommended)
TODAY=$(date +%Y-%m-%d)
icalBuddy -n -iep "title,datetime,location" -df "%Y-%m-%d" -tf "%H:%M" eventsFrom:"$TODAY" to:"$TODAY"

# Using AppleScript (fallback)
osascript .gemini/scripts/read_events.scpt $TODAY $TODAY
```

### List Tasks
```bash
osascript .gemini/scripts/list_tasks.scpt
```

## See Also

- [Claude Code Configuration](../.claude/CLAUDE.md)
- [Agents Documentation](../agents/README.md)
