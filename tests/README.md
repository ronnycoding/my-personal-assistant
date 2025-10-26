# AppleScript Testing Framework

Comprehensive testing framework for validating AppleScript skills with assertions, test data generation, and cleanup utilities.

## Quick Start

### Run All Tests
```bash
./tests/framework/run_tests.sh
```

### Run Specific Domain Tests
```bash
./tests/framework/run_tests.sh --domain apple-mail
```

### Clean Up Before Testing
```bash
./tests/framework/run_tests.sh --cleanup
```

## Framework Components

### 1. Assertions (`framework/assertions.scpt`)

Comprehensive assertion library for AppleScript tests:

**Basic Assertions:**
- `assertEqual(actual, expected, testName)` - Check equality
- `assertNotEqual(actual, unexpected, testName)` - Check inequality
- `assertTrue(value, testName)` - Check if true
- `assertFalse(value, testName)` - Check if false

**Collection Assertions:**
- `assertNotEmpty(value, testName)` - Check not empty
- `assertEmpty(value, testName)` - Check empty
- `assertCountEqual(list, count, testName)` - Check list size
- `assertContains(list, item, testName)` - Check list contains item

**Numeric Assertions:**
- `assertGreaterThan(value, minimum, testName)` - Check > minimum
- `assertLessThan(value, maximum, testName)` - Check < maximum
- `assertInRange(value, min, max, testName)` - Check within range

**Record Assertions:**
- `assertSuccess(record, testName)` - Check success:true
- `assertFailure(record, testName)` - Check success:false
- `assertHasProperty(record, property, testName)` - Check property exists

**Date Assertions:**
- `assertDateInRange(date, start, end, testName)` - Check date in range

### 2. Test Data Generator (`framework/test_data_generator.scpt`)

Generate test data for Calendar, Reminders, and mocked emails:

**Calendar:**
- `createTestCalendar()` - Create test calendar
- `createTestEvent(summary, startDate, endDate)` - Create event
- `createTestSchedule(baseDate, count)` - Create multiple events with gaps

**Reminders:**
- `createTestReminderList()` - Create test list
- `createTestReminder(name, dueDate, priority)` - Create reminder
- `createTestReminders(count)` - Create multiple reminders

**Scenarios:**
- `createBusyDayScenario()` - Packed schedule with 6 meetings
- `createSparseScheduleScenario()` - Light schedule with gaps
- `createConflictingEventsScenario()` - Overlapping events

**Mock Data:**
- `generateMockEmail(subject, sender, hasDeadline)` - Mock email
- `generateMockEmails(count)` - Multiple mock emails

**Date Helpers:**
- `getTestDate(offsetDays)` - Date relative to today
- `getTestDateRange(startOffset, endOffset)` - Date range
- `createDateTime(baseDate, hour, minute)` - Specific time

### 3. Cleanup (`framework/cleanup.scpt`)

Clean up test data after testing:

**Data Cleanup:**
- `cleanupTestEvents()` - Delete all test events
- `cleanupTestReminders()` - Delete all test reminders
- `cleanupAllTestData()` - Delete all test data

**Resource Deletion:**
- `deleteTestCalendar()` - Delete test calendar
- `deleteTestReminderList()` - Delete test reminder list
- `deleteAllTestResources()` - Delete all test containers

**Safe Cleanup:**
- `safeCleanup(deleteContainers)` - Clean with verification
- `verifyCleanup()` - Verify cleanup completed

### 4. Test Runner (`framework/run_tests.sh`)

Bash script to execute all tests with reporting:

```bash
# Usage
./tests/framework/run_tests.sh [OPTIONS]

# Options
--domain DOMAIN    # Run specific domain tests
--cleanup          # Clean up before testing
--verbose          # Show verbose output
--help             # Show help
```

### 5. Permission Verifier (`framework/verify_permissions.sh`)

Verify macOS automation permissions before testing.

## Writing Tests

### Test File Structure

```applescript
-- test_my_skill.scpt
-- Test for my_skill functionality

property testsPassed : 0
property testsFailed : 0

-- Helper: Record pass
on recordPass(testName)
	set testsPassed to testsPassed + 1
	log "✅ PASS: " & testName
end recordPass

-- Helper: Record fail
on recordFail(testName, message)
	set testsFailed to testsFailed + 1
	log "❌ FAIL: " & testName & " - " & message
end recordFail

-- Test 1: Valid input
on testValidInput()
	set result to run script file "path/to/my_skill.scpt" with parameters {24, false}

	if success of result is true then
		recordPass("Valid input test")
	else
		recordFail("Valid input test", "Skill failed: " & errorMessage of result)
	end if
end testValidInput

-- Test 2: Invalid input
on testInvalidInput()
	try
		set result to run script file "path/to/my_skill.scpt" with parameters {-1, false}

		if success of result is false then
			recordPass("Invalid input test")
		else
			recordFail("Invalid input test", "Should have failed with invalid input")
		end if
	on error errMsg
		recordPass("Invalid input test - Error caught: " & errMsg)
	end try
end testInvalidInput

-- Run all tests
testValidInput()
testInvalidInput()

-- Summary
log "======================================"
log "Passed: " & testsPassed & " ✅"
log "Failed: " & testsFailed & " ❌"
log "======================================"

if testsFailed = 0 then
	return "All tests passed ✅"
else
	return "Some tests failed ❌"
end if
```

