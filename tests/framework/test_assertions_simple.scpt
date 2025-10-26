-- test_assertions_simple.scpt
-- Simple test of assertion framework without dependencies

-- Test counter properties
property testsPassed : 0
property testsFailed : 0

-- Simple assertion functions inline
on assertEqual(actual, expected, testName)
	if actual = expected then
		set testsPassed to testsPassed + 1
		log "✅ PASS: " & testName
		return true
	else
		set testsFailed to testsFailed + 1
		log "❌ FAIL: " & testName & " - Expected: " & expected & ", Got: " & actual
		return false
	end if
end assertEqual

on assertTrue(value, testName)
	if value is true then
		set testsPassed to testsPassed + 1
		log "✅ PASS: " & testName
		return true
	else
		set testsFailed to testsFailed + 1
		log "❌ FAIL: " & testName
		return false
	end if
end assertTrue

-- Run tests
log "======================================"
log "Running Assertion Framework Tests"
log "======================================"

assertEqual(5, 5, "Basic equality test")
assertEqual("test", "test", "String equality test")
assertTrue(true, "Boolean true test")
assertEqual(10, 5 + 5, "Addition test")

set myList to {1, 2, 3}
assertEqual(count of myList, 3, "List count test")

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
