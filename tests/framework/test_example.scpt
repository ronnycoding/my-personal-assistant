-- test_example.scpt
-- Example test demonstrating testing framework usage
-- Shows how to use assertions, test data, and cleanup

-- Load testing framework using POSIX paths
set testDir to "/Users/ronnycoding/projects/my-agents/tests/framework"
set assertionsPath to POSIX file (testDir & "/assertions.scpt")
set generatorPath to POSIX file (testDir & "/test_data_generator.scpt")

set assertions to load script assertionsPath
set generator to load script generatorPath

-- Reset test counters
assertions's resetCounters()

log "======================================"
log "Running Example Tests"
log "======================================"

-- Test 1: Basic Assertions
on testBasicAssertions()
	assertions's assertEqual(5, 5, "Numbers should be equal")
	assertions's assertNotEqual(5, 10, "Numbers should be different")
	assertions's assertTrue(true, "Value should be true")
	assertions's assertFalse(false, "Value should be false")
end testBasicAssertions

-- Test 2: List Assertions
on testListAssertions()
	set myList to {1, 2, 3, 4, 5}
	assertions's assertNotEmpty(myList, "List should not be empty")
	assertions's assertCountEqual(myList, 5, "List should have 5 items")
	assertions's assertContains(myList, 3, "List should contain 3")
	assertions's assertGreaterThan(count of myList, 0, "Count should be greater than 0")
end testListAssertions

-- Test 3: Empty List Handling
on testEmptyList()
	set emptyList to {}
	assertions's assertEmpty(emptyList, "List should be empty")
	assertions's assertCountEqual(emptyList, 0, "Empty list count should be 0")
end testEmptyList

-- Test 4: Success/Failure Records
on testSuccessRecords()
	set successRecord to {success:true, data:"test"}
	assertions's assertSuccess(successRecord, "Record should indicate success")

	set failureRecord to {success:false, errorMessage:"test error"}
	assertions's assertFailure(failureRecord, "Record should indicate failure")
end testSuccessRecords

-- Test 5: Range Assertions
on testRangeAssertions()
	assertions's assertInRange(50, 0, 100, "Value should be in range")
	assertions's assertLessThan(5, 10, "5 should be less than 10")
	assertions's assertGreaterThan(10, 5, "10 should be greater than 5")
end testRangeAssertions

-- Test 6: Test Data Generation
on testDataGeneration()
	-- Test calendar creation
	set calResult to generator's createTestCalendar()
	assertions's assertSuccess(calResult, "Test calendar should be created")
	assertions's assertTrue(calendar of calResult contains "TEST-PersonalAgents", "Calendar name should have test prefix")

	-- Test reminder list creation
	set listResult to generator's createTestReminderList()
	assertions's assertSuccess(listResult, "Test reminder list should be created")

	-- Test date helpers
	set testDate to generator's getTestDate(5)
	assertions's assertGreaterThan(testDate, current date, "Test date should be in future")
end testDataGeneration

-- Test 7: Mock Data Generation
on testMockData()
	set mockEmails to generator's generateMockEmails(5)
	assertions's assertSuccess(mockEmails, "Mock emails should be generated")
	assertions's assertEqual(count of mockEmails, 5, "Should generate 5 mock emails")
end testMockData

-- Test 8: Record Properties
on testRecordProperties()
	set testRecord to {name:"Test", value:123, active:true}
	assertions's assertHasProperty(testRecord, "name", "Record should have 'name' property")
	assertions's assertHasProperty(testRecord, "value", "Record should have 'value' property")
	assertions's assertHasProperty(testRecord, "active", "Record should have 'active' property")
end testRecordProperties

-- Run all tests
try
	testBasicAssertions()
	testListAssertions()
	testEmptyList()
	testSuccessRecords()
	testRangeAssertions()
	testDataGeneration()
	testMockData()
	testRecordProperties()

	-- Print results
	set results to assertions's printResults()

	-- Return exit code
	if success of results then
		return "All example tests passed ✅"
	else
		return "Some example tests failed ❌"
	end if

on error errMsg
	log "Test execution error: " & errMsg
	return "Test execution failed: " & errMsg
end try
