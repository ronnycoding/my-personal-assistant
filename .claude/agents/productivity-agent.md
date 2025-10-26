# Productivity Agent

## Description
Personal productivity assistant that orchestrates AppleScript skills across Apple Mail, macOS Calendar, Reminders, and meeting scheduling to help manage daily tasks and organization.

## Status
🚧 **Under Development** - Skills are being implemented incrementally.

## Available Skills

### Apple Mail Skills
Skills for managing email inbox, extracting actionable items, and organizing messages.

**Planned:**
- `scan_inbox` - Scan for unread, priority, actionable emails
- `extract_content` - Parse tasks, dates, meetings from emails
- `organize_mail` - Flag, archive, draft replies

**Status:** Issue #5, #6, #7 - Not yet implemented

### Calendar Skills
Skills for reading calendar events, detecting conflicts, and suggesting optimal meeting times.

**Planned:**
- `read_events` - Fetch events & availability
- `detect_conflicts` - Find overlaps & gaps
- `suggest_times` - Optimal meeting time finder

**Status:** Issue #8, #9, #10 - Not yet implemented

### Reminders Skills
Skills for managing tasks, organizing by priority, and cross-referencing with calendar.

**Planned:**
- `list_tasks` - Read & organize by list/priority
- `manage_tasks` - Create/update/complete
- `cross_reference` - Link with calendar events

**Status:** Issue #11, #12, #13 - Not yet implemented

### Meeting Skills
Skills for finding available time slots and booking meetings with attendees.

**Planned:**
- `find_slots` - Find available time across calendar
- `book_meeting` - Create event with attendees

**Status:** Issue #14, #15 - Not yet implemented

## Workflows

### Morning Briefing
**Goal:** Start the day with a complete overview of priorities.

**Steps:**
1. Read calendar events (today)
2. List reminders (today + overdue)
3. Scan unread mail (last 24h)
4. Cross-reference tasks with events
5. Generate prioritized action list

**Status:** Not yet implemented (Issue #16)

### Evening Review
**Goal:** Summarize the day and prepare for tomorrow.

**Steps:**
1. List completed reminders
2. Review today's calendar events
3. Preview tomorrow's schedule
4. Identify preparation tasks

**Status:** Not yet implemented (Issue #16)

### Email Triage
**Goal:** Process inbox and create actionable tasks.

**Steps:**
1. Scan inbox
2. Extract actionable items
3. Create reminders for tasks
4. Suggest meeting times for requests

**Status:** Not yet implemented (Issue #16)

### Find Focus Time
**Goal:** Identify blocks of uninterrupted time for deep work.

**Steps:**
1. Read calendar (next 7 days)
2. Detect gaps
3. Suggest 2hr+ blocks
4. Offer to block time

**Status:** Not yet implemented (Issue #16)

## Configuration

### Timezone
Default timezone: **America/Costa_Rica**

All date/time operations use the system timezone. Verify with:
```bash
date +%Z
```

### Working Hours
Default working hours (configurable per workflow):
- **Start:** 09:00
- **End:** 17:00

### Preferences
- **Email scan window:** Last 24 hours
- **Calendar lookahead:** 7 days
- **Minimum meeting buffer:** 15 minutes
- **Focus time minimum:** 2 hours

## Usage Examples

Once skills are implemented, you'll be able to use commands like:

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

## Development Roadmap

### Phase 1: Infrastructure ✅
- [x] Repository setup (#2)
- [ ] Skills API framework (#3)
- [ ] Testing framework (#4)

### Phase 2: Core Skills (In Progress)
- [ ] Apple Mail skills (#5, #6, #7)
- [ ] Calendar skills (#8, #9, #10)
- [ ] Reminders skills (#11, #12, #13)
- [ ] Meeting skills (#14, #15)

### Phase 3: Integration
- [ ] Agent orchestration (#16)
- [ ] Documentation (#17)

## Architecture

### Skills Organization
```
.claude/skills/
├── apple-mail/
│   ├── scan_inbox.scpt
│   ├── extract_content.scpt
│   └── organize_mail.scpt
├── calendar/
│   ├── read_events.scpt
│   ├── detect_conflicts.scpt
│   └── suggest_times.scpt
├── reminders/
│   ├── list_tasks.scpt
│   ├── manage_tasks.scpt
│   └── cross_reference.scpt
└── meetings/
    ├── find_slots.scpt
    └── book_meeting.scpt
```

### Data Flow
1. **Input:** User command to agent
2. **Skill Selection:** Agent determines which skill(s) to invoke
3. **AppleScript Execution:** Skill runs via osascript MCP tool
4. **Data Processing:** Results parsed and formatted
5. **Output:** Structured response to user

### Error Handling
- Permission errors → Redirect to PERMISSIONS.md
- AppleScript failures → Retry with simplified query
- Timeout errors → Reduce query scope
- No data → Return empty results with helpful message

## Testing

### Permission Verification
```bash
./tests/framework/verify_permissions.sh
```

### Individual Skill Tests
Once skills are implemented:
```bash
# Test Mail skill
osascript .claude/skills/apple-mail/scan_inbox.scpt 24 false

# Test Calendar skill
osascript .claude/skills/calendar/read_events.scpt

# Test Reminders skill
osascript .claude/skills/reminders/list_tasks.scpt
```

### Integration Tests
```bash
# Run full test suite (once implemented)
./tests/run_all_tests.sh
```

## Troubleshooting

### Common Issues

**"Not authorized to send Apple events"**
- Solution: Check permissions in System Settings → Privacy & Security → Automation
- See: [PERMISSIONS.md](../../docs/PERMISSIONS.md)

**Skills not loading**
- Verify skills exist in `.claude/skills/` subdirectories
- Check AppleScript syntax with: `osascript -s <skill.scpt>`

**Data not returned**
- Verify apps (Mail/Calendar/Reminders) are open and responding
- Check that calendars/lists exist and contain data
- Review timezone settings

For detailed troubleshooting, see [TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md) (coming soon).

## Contributing

This is a personal productivity agent. To add new skills:

1. Create AppleScript in appropriate `skills/` subdirectory
2. Add tests in corresponding `tests/` subdirectory
3. Update this agent definition with skill metadata
4. Document in [SKILLS_REFERENCE.md](../../docs/SKILLS_REFERENCE.md)

## Links

- [Repository](https://github.com/ronnycoding/my-personal-agents)
- [Issue Tracker](https://github.com/ronnycoding/my-personal-agents/issues)
- [Permissions Guide](../../docs/PERMISSIONS.md)
- [Epic Issue #1](https://github.com/ronnycoding/my-personal-agents/issues/1)

## License
Private - Personal Use Only
