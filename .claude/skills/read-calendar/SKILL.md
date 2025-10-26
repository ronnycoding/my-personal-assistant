---
name: read-calendar
description: Read macOS Calendar events for a specified date range. Use this when the user asks about their schedule, upcoming meetings, today's agenda, or wants to know what's on their calendar. Returns events with times, locations, and attendees.
allowed-tools: Bash
---

# Read Calendar

Retrieves calendar events from macOS Calendar for analysis, planning, and scheduling.

## When to Use

- "What's on my calendar today?"
- "Show me my schedule for this week"
- "Do I have any meetings tomorrow?"
- "What's my next meeting?"

## Instructions

### Execute Calendar Read

\`\`\`bash
osascript .claude/skills/read-calendar/read_events.scpt "<start_date>" "<end_date>"
\`\`\`

Example:
\`\`\`bash
osascript .claude/skills/read-calendar/read_events.scpt "2025-10-26" "2025-10-27"
\`\`\`

### Present Results

Format events clearly:
- Group by day
- Show time, title, location
- Highlight conflicts if any
- Identify gaps for focus time
