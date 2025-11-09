-- test_scan_inbox.scpt
-- Tests for scan_inbox skill

property testsPassed : 0
property testsFailed : 0

on recordPass(testName)
	set testsPassed to testsPassed + 1
	log "✅ PASS: " & testName
end recordPass

on recordFail(testName, message)
	set testsFailed to testsFailed + 1
	log "❌ FAIL: " & testName & " - " & message
end recordFail

-- Test 1: Basic execution with default parameters
on testBasicExecution()
	try
		set skillResult to run script file ((path to me as text) & "::..:" & ":skills:apple-mail:scan_inbox.scpt") with parameters {24, false}

		if success of skillResult is true then
			recordPass("Basic execution")
		else
			recordFail("Basic execution", "Skill returned success:false")
		end if
	on error errMsg
		recordFail("Basic execution", errMsg)
	end try
end testBasicExecution

-- Test 2: Priority only mode
on testPriorityMode()
	try
		set skillResult to run script POSIX file "/Users/ronnycoding/projects/my-personal-assistant/.claude/skills/apple-mail/scan_inbox.scpt" with parameters {24, true}

		if success of skillResult is true and priorityOnly of skillResult is true then
			recordPass("Priority only mode")
		else
			recordFail("Priority only mode", "Priority mode not set correctly")
		end if
	on error errMsg
		recordFail("Priority only mode", errMsg)
	end try
end testPriorityMode

-- Test 3: Different time ranges
on testTimeRanges()
	try
		set skillResult to run script POSIX file "/Users/ronnycoding/projects/my-personal-assistant/.claude/skills/apple-mail/scan_inbox.scpt" with parameters {48, false}

		if success of skillResult is true and timeRange of skillResult is 48 then
			recordPass("Time range parameter")
		else
			recordFail("Time range parameter", "Time range not set correctly")
		end if
	on error errMsg
		recordFail("Time range parameter", errMsg)
	end try
end testTimeRanges

-- Test 4: Result structure validation
on testResultStructure()
	try
		set skillResult to run script POSIX file "/Users/ronnycoding/projects/my-personal-assistant/.claude/skills/apple-mail/scan_inbox.scpt" with parameters {24, false}

		set hasAllFields to true

		-- Check required fields exist
		try
			set temp to success of skillResult
			set temp to unreadCount of skillResult
			set temp to actionableCount of skillResult
			set temp to priorityCount of skillResult
		on error
			set hasAllFields to false
		end try

		if hasAllFields then
			recordPass("Result structure validation")
		else
			recordFail("Result structure validation", "Missing required fields")
		end if
	on error errMsg
		recordFail("Result structure validation", errMsg)
	end try
end testResultStructure

-- Run all tests
log "======================================"
log "Running scan_inbox Tests"
log "======================================"

testBasicExecution()
testPriorityMode()
testTimeRanges()
testResultStructure()

log "======================================"
log "Test Results"
log "======================================"
log "Passed: " & testsPassed & " ✅"
log "Failed: " & testsFailed & " ❌"
log "Total: " & (testsPassed + testsFailed)
log "======================================"

if testsFailed = 0 then
	log "All tests passed! ✅"
	return "SUCCESS"
else
	log "Some tests failed ❌"
	return "FAILURE"
end if
