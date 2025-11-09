# My Personal Assistant

Personal AI assistant supporting **Claude Code** and **Gemini CLI** - productivity automation, AppleScript skills, and custom workflows for macOS.

## Overview

This repository contains specialized AI agents designed to automate personal productivity tasks across macOS applications using AppleScript automation. The configuration supports both Claude Code's skill-based architecture and Gemini's command-based system.

## Current Agents

### Productivity Assistant
Unified command center for daily organization across Apple Mail, macOS Calendar, Reminders, and other productivity apps.

**Key Capabilities:**
- **Email Management** - Scan Apple Mail for actionable items, deadlines, meeting requests
- **Calendar Intelligence** - Read macOS Calendar for events and availability
- **Task Orchestration** - Read macOS Reminders to surface today's priorities
- **Daily Planning** - Morning briefings and evening reviews

### Personal Finance Advisor
AI-powered financial management using Jupyter notebooks for analysis, projections, and recommendations.

**Key Capabilities:**
- **Financial Analysis** - Income, expenses, cash flow, net worth, savings metrics
- **Smart Budgeting** - Budget tracking, variance analysis, category insights
- **Projections** - 12-month forecasts, savings goals, retirement planning, debt payoff
- **AI Advisory** - Context-aware recommendations for savings, budgeting, and goals
- **Visualizations** - Interactive charts for trends, categories, and projections
- **Data Privacy** - All data stays local, fully encrypted, gitignored

[📖 See Finance Documentation](docs/FINANCE.md) | [🚀 Quick Start](docs/finance/QUICK_START.md)

## Repository Structure

```
my-personal-assistant/
├── .claude/              # Claude Code configuration
│   ├── commands/         # Slash commands for quick access
│   │   ├── morning.md    # Daily briefing (calendar + email + tasks)
│   │   ├── inbox.md      # Intelligent email scanning
│   │   ├── calendar.md   # Calendar events viewer
│   │   ├── tasks.md      # Reminders/tasks organizer
│   │   ├── finance.md    # Personal finance management
│   │   ├── tech.md       # Tech news across categories
│   │   ├── ai.md         # AI/ML news
│   │   ├── backend.md    # Backend engineering news
│   │   ├── frontend.md   # Frontend development news
│   │   ├── cloud.md      # Cloud/infrastructure news
│   │   ├── tech-briefing.md # Morning tech digest
│   │   ├── weekly.md     # Weekly tech digest
│   │   └── search.md     # Search technical articles
│   ├── agents/           # Specialized agent submodules
│   ├── skills/           # AppleScript automations (skill structure)
│   │   ├── scan-inbox/   # Apple Mail inbox scanning
│   │   ├── read-calendar/ # macOS Calendar events
│   │   ├── list-reminders/ # macOS Reminders tasks
│   │   ├── daily-briefing/ # Morning briefing orchestration
│   │   └── tech-news-curator/ # Engineering blog curation
│   └── templates/        # GitHub PR/issue templates
│
├── .gemini/              # Gemini CLI configuration
│   ├── commands/         # TOML command files (self-contained)
│   │   ├── tasks.toml, calendar.toml, inbox.toml
│   │   ├── morning.toml  # Daily briefing
│   │   └── tech.toml, ai.toml, backend.toml, etc.
│   ├── scripts/          # Centralized AppleScript files
│   │   ├── list_tasks.scpt
│   │   ├── read_events.scpt
│   │   └── scan_inbox.scpt
│   └── README.md         # Gemini-specific documentation
│
├── tests/                # AppleScript test suites
└── docs/                 # Documentation
```

## Claude Code vs Gemini CLI

This repository supports both AI coding assistants with optimized configurations for each:

| Feature | Claude Code | Gemini CLI |
|---------|-------------|------------|
| **Configuration** | `.claude/` | `.gemini/` |
| **Skills** | Separate `SKILL.md` files | Embedded in command TOML files |
| **Scripts** | Distributed in skill directories | Centralized in `scripts/` |
| **Commands** | Built-in skill system | Self-contained TOML commands |
| **Documentation** | Skill-level markdown files | Inline instructions in commands |
| **Best For** | Complex workflows, agent orchestration | Quick commands, flat structure |

**Key Differences:**
- **Claude Code** uses `.claude/skills/` with structured SKILL.md documentation
- **Gemini** uses `.gemini/commands/` with all instructions embedded in TOML files
- **Scripts are identical** - both use the same AppleScript implementations
- **Capabilities are the same** - both provide identical functionality

## Skills & Commands

### Core Capabilities

Both Claude Code and Gemini provide the same productivity features:

**Personal Productivity:**
- 📧 **Inbox Scanning** - Apple Mail triage with job opportunity detection
- 📅 **Calendar Reading** - macOS Calendar events with recurring support
- ✅ **Task Management** - macOS Reminders organized by priority
- 🌅 **Daily Briefing** - Morning planning (calendar + email + tasks)
- 📰 **Tech News** - Engineering blog curation via MCP server
- 💰 **Personal Finance** - Financial analysis, budgeting, and AI advisory via Jupyter notebooks

