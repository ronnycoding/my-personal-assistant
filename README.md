# My Personal Agents

Personal AI agents collection using Claude Code - productivity automation, AppleScript skills, and custom workflows for macOS.

## Overview

This repository contains specialized AI agents designed to automate personal productivity tasks across macOS applications using AppleScript automation.

## Current Agents

### Productivity Assistant
Unified command center for daily organization across Apple Mail, macOS Calendar, Reminders, and other productivity apps.

**Key Capabilities:**
- **Email Management** - Scan Apple Mail for actionable items, deadlines, meeting requests
- **Calendar Intelligence** - Read macOS Calendar for events and availability
- **Task Orchestration** - Read macOS Reminders to surface today's priorities
- **Daily Planning** - Morning briefings and evening reviews

## Repository Structure

```
my-personal-agents/
├── .claude/
│   ├── agents/           # Agent definitions
│   │   └── productivity-agent.md
│   └── skills/           # AppleScript automations
│       ├── apple-mail/   # Apple Mail automation
│       ├── calendar/     # macOS Calendar automation
│       ├── reminders/    # macOS Reminders automation
│       └── meetings/     # Meeting scheduling workflows
├── tests/                # AppleScript test suites
└── docs/                 # Documentation
```

## Skills Organization

Skills are organized by macOS application domain:

- **apple-mail/** - Email scanning, parsing, and organization
- **calendar/** - Event reading, conflict detection, time suggestions
- **reminders/** - Task management and cross-referencing
- **meetings/** - Meeting scheduling and availability finding

## Setup Requirements

**Permissions Required:**
- System Settings → Privacy & Security → Automation → Terminal (or Claude app)
  - Enable: Mail, Calendar, Reminders
- System Settings → Privacy & Security → Full Disk Access (if needed for Mail database)

**MCP Servers:**
- macOS control (osascript tool)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/ronnycoding/my-personal-agents.git

# Navigate to the project
cd my-personal-agents

# Review available agents
ls .claude/agents/

# Review available skills
ls .claude/skills/
```

## Usage Examples

**Daily Planning:**
```
"Review my schedule for today and create a prioritized task list
based on calendar events, emails from the last 24hrs, and existing reminders"
```

**Email Triage:**
```
"Check my unread email and create reminders for anything actionable"
```

**Time Management:**
```
"Find me 2 hours of focus time this week for deep work"
```

**Meeting Prep:**
```
"What's my next meeting and what should I prepare?"
```

## Development

Each skill is a tested AppleScript file (`.scpt`) that can be invoked by agents using Claude's Skills API.

**AppleScript Syntax Notes:**
- Date arithmetic: Use `days`, `hours`, `minutes` directly (not `1 * days`)
- Comparison operators: Use `≥` and `≤` (or `>=` and `<=`)
- String concatenation: Use `&` operator
- Error handling: Wrap calendar/reminder loops in `try` blocks
- Time zones: AppleScript uses system timezone (America/Costa_Rica)

## Contributing

This is a personal repository. For issues and feature requests, please use GitHub Issues.

## License

Private - Personal Use Only
