# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Personal AI assistant for macOS productivity automation via AppleScript skills. Dual-platform support: Claude Code (skill-based) and Gemini CLI (command-based). Key domains: email management (Apple Mail), calendar intelligence (macOS Calendar), task orchestration (Reminders), and personal finance (Jupyter notebooks).

## Key Commands

### Testing

```bash
# Run all AppleScript tests
./tests/framework/run_tests.sh

# Test specific domain
./tests/framework/run_tests.sh --domain apple-mail

# Verify macOS permissions
./tests/framework/verify_permissions.sh

# Test individual skill
osascript .claude/skills/scan-inbox/scripts/scan_inbox.scpt 24 false
osascript .claude/skills/read-calendar/scripts/read_events.scpt "2025-10-26" "2025-10-26"
osascript .claude/skills/list-reminders/scripts/list_tasks.scpt
```

### Finance Commands

```bash
# Extract transactions from PDFs
cd .claude/finance-notebooks
python extract_pdf_statements.py ~/Documents/Finance/*.pdf -o output.csv

# Consolidate multiple CSV files
python consolidate_statements.py ~/Documents/Finance/*.csv -o combined.csv

# Finance command workflow (via Claude Code)
/finance init --notebook="2025-budget"
/finance import --source="transactions.csv" --type="checking"
/finance analyze --type=overview
/finance advise --focus="savings"
```

## Architecture

### Dual-Platform Design

**Claude Code** (`.claude/`):
- Skill-based architecture with SKILL.md files
- Scripts distributed in skill directories
- Complex workflow orchestration
- Best for: Multi-step tasks, agent coordination

**Gemini CLI** (`.gemini/`):
- TOML command files with embedded instructions
- Centralized scripts in `.gemini/scripts/`
- Flat, self-contained structure
- Best for: Quick commands, CLI workflows

**Shared Components**: Both use identical AppleScript implementations - only invocation differs.

### Core System Flow

```
User Request → Claude Code/Gemini → Skill/Command → AppleScript → macOS App
                                                           ↓
                               Skills: scan-inbox, read-calendar, list-reminders
                               Finance: Jupyter notebooks via MCP
```

### Skill Architecture

Each Claude Code skill has:
- `SKILL.md` - YAML frontmatter + instructions (required)
- `reference.md` - Technical documentation (optional)
- `examples.md` - Usage examples (optional)
- `scripts/*.scpt` - AppleScript implementations (optional)

Skill discovery is automatic via YAML frontmatter description.

### Finance System Architecture

```
/finance command → finance.md → jupyter-mcp → Jupyter notebook
                                     ↓
                    finance_utils.py (analysis library)
                    finance-notebooks/ (data files - gitignored)
```

**Data Flow**:
1. Import: CSV/PDF → pandas DataFrame → notebook cell
2. Analysis: finance_utils.py functions → metrics
3. Visualization: matplotlib charts → notebook output
4. Advisory: Claude AI → recommendations based on data

**Privacy**: All notebooks (`.ipynb`), transaction files (`.csv`, `.xlsx`), and reports are gitignored.

## AppleScript Development

### Critical Patterns

**Date Arithmetic** (macOS AppleScript quirk):
```applescript
# Correct
set yesterday to (current date) - (1 * days)
set cutoff to (current date) - (24 * hours)

# Wrong - will cause runtime errors
set yesterday to (current date) - 1 day
```

**Error Handling** (always required):
```applescript
try
    tell application "Mail"
        # operations
    end tell
on error errMsg number errNum
    return {success:false, errorMessage:errMsg, errorNumber:errNum}
end try
```

**Return Format** (standardized):
```applescript
return {¬
    success:true, ¬
    count:10, ¬
    data:myList¬
}
```

### macOS Permissions

All skills require automation permissions:
- System Settings → Privacy & Security → Automation
- Enable: Mail, Calendar, Reminders for Terminal/Claude

**Common Issue**: Permission prompt appears on first run. User must click "OK" in System Preferences.

### icalBuddy Dependency

**Critical**: Install `icalBuddy` for recurring events:
```bash
brew install ical-buddy
```

**Why**: macOS Calendar via AppleScript doesn't pre-generate recurring event instances. `icalBuddy` properly expands recurring events for future date queries.

## Finance System

### Notebook Structure

