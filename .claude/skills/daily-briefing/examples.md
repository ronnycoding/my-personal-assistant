# daily-briefing Examples

## Example 1: Standard Morning Briefing

**User**: "Give me my morning briefing"

**Execution**:
```bash
# Get today's date
TODAY=$(date +%Y-%m-%d)

# Gather all data
osascript .claude/skills/read-calendar/scripts/read_events.scpt "$TODAY" "$TODAY"
osascript .claude/skills/scan-inbox/scripts/scan_inbox.scpt 24 false
osascript .claude/skills/list-reminders/scripts/list_tasks.scpt
```

**Response**:
```
🌅 Good Morning, Ronny! Here's Your Sunday (October 26, 2025)

📅 CALENDAR
• No events scheduled today
• Full day open for focused work ✨

📬 INBOX (Last 24 Hours)
• 38 unread messages
• 0 urgent/actionable items
• Mix of newsletters and notifications

Top senders:
- Google (security alerts)
- Tech newsletters (C#, React, Programming Digest)
- Bank notifications (BAC)

✅ REMINDERS
• 0 overdue tasks
• 0 due today
• 12 pending tasks across all lists

⏰ SUGGESTED SCHEDULE
• 9:00-12:00: Deep work session (no interruptions)
• 12:00-13:00: Lunch + email batch processing
• 13:00-16:00: Continue focused work
• 16:00-17:00: Weekly review + planning tomorrow

💡 TOP PRIORITIES TODAY
1. Complete your focused work - no meetings to interrupt
2. Clear inbox during lunch (batch process newsletters)
3. Review pending tasks for the week ahead

🎯 INSIGHT: Perfect day for deep work! No meetings means uninterrupted focus time.

What would you like to tackle first?
```

## Example 2: Busy Day Briefing

**User**: "Plan my day"

**Response** (hypothetical busy day):
```
🌅 Good Morning! Here's Your Monday (October 28, 2025)

📅 CALENDAR (6 events)
• 9:00-9:30: Morning Standup (Work calendar)
• 10:00-11:00: Project Review
• 12:00-13:00: Lunch with Client
• 14:00-15:00: Team Sync
• 15:30-16:00: 1-on-1 with Manager
• 16:30-17:00: EOD Wrap-up

⚠️  Conflicts Detected:
• Only 30min gaps between meetings
• No time blocked for focused work

📬 INBOX (Last 24 Hours)
• 45 unread messages
• 3 URGENT items requiring response
• 5 meeting requests to schedule

⚡ ACTIONABLE:
1. [URGENT] Client escalation - respond before 10am
2. Budget approval needed - deadline today
3. Meeting request - find time this week

✅ REMINDERS
• 2 overdue tasks ⚠️
• 5 due today
• 18 pending tasks total

🚨 OVERDUE (needs attention):
1. Complete Q4 planning doc
2. Review team performance reviews

⏰ OPTIMIZED SCHEDULE
• 8:00-9:00: ⚡ Handle 3 urgent emails + overdue tasks
• 9:00-16:30: Back-to-back meetings (stay focused)
• 16:30-17:30: Process inbox + plan tomorrow

💡 TOP PRIORITIES TODAY
1. URGENT: Respond to client escalation (before 10am)
2. Complete 2 overdue tasks during gaps
3. Survive 6 meetings - stay present
4. Block time tomorrow for focused work

⚠️  HEADS UP: Packed schedule today. Protect tomorrow for deep work!

Need me to reschedule anything or block focus time?
```

## Example 3: Weekend Planning

**User**: "What's my day look like?" (Sunday)

**Response**:
```
🌅 Happy Sunday! (October 26, 2025)

📅 CALENDAR
• No events scheduled
• Weekend - enjoy! 🎉

📬 INBOX
• 38 unread (mostly newsletters)
• Nothing urgent
• Can wait until Monday

✅ REMINDERS
• 0 work tasks due
• 3 personal items pending
• All low priority

💡 WEEKEND MODE
Since it's Sunday with no urgent items:

✅ Suggested Activities:
1. Relax and recharge
2. Optional: 30min inbox cleanup (newsletters)
3. Optional: Plan Monday priorities
4. Enjoy your free time!

🎯 You're all caught up. Have a great day off! 🌟

Want me to help prep for Monday?
```