**Organization:**
- **Claude Code** - Organized by skill directories (`.claude/skills/`)
- **Gemini CLI** - Organized by command files (`.gemini/commands/`)

### Available Skills/Commands

| Capability | Claude Code Skill | Gemini Command | Description |
|------------|------------------|----------------|-------------|
| Email Triage | `scan-inbox` | `inbox.toml` | Scan Apple Mail for actionable items |
| Calendar Events | `read-calendar` | `calendar.toml` | Read macOS Calendar with recurring events |
| Task List | `list-reminders` | `tasks.toml` | List macOS Reminders by priority |
| Morning Briefing | `daily-briefing` | `morning.toml` | Orchestrated daily planning |
| Tech News | `tech-news-curator` | `tech.toml`, `ai.toml`, etc. | Engineering blog curation |
| Personal Finance | `/finance` command | N/A | Financial analysis & budgeting via Jupyter |

## Claude Code Slash Commands

Slash commands provide quick access to common workflows. Type `/` in Claude Code to see all available commands.

**How to Use:**
- Simply type the command in Claude Code chat (e.g., `/morning`)
- Commands automatically execute their workflow
- Some commands accept parameters (e.g., `/finance init --notebook="name"`)
- Tab completion available - type `/` to see suggestions

### Productivity Commands

| Command | Description | Example Usage |
|---------|-------------|---------------|
| `/morning` | Complete morning briefing with calendar, email, and tasks | `/morning` |
| `/inbox` | Intelligent email scanning with job opportunity detection | `/inbox` |
| `/calendar` | Show today's calendar events and upcoming schedule | `/calendar` |
| `/tasks` | List tasks and reminders organized by priority | `/tasks` |

### Finance Commands

| Command | Description | Example Usage |
|---------|-------------|---------------|
| `/finance init` | Create new financial analysis notebook | `/finance init --notebook="2025-budget"` |
| `/finance import` | Import transaction data from CSV/Excel | `/finance import --source="file.csv"` |
| `/finance analyze` | Analyze financial data and calculate metrics | `/finance analyze --type="overview"` |
| `/finance project` | Generate financial projections and forecasts | `/finance project --months=12` |
| `/finance advise` | Get AI-driven financial recommendations | `/finance advise --focus="savings"` |
| `/finance report` | Create visualizations and reports | `/finance report --type="income-expense"` |
| `/finance list` | List all existing financial notebooks | `/finance list` |

### Tech News Commands

| Command | Description | Example Usage |
|---------|-------------|---------------|
| `/tech` | Tech news across all categories (AI, backend, frontend, cloud) | `/tech` |
| `/ai` | Latest AI and machine learning developments | `/ai` |
| `/backend` | Backend engineering articles (databases, APIs, distributed systems) | `/backend` |
| `/frontend` | Frontend development articles (React, Vue, performance) | `/frontend` |
| `/cloud` | Cloud and infrastructure articles (Kubernetes, AWS, DevOps) | `/cloud` |
| `/tech-briefing` | Comprehensive morning tech briefing by category | `/tech-briefing` |
| `/weekly` | Weekly tech digest from the last 7 days | `/weekly` |
| `/search` | Search for technical articles about specific topics | `/search "GraphQL performance"` |

## Setup Requirements

### macOS Permissions

**Both Claude Code and Gemini require:**
- System Settings → Privacy & Security → Automation → Terminal (or respective app)
  - ✅ Enable: Mail, Calendar, Reminders
- System Settings → Privacy & Security → Full Disk Access (if needed for Mail database)

### Optional Tools

**For Enhanced Calendar Support:**
```bash
brew install ical-buddy
```

icalBuddy provides better recurring event handling than AppleScript.

### MCP Servers

**Tech News Curation:**
- `engblogs` MCP server (engineering blog aggregation)
- Provides curated tech articles from 500+ sources
- Used by tech news commands in both systems

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/ronnycoding/my-personal-assistant.git
cd my-personal-assistant
```

### 2. Verify Permissions
Run the permission verification script to ensure proper access:
```bash
./tests/framework/verify_permissions.sh
```

If permissions are missing, follow the setup guide:
```bash
cat docs/PERMISSIONS.md
```

### 3. Explore the Structure

**Claude Code:**
```bash
# Check available skills
ls .claude/skills/

# Review a skill
cat .claude/skills/scan-inbox/SKILL.md

# View commands
ls .claude/commands/
```

**Gemini CLI:**
```bash
# Check available commands
ls .gemini/commands/

# Review scripts
ls .gemini/scripts/

# Read Gemini documentation
cat .gemini/README.md
```

**Shared:**
```bash
# View test framework
ls tests/framework/
```


## Usage Examples

### Claude Code

**Using Slash Commands:**
```bash
# Morning productivity workflow
/morning                    # Complete daily briefing

# Individual productivity commands
/inbox                      # Scan email for urgent items
/calendar                   # Today's schedule
/tasks                      # Task list by priority

