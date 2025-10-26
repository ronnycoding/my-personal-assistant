# Skills Directory

This directory contains AppleScript-based skills organized by macOS application domain. Each skill is designed to be invoked by the productivity agent using Claude Code's Skills API.

## Directory Structure

```
skills/
├── apple-mail/      # Apple Mail automation skills
├── calendar/        # macOS Calendar automation skills
├── reminders/       # macOS Reminders automation skills
├── meetings/        # Meeting scheduling workflows
└── README.md        # This file
```

## Skill Organization

Skills are organized by the primary macOS application they automate:

- **apple-mail/**: Email scanning, parsing, organizing
- **calendar/**: Event reading, conflict detection, time suggestions
- **reminders/**: Task management, cross-referencing
- **meetings/**: Multi-app workflows for meeting scheduling

## Skill Format

Each skill consists of:

1. **AppleScript file** (`.scpt` or `.applescript`)
2. **Metadata file** (`.skill.json`)
3. **Test file** (`../tests/{domain}/test_{skill_name}.scpt`)

### Example Skill Structure

```
apple-mail/
├── scan_inbox.scpt           # AppleScript implementation
├── scan_inbox.skill.json     # Skill metadata
└── README.md                 # Documentation
```

## Skill Metadata Format

Each skill has a `.skill.json` file containing metadata:

```json
{
  "name": "scan_inbox",
  "domain": "apple-mail",
  "description": "Scan Apple Mail inbox for unread and actionable messages",
  "version": "1.0.0",
  "parameters": [
    {
      "name": "time_range",
      "type": "integer",
      "description": "Hours to look back",
      "default": 24,
      "required": false
    },
    {
      "name": "priority_only",
      "type": "boolean",
      "description": "Return only priority messages",
      "default": false,
      "required": false
    }
  ],
  "returns": {
    "type": "object",
    "properties": {
      "unread_count": {"type": "integer"},
      "actionable_count": {"type": "integer"},
      "priority_count": {"type": "integer"},
      "unread_list": {"type": "array"},
      "actionable_list": {"type": "array"},
      "priority_list": {"type": "array"}
    }
  },
  "error_handling": {
    "permission_denied": "Check Mail automation permissions in System Settings",
    "no_messages": "Return empty lists with zero counts",
    "timeout": "Reduce time_range parameter"
  },
  "dependencies": {
    "apps": ["Mail"],
    "permissions": ["Mail automation"],
    "other_skills": []
  }
}
```

## Skill Implementation Guidelines

### AppleScript Best Practices

1. **Error Handling**: Always wrap operations in `try` blocks
   ```applescript
   try
       tell application "Mail"
           -- Your code here
       end tell
   on error errMsg
       return {success:false, error:errMsg}
   end try
   ```

2. **Date Arithmetic**: Use direct time units
   ```applescript
   set cutoffDate to (current date) - (24 * hours)  -- Correct
   ```

3. **Comparison Operators**: Use `≥`, `≤` or `>=`, `<=`
   ```applescript
   if dateReceived >= cutoffDate then
       -- Process message
   end if
   ```

4. **String Handling**: Use `&` for concatenation
   ```applescript
   set result to "Count: " & messageCount
   ```

5. **Return Structured Data**: Use AppleScript records
   ```applescript
   return {¬
       success:true, ¬
       count:10, ¬
       data:myList¬
   }
   ```

### Timezone Handling

All skills should use the system timezone (America/Costa_Rica by default):

```applescript
-- AppleScript automatically uses system timezone
set now to current date
```

### Performance Considerations

1. **Limit Query Scope**: Use time ranges and filters
2. **Pagination**: Handle large data sets in chunks
3. **Caching**: Store frequently accessed data
4. **Timeout Handling**: Fail gracefully on slow operations

## Skill Invocation

Skills are invoked by the productivity agent using Claude Code's Skills API:

### Via Agent Prompt
```
"Scan my inbox for unread emails from the last 24 hours"
→ Agent invokes: scan_inbox skill with time_range=24
```

### Direct Invocation (for testing)
```bash
osascript .claude/skills/apple-mail/scan_inbox.scpt 24 false
```

## Skill Development Workflow

### 1. Create Skill Files
```bash
# Navigate to appropriate domain directory
cd .claude/skills/apple-mail

# Create AppleScript file
touch my_skill.scpt

# Create metadata file
touch my_skill.skill.json
```

### 2. Implement AppleScript
Write your skill following the guidelines above.

### 3. Create Metadata
Define parameters, return types, and error handling in `.skill.json`.

### 4. Write Tests
Create corresponding test in `tests/{domain}/test_my_skill.scpt`.

### 5. Document
Add skill to domain README and update agent definition.

### 6. Test
```bash
# Run skill directly
osascript .claude/skills/{domain}/my_skill.scpt [args]

# Run tests
./tests/framework/verify_permissions.sh
osascript tests/{domain}/test_my_skill.scpt
```

## Example Skills

### Simple Skill: Get Inbox Count
```applescript
-- get_inbox_count.scpt
tell application "Mail"
    set inboxMessages to messages of inbox
    set unreadCount to count of (messages of inbox whose read status is false)

    return {¬
        total:count of inboxMessages, ¬
        unread:unreadCount¬
    }
end tell
```

### Complex Skill: Find Free Time
```applescript
-- find_free_time.scpt
on run {durationMinutes, searchDays}
    set freeSlots to {}
    set startDate to current date
    set endDate to startDate + (searchDays * days)

    tell application "Calendar"
        set allEvents to events whose (start date ≥ startDate and start date ≤ endDate)

        -- Logic to find gaps between events
        -- Add to freeSlots list
    end tell

    return {slots:freeSlots, count:(count of freeSlots)}
end run
```

## Testing Skills

Each skill should have comprehensive tests:

```applescript
-- tests/apple-mail/test_scan_inbox.scpt
property testsPassed : 0
property testsFailed : 0

on runTests()
    testEmptyInbox()
    testWithUnreadMessages()
    testTimeRangeFilter()
    testPriorityFilter()

    log "Tests passed: " & testsPassed
    log "Tests failed: " & testsFailed
end runTests

on testEmptyInbox()
    -- Test with no unread messages
    set result to run script file ((path to me as text) & "::scan_inbox.scpt") with parameters {24, false}
    if unread_count of result is 0 then
        set testsPassed to testsPassed + 1
    else
        set testsFailed to testsFailed + 1
    end if
end testEmptyInbox
```

## Error Handling

Skills should return structured errors:

```applescript
on error errMsg number errNum
    return {¬
        success:false, ¬
        error:errMsg, ¬
        errorNumber:errNum, ¬
        suggestion:"Check System Settings → Privacy & Security → Automation"¬
    }
end try
```

## Security Considerations

1. **Read-Only by Default**: Skills should prefer read operations
2. **User Confirmation**: Prompt before destructive actions
3. **Data Sanitization**: Clean output before returning
4. **Permission Checks**: Verify access before operations
5. **Logging**: Log actions for audit trail

## Troubleshooting

### Permission Errors
```
execution error: Mail got an error: Not authorized to send Apple events
```
→ Run `./tests/framework/verify_permissions.sh`

### Skill Not Found
- Verify file exists in correct directory
- Check file permissions (should be readable)
- Confirm `.skill.json` metadata exists

### Syntax Errors
```bash
# Check AppleScript syntax
osascript -s .claude/skills/{domain}/{skill}.scpt
```

### Performance Issues
- Reduce query time range
- Add pagination
- Use filters to limit data
- Profile with `log` statements

## Next Steps

1. Review [Epic Issue #1](https://github.com/ronnycoding/my-personal-agents/issues/1) for skill roadmap
2. Check individual skill issues (#5-#15) for specifications
3. Start with simple skills (read-only operations)
4. Test thoroughly before integration

## Resources

- [AppleScript Language Guide](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/)
- [Mail Scripting Dictionary](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/MailScriptingRef/)
- [Calendar Scripting Dictionary](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/CalendarScriptingRef/)
- [Permissions Guide](../../docs/PERMISSIONS.md)
