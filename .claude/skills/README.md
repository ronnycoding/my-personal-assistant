# Skills Directory

Personal productivity skills for Claude Code using AppleScript automation.

## Active Skills

### scan-inbox
**Purpose**: Scan Apple Mail inbox for unread, actionable, and priority messages

**Files**:
- `SKILL.md` - Main skill definition
- `reference.md` - Technical details
- `examples.md` - Usage examples
- `scripts/scan_inbox.scpt` - AppleScript implementation

**Usage**: Activated when you ask Claude to check your email, show unread messages, or triage your inbox.

### read-calendar
**Purpose**: Read macOS Calendar events for a specified date range

**Files**:
- `SKILL.md` - Main skill definition
- `examples.md` - Usage examples
- `scripts/read_events.scpt` - AppleScript implementation

**Usage**: Activated when you ask about your schedule, meetings, or calendar.

### list-reminders
**Purpose**: List tasks from macOS Reminders organized by priority and due date

**Files**:
- `SKILL.md` - Main skill definition
- `scripts/list_tasks.scpt` - AppleScript implementation

**Usage**: Activated when you ask about your to-do list, tasks, or reminders.

### daily-briefing
**Purpose**: Comprehensive daily briefing combining calendar, email, and tasks

**Files**:
- `SKILL.md` - Main skill definition with orchestration instructions
- `examples.md` - Briefing examples

**Usage**: Activated when you ask to plan your day, get a morning briefing, or want an overview.

### tech-news-curator
**Purpose**: Curate and analyze technical articles from engineering blogs about AI, software engineering, and emerging tech trends

**Files**:
- `SKILL.md` - Main skill definition with MCP tools integration
- `reference.md` - Complete MCP tools documentation
- `examples.md` - Article presentations and workflows

**Usage**: Activated when you ask about tech news, AI updates, engineering blogs, new frameworks, industry trends, or want a daily tech briefing. Uses the engblogs MCP server for RSS feed aggregation.

## How Skills Work

Skills are automatically discovered and invoked by Claude based on your requests. Each skill:

1. **Has a clear description** in SKILL.md frontmatter that tells Claude when to use it
2. **Includes step-by-step instructions** for Claude to follow
3. **Uses allowed-tools** to safely execute operations (mainly Bash for AppleScript)
4. **Returns structured data** that Claude formats for you

## Skill Structure

Each skill follows this pattern:

```
skill-name/
├── SKILL.md (required) - Skill definition with YAML frontmatter
├── reference.md (optional) - Technical documentation
├── examples.md (optional) - Usage examples
└── scripts/ (optional) - Supporting AppleScript files
    └── script_name.scpt
```

## Creating New Skills

To create a new skill:

1. Create a directory: `.claude/skills/your-skill-name/`
2. Add `SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: What it does and when to use it
   allowed-tools: Bash
   ---
   ```
3. Add instructions for Claude
4. Optionally add supporting files (reference.md, examples.md, scripts/)

See [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills) for details.

## Testing Skills

### Test Individual Scripts

```bash
# Scan inbox
osascript .claude/skills/scan-inbox/scripts/scan_inbox.scpt 24 false

# Read calendar
osascript .claude/skills/read-calendar/scripts/read_events.scpt "2025-10-26" "2025-10-26"

# List reminders
osascript .claude/skills/list-reminders/scripts/list_tasks.scpt
```

### Test Skills with Claude

Just ask Claude naturally:

**Productivity Skills:**
- "Check my email"
- "What's on my calendar today?"
- "Show me my to-do list"
- "Give me my morning briefing"

**Tech News Curator:**
- "What's new in AI?"
- "Show me tech news today"
- "Find articles about GraphQL performance"
- "Give me my morning tech briefing"

Claude will automatically activate the appropriate skill(s).

## Requirements

### System Dependencies

Install `icalBuddy` for proper recurring event support:
```bash
brew install ical-buddy
```

**Why icalBuddy?** macOS Calendar via AppleScript doesn't pre-generate future instances of recurring events, so weekly/monthly meetings won't appear when querying future dates. icalBuddy properly expands recurring events, ensuring you see all upcoming meetings including recurring ones.

### macOS Permissions

All skills require macOS automation permissions:

**System Settings → Privacy & Security → Automation → Terminal/Claude**
- ✅ Mail
- ✅ Calendar
- ✅ Reminders

Verify permissions:
```bash
./tests/framework/verify_permissions.sh
```

## Troubleshooting

### Skill Not Activating

1. Check description is specific about when to use it
2. Verify SKILL.md has valid YAML frontmatter
3. Ask Claude directly: "Use the scan-inbox skill"

### Permission Errors

Run permission verification:
```bash
./tests/framework/verify_permissions.sh
```

### Script Errors

Test scripts directly to isolate issues:
```bash
osascript .claude/skills/SKILL-NAME/scripts/script.scpt [args]
```

## Next Steps

- Add more specialized skills
- Create workflows combining multiple skills
- Implement advanced features (flagging, organizing, etc.)

## Resources

- [Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [AppleScript Language Guide](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/)
- [Project Issues](https://github.com/ronnycoding/my-personal-assistant/issues)
