# Apple Mail Skills

AppleScript skills for automating Apple Mail operations including inbox scanning, email parsing, and message organization.

## Available Skills

| Skill | Status | Issue | Description |
|-------|--------|-------|-------------|
| `scan_inbox` | 📋 Planned | [#5](https://github.com/ronnycoding/my-personal-assistant/issues/5) | Scan inbox for unread and actionable messages |
| `extract_content` | 📋 Planned | [#6](https://github.com/ronnycoding/my-personal-assistant/issues/6) | Parse tasks, dates, meetings from emails |
| `organize_mail` | 📋 Planned | [#7](https://github.com/ronnycoding/my-personal-assistant/issues/7) | Flag, archive, draft replies |

## Skill Specifications

### scan_inbox

**Purpose**: Scan Apple Mail inbox for unread messages and identify actionable items.

**Parameters**:
- `time_range` (integer, default: 24): Hours to look back
- `priority_only` (boolean, default: false): Return only priority messages

**Returns**:
```json
{
  "unread_count": 10,
  "actionable_count": 3,
  "priority_count": 5,
  "unread_list": [...],
  "actionable_list": [...],
  "priority_list": [...]
}
```

**Actionable Keywords**: deadline, urgent, action required, meeting, request, please review

### extract_content

**Purpose**: Parse email content to extract tasks, meetings, and deadlines.

**Parameters**:
- `message_id` (string): Email identifier
- `extract_type` (string, default: "all"): tasks|meetings|all

**Returns**:
```json
{
  "tasks": [{
    "description": "Review proposal",
    "deadline": "2025-10-28",
    "source_email": "...",
    "confidence": 0.95
  }],
  "meetings": [{
    "subject": "Project sync",
    "date_time": "2025-10-27 14:00",
    "location": "Conference Room A",
    "attendees": ["user@example.com"]
  }],
  "deadlines": [...]
}
```

### organize_mail

**Purpose**: Automate email organization through flagging, archiving, and drafting.

**Parameters**:
- `message_ids` (array of strings): Email identifiers
- `action` (string): flag|archive|move|draft_reply
- `options` (object): Action-specific options

**Returns**:
```json
{
  "success": true,
  "processed_count": 5,
  "errors": []
}
```

## Usage Examples

### Scan Inbox for Today
```bash
osascript .claude/skills/apple-mail/scan_inbox.scpt 24 false
```

### Extract Content from Email
```bash
osascript .claude/skills/apple-mail/extract_content.scpt "message-id" "all"
```

### Flag Important Emails
```bash
osascript .claude/skills/apple-mail/organize_mail.scpt "id1,id2" "flag" "{}"
```

## Development Status

🚧 **Not Yet Implemented**

These skills are planned for development. See individual issues for specifications:
- Issue #5: scan_inbox
- Issue #6: extract_content
- Issue #7: organize_mail

## Testing

Tests will be located in:
```
tests/apple-mail/
├── test_scan_inbox.scpt
├── test_extract_content.scpt
└── test_organize_mail.scpt
```

## Permissions Required

- System Settings → Privacy & Security → Automation → Mail
- Optional: Full Disk Access (for Mail database access)

Verify permissions:
```bash
./tests/framework/verify_permissions.sh
```

## Error Handling

Common errors and solutions:

**Permission Denied**:
```
execution error: Mail got an error: Not authorized to send Apple events
```
→ Check automation permissions for Mail

**Timeout**:
→ Reduce `time_range` parameter or add pagination

**No Messages Found**:
→ Returns empty lists with zero counts (not an error)

## Next Steps

1. Review issue specifications (#5, #6, #7)
2. Implement skills following [Skills README](../README.md)
3. Write comprehensive tests
4. Update this README with implementation details
