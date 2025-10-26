# read-calendar Examples

## Example 1: Today's Schedule

**User**: "What's on my calendar today?"

**Command**:
```bash
osascript .claude/skills/read-calendar/scripts/read_events.scpt "2025-10-26" "2025-10-26"
```

**Response**:
```
📅 Today's Schedule (October 26, 2025)

No events scheduled for today.
Enjoy your free time! 🎉
```

## Example 2: This Week's Meetings

**User**: "Show me my meetings this week"

**Command**:
```bash
osascript .claude/skills/read-calendar/scripts/read_events.scpt "2025-10-26" "2025-11-01"
```

## Example 3: Tomorrow's Agenda

**User**: "What do I have tomorrow?"

**Command**:
```bash
osascript .claude/skills/read-calendar/scripts/read_events.scpt "2025-10-27" "2025-10-27"
```
