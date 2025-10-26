# Skills API Integration Guide

This guide explains how to create, register, and invoke AppleScript skills using Claude Code's Skills API for the Personal Productivity Assistant.

## Overview

Skills are modular AppleScript automations that can be invoked by the productivity agent. Each skill:
- Performs a specific task (read emails, check calendar, manage reminders)
- Has well-defined parameters and return values
- Includes error handling and validation
- Is documented with metadata

## Architecture

```
User Request
    ↓
Productivity Agent (.claude/agents/productivity-agent.md)
    ↓
Skills API (Claude Code)
    ↓
osascript (MCP Tool)
    ↓
AppleScript Skill (.claude/skills/{domain}/{skill}.scpt)
    ↓
macOS Application (Mail, Calendar, Reminders)
```

## Creating a New Skill

### 1. Choose Domain

Organize skills by the primary macOS application:
- `apple-mail/` - Email operations
- `calendar/` - Calendar operations
- `reminders/` - Task operations
- `meetings/` - Multi-app workflows

### 2. Create AppleScript File

```bash
cd .claude/skills/{domain}
touch my_skill.scpt
```

Use the template from `.claude/skills/_templates/skill_template.scpt`:

```applescript
on run argv
	-- Parse parameters
	if (count of argv) > 0 then
		set param1 to item 1 of argv
	else
		set param1 to "default_value"
	end if

	-- Execute with error handling
	try
		set skillResult to mySkillLogic(param1)
		return skillResult
	on error errMsg number errNum
		return {¬
			success:false, ¬
			errorMessage:errMsg, ¬
			errorNumber:errNum¬
		}
	end try
end run

on mySkillLogic(param1)
	tell application "TargetApp"
		-- Your logic here
	end tell

	return {success:true, data:"result"}
end mySkillLogic
```

### 3. Create Metadata File

```bash
touch my_skill.skill.json
```

Use the template from `.claude/skills/_templates/skill_metadata_template.json`:

```json
{
  "name": "my_skill",
  "domain": "apple-mail",
  "description": "What this skill does",
  "version": "1.0.0",
  "parameters": [...],
  "returns": {...},
  "error_handling": {...},
  "dependencies": {...}
}
```

### 4. Write Tests

Create test file in `tests/{domain}/test_my_skill.scpt`:

```applescript
-- Test with valid input
set result1 to run script file "path/to/my_skill.scpt" with parameters {"valid"}
if success of result1 is true then
	log "Test passed"
else
	log "Test failed: " & errorMessage of result1
end if
```

### 5. Document

Add skill to domain README (`.claude/skills/{domain}/README.md`).

## Skill Metadata Format

### Required Fields

```json
{
  "name": "skill_name",
  "domain": "apple-mail|calendar|reminders|meetings",
  "description": "Brief description",
  "version": "1.0.0"
}
```

### Parameters

```json
"parameters": [
  {
    "name": "time_range",
    "type": "integer",
    "description": "Hours to look back",
    "default": 24,
    "required": false,
    "validation": {
      "min": 1,
      "max": 168
    }
  }
]
```

**Supported Types:**
- `string` - Text values
- `integer` - Whole numbers
- `boolean` - true/false
- `array` - Lists
- `object` - Structured data

### Return Values

```json
"returns": {
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "count": {"type": "integer"},
    "data": {"type": "array"}
  },
  "example": {
    "success": true,
    "count": 5,
    "data": []
  }
}
```

### Error Handling

```json
"error_handling": {
  "permission_denied": "Check System Settings → Privacy & Security",
  "invalid_input": "Verify parameter types",
  "timeout": "Reduce query scope",
  "no_data": "Returns empty result (not an error)"
}
```

### Dependencies

```json
"dependencies": {
  "apps": ["Mail", "Calendar"],
  "permissions": ["Mail automation", "Calendar automation"],
  "other_skills": ["read_events"],
  "external": []
}
```

## Invoking Skills

### Via Agent

The productivity agent automatically selects and invokes skills based on user requests:

```
User: "Check my unread emails from today"
→ Agent invokes: scan_inbox skill with time_range=24
```

### Direct Invocation (Testing)

```bash
# Basic invocation
osascript .claude/skills/apple-mail/scan_inbox.scpt 24 false

# With error handling
osascript .claude/skills/calendar/read_events.scpt 2025-10-26 2025-10-27
```

### From Another AppleScript

```applescript
set skillPath to ".claude/skills/apple-mail/scan_inbox.scpt"
set result to run script file skillPath with parameters {24, false}

if success of result is true then
	set emailCount to unread_count of result
	log "Found " & emailCount & " unread emails"
end if
```

## AppleScript Best Practices

### Error Handling

Always wrap operations in try blocks:

```applescript
try
	tell application "Mail"
		-- Operations
	end tell
on error errMsg number errNum
	return {success:false, errorMessage:errMsg, errorNumber:errNum}
end try
```

### Date Operations

Use direct time units (not multiplication):

```applescript
-- Correct
set yesterday to (current date) - (1 * days)
set cutoff to (current date) - (24 * hours)

-- Also correct
set tomorrow to (current date) + (1 * days)
```

### Comparisons

Use proper operators:

```applescript
-- Correct
if dateReceived >= cutoffDate then
	-- Process
end if

-- Also works
if dateReceived ≥ cutoffDate then
	-- Process
end if
```

### String Handling

Use `&` for concatenation:

