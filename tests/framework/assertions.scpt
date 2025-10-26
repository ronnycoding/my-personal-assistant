-- assertions.scpt
-- AppleScript assertion helpers for testing skills
-- Provides common test assertions with clear error messages

-- Properties to track test results
property testsPassed : 0
property testsFailed : 0
property currentTestName : ""

-- Reset test counters
on resetCounters()
	set testsPassed to 0
	set testsFailed to 0
	set currentTestName to ""
end resetCounters

-- Get test results summary
on getResults()
	return {¬
		passed:testsPassed, ¬
		failed:testsFailed, ¬
		total:(testsPassed + testsFailed), ¬
		success:(testsFailed = 0)¬
	}
end getResults

-- Print test results
on printResults()
	set results to getResults()
	set totalTests to total of results

	log "======================================"
	log "Test Results Summary"
	log "======================================"
	log "Total tests: " & totalTests
	log "Passed: " & (passed of results) & " ✅"
	log "Failed: " & (failed of results) & " ❌"
	log "======================================"

	if success of results then
		log "All tests passed! ✅"
	else
		log "Some tests failed ❌"
	end if

	return results
end printResults

-- Record test pass
on recordPass(testName)
	set testsPassed to testsPassed + 1
	log "✅ PASS: " & testName
end recordPass

-- Record test failure
on recordFail(testName, message)
	set testsFailed to testsFailed + 1
	log "❌ FAIL: " & testName
	log "   " & message
end recordFail

-- assertEqual: Check if two values are equal
on assertEqual(actual, expected, testName)
	set currentTestName to testName

	if actual = expected then
		recordPass(testName)
		return true
	else
		recordFail(testName, "Expected: " & expected & ", Got: " & actual)
		return false
	end if
end assertEqual

-- assertNotEqual: Check if two values are different
on assertNotEqual(actual, unexpected, testName)
	set currentTestName to testName

	if actual ≠ unexpected then
		recordPass(testName)
		return true
	else
		recordFail(testName, "Expected values to be different, both were: " & actual)
		return false
	end if
end assertNotEqual

-- assertTrue: Check if value is true
on assertTrue(value, testName)
	set currentTestName to testName

	if value is true then
		recordPass(testName)
		return true
	else
		recordFail(testName, "Expected: true, Got: " & value)
		return false
	end if
end assertTrue

-- assertFalse: Check if value is false
on assertFalse(value, testName)
	set currentTestName to testName

	if value is false then
		recordPass(testName)
		return true
	else
		recordFail(testName, "Expected: false, Got: " & value)
		return false
	end if
end assertFalse

-- assertNotEmpty: Check if value is not empty
on assertNotEmpty(value, testName)
	set currentTestName to testName

	try
		if value is not "" and value is not {} and value is not missing value then
			if class of value is list then
				if (count of value) > 0 then
					recordPass(testName)
					return true
				else
					recordFail(testName, "List is empty")
					return false
				end if
			else
				recordPass(testName)
				return true
			end if
		else
			recordFail(testName, "Value is empty")
			return false
		end if
	on error
		recordFail(testName, "Error checking if value is empty")
		return false
	end try
end assertNotEmpty

-- assertEmpty: Check if value is empty
on assertEmpty(value, testName)
	set currentTestName to testName

	try
		if value is "" or value is {} or value is missing value then
			recordPass(testName)
			return true
		else if class of value is list then
			if (count of value) = 0 then
				recordPass(testName)
				return true
			else
				recordFail(testName, "Expected empty list, got " & (count of value) & " items")
				return false
			end if
		else
			recordFail(testName, "Value is not empty: " & value)
			return false
		end if
	on error
		recordFail(testName, "Error checking if value is empty")
		return false
	end try
end assertEmpty

-- assertGreaterThan: Check if value is greater than minimum
on assertGreaterThan(value, minimum, testName)
	set currentTestName to testName

	if value > minimum then
		recordPass(testName)
		return true
	else
		recordFail(testName, "Expected > " & minimum & ", Got: " & value)
		return false
	end if
end assertGreaterThan

-- assertLessThan: Check if value is less than maximum
on assertLessThan(value, maximum, testName)
	set currentTestName to testName

	if value < maximum then
		recordPass(testName)
		return true
	else
		recordFail(testName, "Expected < " & maximum & ", Got: " & value)
		return false
	end if
end assertLessThan

-- assertInRange: Check if value is within range (inclusive)
on assertInRange(value, minValue, maxValue, testName)
	set currentTestName to testName

	if value >= minValue and value <= maxValue then
		recordPass(testName)
		return true
	else
		recordFail(testName, "Expected value in range [" & minValue & ", " & maxValue & "], Got: " & value)
		return false
	end if
end assertInRange

-- assertContains: Check if list contains item
on assertContains(theList, item, testName)
	set currentTestName to testName

	try
		if theList contains item then
			recordPass(testName)
			return true
		else
			recordFail(testName, "List does not contain: " & item)
			return false
		end if
	on error
		recordFail(testName, "Error checking if list contains item")
		return false
	end try
end assertContains

-- assertDateInRange: Check if date is within range
on assertDateInRange(targetDate, startDate, endDate, testName)
	set currentTestName to testName

	if targetDate >= startDate and targetDate <= endDate then
		recordPass(testName)
		return true
	else
		recordFail(testName, "Date " & targetDate & " not in range [" & startDate & ", " & endDate & "]")
		return false
	end if
end assertDateInRange

-- assertSuccess: Check if result record has success=true
on assertSuccess(resultRecord, testName)
	set currentTestName to testName

	try
		if success of resultRecord is true then
			recordPass(testName)
			return true
		else
			set errMsg to "Operation failed"
			try
				set errMsg to errorMessage of resultRecord
			end try
			recordFail(testName, errMsg)
			return false
		end if
	on error
		recordFail(testName, "Result does not have 'success' property")
		return false
	end try
end assertSuccess

-- assertFailure: Check if result record has success=false
on assertFailure(resultRecord, testName)
	set currentTestName to testName

	try
		if success of resultRecord is false then
			recordPass(testName)
			return true
		else
			recordFail(testName, "Expected operation to fail, but it succeeded")
			return false
		end if
	on error
		recordFail(testName, "Result does not have 'success' property")
		return false
	end try
end assertFailure

-- assertCountEqual: Check if count matches expected
on assertCountEqual(theList, expectedCount, testName)
	set currentTestName to testName
	set actualCount to count of theList

	if actualCount = expectedCount then
		recordPass(testName)
		return true
	else
		recordFail(testName, "Expected count: " & expectedCount & ", Got: " & actualCount)
		return false
	end if
end assertCountEqual

-- assertHasProperty: Check if record has specified property
on assertHasProperty(theRecord, propertyName, testName)
	set currentTestName to testName

	try
		-- Attempt to access the property
		set testValue to propertyName of theRecord
		recordPass(testName)
		return true
	on error
		recordFail(testName, "Record does not have property: " & propertyName)
		return false
	end try
end assertHasProperty

-- Example usage in tests:
-- set assertions to load script file "tests/framework/assertions.scpt"
-- assertions's resetCounters()
-- assertions's assertEqual(5, 5, "Basic equality test")
-- assertions's assertNotEmpty(myList, "List should not be empty")
-- set results to assertions's printResults()