Created by `/finance init`:
- Setup cell: Import libraries, configure pandas
- Data cell: Transaction storage (DataFrame)
- Analysis cells: Income, expenses, categories
- Projection cells: Forecasting, scenarios
- Visualization cells: Charts and graphs
- AI cell: Context for recommendations

### Helper Library (`finance_utils.py`)

Core functions:
- `calculate_income_expense(df)` - Categorize transactions
- `analyze_cashflow(df)` - Monthly flow analysis
- `project_savings(df, months)` - Future projections
- `categorize_transaction(description)` - Auto-categorization
- `generate_budget_comparison(df, budget)` - Variance analysis

### Data Import Workflow

**CSV/Excel**:
```bash
/finance import --source="file.csv" --type="checking"
```

**PDF Statements**:
```bash
cd .claude/finance-notebooks
python extract_pdf_statements.py bank-statement.pdf -o transactions.csv
# Then import via /finance command
```

**Multiple Files**:
```bash
python consolidate_statements.py file1.csv file2.csv -o combined.csv
```

## Skill Development

### Creating New Skills

1. **Create directory**: `.claude/skills/<skill-name>/`
2. **Write SKILL.md** with YAML frontmatter:
```yaml
---
name: skill-name
description: When to use this skill (specific triggers)
allowed-tools: Bash
---
```
3. **Add instructions**: Step-by-step for Claude to execute
4. **Create scripts**: AppleScript in `scripts/` subdirectory
5. **Test**: Use testing framework or run directly

### Testing Framework

Located in `tests/framework/`:
- `assertions.scpt` - Assertion library (assertEqual, assertTrue, etc.)
- `test_data_generator.scpt` - Mock data creation
- `cleanup.scpt` - Test data removal
- `verify_permissions.sh` - Permission checker

**Usage**:
```applescript
set assertions to load script (POSIX file "/path/to/assertions.scpt")
assertions's assertEqual(5, 5, "Numbers equal")
assertions's printResults()
```

## MCP Integration

### Tech News (engblogs server)

Skills using MCP:
- `tech-news-curator` - Engineering blog aggregation
- Commands: ai.md, backend.md, frontend.md, cloud.md, etc.

**MCP Tools Available**:
- `get_content` - Browse articles with filters
- `search_articles` - Keyword search
- `semantic_search` - AI-powered search
- `get_daily_digest` - Today's unread articles
- `set_tag` - Mark as read/favorite

### Finance (jupyter-mcp server)

**MCP Tools**:
- `use_notebook` - Connect to notebook
- `read_notebook` - Get cell contents
- `insert_cell` - Add new cell
- `execute_cell` - Run code with timeout
- `insert_execute_code_cell` - Combined insert+execute

**Workflow**: `/finance` command → jupyter-mcp → notebook operations → return results

## Common Patterns

### Skill Invocation

Claude automatically selects skills based on user requests via YAML description matching. No explicit skill names needed in user queries.

**Example**:
- User: "Check my email" → Activates `scan-inbox`
- User: "What's my schedule?" → Activates `read-calendar`
- User: "Daily briefing" → Activates `daily-briefing` (orchestrates multiple skills)

### Error Patterns

**Permission Denied**:
```
Solution: Run ./tests/framework/verify_permissions.sh
```

**Script Not Found**:
```
Solution: Verify path is absolute or use POSIX file syntax
```

**Timeout**:
```
Solution: Reduce query scope (time range, filters)
```

### Finance Data Privacy

**Critical**: Never commit:
- Jupyter notebooks (`.ipynb`)
- Transaction files (`.csv`, `.xlsx`, `.pdf`)
- Reports (`reports/*.png`, `reports/*.pdf`)

All gitignored in `.claude/finance-notebooks/.gitignore`.

## Repository-Specific Notes

### Timezone

Default: `America/Costa_Rica`
- AppleScript uses system timezone
- Verify: `sudo systemsetup -gettimezone`

### Personal Calendar

When creating personal events, use calendar `ronnyangelo.freites@gmail.com` instead of default "Home" calendar.

### Git Workflow

Standard branch workflow:
- Main branch: `main`
- Feature branches: `issue-N-description`
- Commits: Include issue references

### Documentation Structure

- `docs/` - General documentation
- `docs/finance/` - Finance-specific guides
- `.claude/skills/<skill>/` - Skill documentation
- `.gemini/README.md` - Gemini CLI guide
- `tests/README.md` - Testing framework guide