# Finance management
/finance init --notebook="2025-budget"
/finance import --source="~/Documents/checking.csv"
/finance analyze --type="overview"
/finance advise --focus="savings"

# Tech news
/tech                       # All tech categories
/ai                         # AI/ML developments
/backend                    # Backend engineering
/search "GraphQL performance"
```

**Using Skills (Natural Language):**
```
"Use the daily-briefing skill to plan my day"
"Check my inbox using scan-inbox for urgent items"
"Show me my calendar for today using read-calendar"
```

**Natural Language Queries:**
```
"Review my schedule for today and create a prioritized task list
based on calendar events, emails from the last 24hrs, and existing reminders"

"Check my unread email and create reminders for anything actionable"

"Find me 2 hours of focus time this week for deep work"

"Analyze my spending patterns from last month and suggest budget improvements"
```

### Gemini CLI

**Using Commands:**
```bash
# Morning briefing
gemini -c .gemini/commands/morning.toml

# Check email
gemini -c .gemini/commands/inbox.toml

# Today's calendar
gemini -c .gemini/commands/calendar.toml

# Task list
gemini -c .gemini/commands/tasks.toml
```

**Tech News:**
```bash
# Daily tech digest
gemini -c .gemini/commands/tech.toml

# AI news
gemini -c .gemini/commands/ai.toml

# Backend articles
gemini -c .gemini/commands/backend.toml
```

### Both Systems

Both support the same natural language queries:
- "What's my day looking like?"
- "Any urgent emails I need to handle?"
- "What tasks are due today?"
- "Give me my morning briefing"

## Development

### Adding New Capabilities

**For Claude Code:**
1. Create skill directory in `.claude/skills/`
2. Write `SKILL.md` with frontmatter and instructions
3. Add AppleScript in `scripts/` subdirectory
4. Test using the testing framework

**For Gemini CLI:**
1. Create AppleScript in `.gemini/scripts/`
2. Create TOML command in `.gemini/commands/`
3. Embed complete instructions in `instruction` field
4. Test script execution

**Shared AppleScript Development:**

Each capability uses the same AppleScript implementation, just invoked differently.

**AppleScript Best Practices:**
- Date arithmetic: Use `days`, `hours`, `minutes` directly (not `1 * days`)
- Comparison operators: Use `≥` and `≤` (or `>=` and `<=`)
- String concatenation: Use `&` operator
- Error handling: Wrap calendar/reminder loops in `try` blocks
- Time zones: AppleScript uses system timezone
- Testing: Use the framework in `tests/`

**Script Locations:**
- **Claude Code**: `.claude/skills/<skill-name>/scripts/*.scpt`
- **Gemini CLI**: `.gemini/scripts/*.scpt`
- Both can share the same script files

## Project Status

**Current Features:**
- ✅ Repository setup and directory structure
- ✅ macOS permissions configuration and verification
- ✅ Permission documentation and testing framework
- ✅ Skills API framework and documentation
- ✅ AppleScript testing & validation framework
- ✅ Core productivity skills (scan-inbox, read-calendar, list-reminders, daily-briefing)
- ✅ Tech news curation via MCP server
- ✅ Personal finance advisor with Jupyter notebooks

**Planned Features:**
See [GitHub Issues](https://github.com/ronnycoding/my-personal-assistant/issues) for planned features and enhancements.

## Documentation

### General
- [Permissions Setup Guide](docs/PERMISSIONS.md) - Detailed macOS permission configuration
- [Testing Framework](tests/README.md) - AppleScript testing, assertions, and test data
- [Tech Digest Format](docs/TECH_DIGEST_FORMAT.md) - Standards for presenting tech news with proper attribution

### Claude Code
- [Claude Code Configuration](.claude/CLAUDE.md) - Complete Claude Code setup guide
- [Skills API Guide](docs/SKILLS_API.md) - Creating and using AppleScript skills
- [Skills Directory](.claude/skills/README.md) - Skills organization and best practices
- [Agent Definitions](.claude/agents/) - Specialized agent submodules

### Gemini CLI
- [Gemini Configuration](.gemini/README.md) - Complete Gemini CLI setup guide
- [Commands Directory](.gemini/commands/) - TOML command files with embedded instructions
- [Scripts Directory](.gemini/scripts/) - Centralized AppleScript implementations

### Choosing Between Claude Code and Gemini

**Use Claude Code if you:**
- Need complex multi-agent orchestration
- Prefer structured skill documentation
- Want agent specialization (backend, frontend, security, etc.)
- Work on larger projects with multiple contexts

**Use Gemini CLI if you:**
- Prefer quick, command-line workflows
- Want simpler, flatter configuration
- Like everything in one command file
- Need fast access to specific capabilities

**Use Both if you:**
- Want flexibility in different scenarios
- Like having options for different workflows
- Benefit from command-line AND IDE integration

## Contributing

Contributions are welcome! Feel free to:
- Submit bug reports and feature requests via [GitHub Issues](https://github.com/ronnycoding/my-personal-assistant/issues)
- Fork the repository and submit pull requests
- Improve documentation and examples
- Share your custom skills and workflows

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
