# scan-inbox Examples

## Example 1: Check Today's Email

**User**: "Check my email from today"

**Command**:
```bash
osascript .claude/skills/scan-inbox/scripts/scan_inbox.scpt 24 false
```

**Response**:
```
📬 Inbox Summary (Last 24 Hours)

📊 Overview:
- 38 unread messages
- 0 actionable items
- 0 priority/flagged

📧 Recent Unread:
1. Google - Security alert for ronnyangelo.freites@gmail.com
2. C# Digest - CD#580 You don't need a repository in EF Core
3. React Digest - RD#529 React Server Components
4. Programming Digest - PD#649 What happens when you press send to ChatGPT
5. Leadership in Tech - LT#265 Stop caring so much about your people

💡 No urgent items requiring immediate attention.
```

## Example 2: Check Urgent Items Only

**User**: "Any urgent emails?"

**Command**:
```bash
osascript .claude/skills/scan-inbox/scripts/scan_inbox.scpt 24 true
```

**Response**:
```
🚨 Priority Emails (Last 24 Hours)

No flagged or priority messages found.
All clear! ✅
```

## Example 3: Weekly Email Summary

**User**: "Show me actionable emails from this week"

**Command**:
```bash
osascript .claude/skills/scan-inbox/scripts/scan_inbox.scpt 168 false
```

**Response**:
```
📬 Weekly Inbox Summary (Last 7 Days)

📊 Overview:
- 156 unread messages
- 3 actionable items
- 1 priority/flagged

⚡ Actionable Items:
1. [URGENT] Project deadline - Please review by Friday
2. Meeting request - Schedule sync for next week
3. Action required - Approve budget proposal

🚩 Priority:
1. [FLAGGED] Client escalation - Immediate response needed

💡 Recommended: Address the 3 actionable items today.
```

## Example 4: Morning Triage

**User**: "Help me triage my inbox"

**Workflow**:
1. Scan last 24 hours
2. Categorize by urgency
3. Suggest action plan

**Commands**:
```bash
osascript .claude/skills/scan-inbox/scripts/scan_inbox.scpt 24 false
```

**Response**:
```
📬 Morning Email Triage

🎯 Action Plan:
1. ✅ No urgent items - you're in good shape
2. 📰 38 newsletters - batch process later
3. 🔔 7 notifications - review when convenient

⏰ Estimated time: 15 minutes to clear actionable items

💡 Focus on your planned work - email can wait!
```