```applescript
set message to "Found " & count & " items"
```

### Returning Data

Use records with descriptive keys:

```applescript
return {¬
	success:true, ¬
	total_count:10, ¬
	unread_count:3, ¬
	items:myList¬
}
```

## Performance Optimization

### Limit Query Scope

```applescript
-- Good: Limited time range
set cutoff to (current date) - (24 * hours)
set messages to (messages of inbox whose date received >= cutoff)

-- Bad: All messages
set messages to messages of inbox
```

### Use Filters

```applescript
-- Good: Filter in query
set unread to (messages of inbox whose read status is false)

-- Bad: Loop and check
repeat with msg in allMessages
	if read status of msg is false then
		-- Process
	end if
end repeat
```

### Pagination

For large datasets:

```applescript
on getMessagesBatch(startIndex, batchSize)
	set endIndex to startIndex + batchSize - 1
	set batch to items startIndex thru endIndex of allMessages
	return batch
end getMessagesBatch
```

## Testing Skills

### Unit Tests

Test individual skill functions:

```applescript
-- tests/apple-mail/test_scan_inbox.scpt
on testWithValidParams()
	set result to run script file "scan_inbox.scpt" with parameters {24, false}
	if success of result is true then
		return "PASS"
	else
		return "FAIL: " & errorMessage of result
	end if
end testWithValidParams
```

### Integration Tests

Test skill workflows:

```applescript
-- Test email to reminder workflow
set emails to run script file "scan_inbox.scpt" with parameters {24, true}
set extracted to run script file "extract_content.scpt" with parameters {item 1 of emails, "tasks"}
set reminder to run script file "manage_tasks.scpt" with parameters {"create", extracted}
```

### Permission Tests

Verify access before running:

```bash
./tests/framework/verify_permissions.sh
```

## Debugging

### Enable Logging

```applescript
log "Processing " & (count of messages) & " messages"
log "Current timezone: " & time zone of (current date)
```

### Check Syntax

```bash
osascript -s .claude/skills/{domain}/{skill}.scpt
```

### Verbose Output

```applescript
on debug(message)
	if debugMode is true then
		log "DEBUG: " & message
	end if
end debug
```

### Error Messages

Include helpful context:

```applescript
on error errMsg number errNum
	set contextMsg to "Failed while processing inbox. Original error: " & errMsg
	return {success:false, errorMessage:contextMsg, errorNumber:errNum}
end try
```

## Skill Examples

### Simple Read Operation

```applescript
-- get_calendar_count.scpt
on run argv
	tell application "Calendar"
		set eventCount to count of events of calendar 1
		return {success:true, count:eventCount}
	end tell
end run
```

### With Parameters

```applescript
-- list_reminders_by_list.scpt
on run argv
	set listName to item 1 of argv

	tell application "Reminders"
		set targetList to list listName
		set allReminders to reminders of targetList
		return {success:true, count:(count of allReminders)}
	end tell
end run
```

### Complex Workflow

```applescript
-- find_conflicts.scpt
on run argv
	set startDate to item 1 of argv as date
	set endDate to item 2 of argv as date

	set conflicts to {}

	tell application "Calendar"
		set allEvents to events whose (start date >= startDate and start date <= endDate)

		repeat with i from 1 to (count of allEvents) - 1
			set event1 to item i of allEvents
			repeat with j from (i + 1) to count of allEvents
				set event2 to item j of allEvents

				if (end date of event1 > start date of event2) and ¬
				   (start date of event1 < end date of event2) then
					set end of conflicts to {event1:summary of event1, event2:summary of event2}
				end if
			end repeat
		end repeat
	end tell

	return {success:true, conflicts:conflicts, count:(count of conflicts)}
end run
```

## Security Considerations

### Validate Input

```applescript
on validateTimeRange(hours)
	if hours < 1 or hours > 168 then
		error "Time range must be between 1 and 168 hours"
	end if
end validateTimeRange
```

### Sanitize Output

```applescript
on sanitizeEmailContent(content)
	-- Remove sensitive data
	-- Truncate long content
	return sanitized
end sanitizeEmailContent
```

### Limit Scope

```applescript
-- Good: Only inbox
set messages to messages of mailbox "INBOX"

-- Avoid: All mailboxes
set messages to every message
```

## Troubleshooting

### "Not authorized to send Apple events"

**Solution**: Check automation permissions
```bash
./tests/framework/verify_permissions.sh
```

### Skill not found

**Solution**: Verify file path and permissions
```bash
ls -la .claude/skills/{domain}/{skill}.scpt
```

### Timeout errors

**Solutions**:
- Reduce query time range
- Add pagination
- Use more specific filters

### Unexpected results

**Solutions**:
- Add logging to trace execution
- Test with minimal dataset
- Verify timezone settings

## Next Steps

1. Review [Skills README](.claude/skills/README.md)
2. Check domain-specific READMEs
3. Use templates from `.claude/skills/_templates/`
4. Test with example skill: `example_get_inbox_count.scpt`
5. Create your first skill!

## Resources

- [AppleScript Language Guide](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/)
- [Mail Scripting Dictionary](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/MailScriptingRef/)
- [Calendar Scripting Dictionary](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/CalendarScriptingRef/)
- [Reminders Scripting Dictionary](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/RemindersScriptingRef/)
- [Issue Tracker](https://github.com/ronnycoding/my-personal-agents/issues)