### Using Assertions

```applescript
-- Load assertion framework
set assertions to load script POSIX file "/path/to/assertions.scpt"
assertions's resetCounters()

-- Use assertions
assertions's assertEqual(actual, expected, "Test name")
assertions's assertNotEmpty(myList, "List should not be empty")
assertions's assertSuccess(result, "Operation should succeed")

-- Print results
set results to assertions's printResults()
```

### Using Test Data

```applescript
-- Load generator
set generator to load script POSIX file "/path/to/test_data_generator.scpt"

-- Create test calendar
set calResult to generator's createTestCalendar()

-- Create test event
set eventResult to generator's createTestEvent("Test Meeting", ¬
	(current date), (current date) + (1 * hours))

-- Create busy day
set busyDay to generator's createBusyDayScenario()
```

### Cleanup After Tests

```applescript
-- Load cleanup utilities
set cleanup to load script POSIX file "/path/to/cleanup.scpt"

-- Clean up test data
cleanup's cleanupAllTestData()

-- Or delete everything
cleanup's deleteAllTestResources()

-- Verify cleanup
set verification to cleanup's verifyCleanup()
if isClean of verification is true then
	log "Cleanup successful"
end if
```

## Test Isolation

All test resources use the `TEST-PersonalAgents-` prefix:

- **Calendar**: `TEST-PersonalAgents-Calendar`
- **Reminder List**: `TEST-PersonalAgents-Tasks`
- **Events**: Created in test calendar only
- **Reminders**: Created in test list only

This ensures production data is never affected.

## Running Tests

### Individual Test
```bash
osascript tests/framework/test_assertions_simple.scpt
```

### Domain Tests
```bash
osascript tests/apple-mail/test_scan_inbox.scpt
osascript tests/calendar/test_read_events.scpt
```

### All Tests
```bash
./tests/framework/run_tests.sh
```

### With Cleanup
```bash
./tests/framework/run_tests.sh --cleanup
```

## Best Practices

### 1. Test Naming
- Prefix test files with `test_`
- Use descriptive names: `test_scan_inbox.scpt`

### 2. Test Independence
- Each test should be independent
- Don't rely on execution order
- Clean up test data after each test

### 3. Test Coverage
- Test valid inputs
- Test invalid inputs
- Test edge cases (empty data, large datasets)
- Test error handling

### 4. Assertions
- Use descriptive test names
- One assertion per logical check
- Provide helpful failure messages

### 5. Test Data
- Use test isolation (TEST- prefix)
- Clean up after tests
- Don't use production data

### 6. Performance
- Keep tests fast (< 5 seconds each)
- Use small datasets
- Mock when possible

## Example Tests

### Simple Assertion Test
```applescript
property testsPassed : 0
property testsFailed : 0

on assertEqual(actual, expected, testName)
	if actual = expected then
		set testsPassed to testsPassed + 1
		log "✅ PASS: " & testName
	else
		set testsFailed to testsFailed + 1
		log "❌ FAIL: " & testName
	end if
end assertEqual

-- Run tests
assertEqual(5, 5, "Basic test")
assertEqual(count of {1,2,3}, 3, "List count test")

-- Results
if testsFailed = 0 then
	return "SUCCESS"
else
	return "FAILURE"
end if
```

### Integration Test
```applescript
-- Test email to reminder workflow
set generator to load script POSIX file "/path/to/test_data_generator.scpt"
set assertions to load script POSIX file "/path/to/assertions.scpt"

-- Create test data
set mockEmails to generator's generateMockEmails(5)

-- Run email scanning skill
set scanResult to run script file "scan_inbox.scpt" with parameters {24, false}

-- Verify results
assertions's assertSuccess(scanResult, "Scan should succeed")
assertions's assertGreaterThan(unread_count of scanResult, 0, "Should have unread emails")

-- Print results
assertions's printResults()
```

## Troubleshooting

### Tests Won't Run
**Issue**: Permission errors
**Solution**: Run `./tests/framework/verify_permissions.sh`

### Test Data Not Cleaned
**Issue**: Cleanup script fails
**Solution**: Manually delete test calendar and reminder list

### Assertions Not Found
**Issue**: Cannot load script
**Solution**: Use absolute POSIX paths to framework files

### Tests Timeout
**Issue**: AppleScript operations too slow
**Solution**: Reduce test data size or add pagination

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run AppleScript Tests
  run: |
    ./tests/framework/verify_permissions.sh
    ./tests/framework/run_tests.sh --cleanup
```

## Resources

- [Assertions Reference](framework/assertions.scpt)
- [Test Data Generator](framework/test_data_generator.scpt)
- [Cleanup Utilities](framework/cleanup.scpt)
- [Skills API Guide](../docs/SKILLS_API.md)
- [Issue #4](https://github.com/ronnycoding/my-personal-agents/issues/4)
