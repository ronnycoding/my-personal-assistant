# scan-inbox Reference

## Script Details

### scan_inbox.scpt

**Location**: `scripts/scan_inbox.scpt`

**Parameters**:
1. `timeRange` (integer): Hours to look back (default: 24)
2. `priorityOnly` (boolean): Return only flagged/priority messages (default: false)

**Returns**:
```applescript
{
  success: boolean,
  unreadCount: integer,
  actionableCount: integer,
  priorityCount: integer,
  unreadList: array,
  actionableList: array,
  priorityList: array,
  timeRange: integer,
  priorityOnly: boolean
}
```

## Actionable Keywords

The script detects these keywords in email subjects:
- deadline
- urgent
- action required
- meeting
- request
- please review
- asap
- todo
- action item

## Email Data Structure

Each email in the returned lists contains:
- `sender`: Email sender (name and address)
- `subject`: Email subject line
- `dateReceived`: Date message was received
- `isFlagged`: Boolean flag status

## Error Codes

- `-1708`: Can't continue operation (permission issue)
- Check: System Settings → Privacy & Security → Automation → Mail

## Performance

- Typical: ~2 seconds for 100 messages
- Scales with inbox size
- Recommend max 168 hours (1 week) lookback
