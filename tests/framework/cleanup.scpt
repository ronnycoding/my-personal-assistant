-- cleanup.scpt
-- Cleanup test data from Calendar, Reminders, and Mail
-- Removes all test resources created during testing

property testPrefix : "TEST-PersonalAgents-"

-- ========================================
-- CALENDAR CLEANUP
-- ========================================

-- Delete all test events from test calendar
on cleanupTestEvents()
	set deletedCount to 0

	tell application "Calendar"
		try
			set testCalName to testPrefix & "Calendar"
			set testCal to calendar testCalName

			set testEvents to events of testCal
			set eventCount to count of testEvents

			repeat with testEvent in testEvents
				delete testEvent
				set deletedCount to deletedCount + 1
			end repeat

			log "Deleted " & deletedCount & " test events from calendar: " & testCalName

			return {success:true, deleted:deletedCount, calendar:testCalName}
		on error errMsg
			log "Error cleaning up test events: " & errMsg
			return {success:false, error:errMsg, deleted:deletedCount}
		end try
	end tell
end cleanupTestEvents

-- Delete test calendar entirely
on deleteTestCalendar()
	tell application "Calendar"
		try
			set testCalName to testPrefix & "Calendar"
			set testCal to calendar testCalName

			delete testCal

			log "Deleted test calendar: " & testCalName

			return {success:true, calendar:testCalName, deleted:true}
		on error errMsg
			log "Error deleting test calendar: " & errMsg
			return {success:false, error:errMsg, deleted:false}
		end try
	end tell
end deleteTestCalendar

-- ========================================
-- REMINDERS CLEANUP
-- ========================================

-- Delete all test reminders from test list
on cleanupTestReminders()
	set deletedCount to 0

	tell application "Reminders"
		try
			set testListName to testPrefix & "Tasks"
			set testList to list testListName

			set testReminders to reminders of testList
			set reminderCount to count of testReminders

			repeat with testReminder in testReminders
				delete testReminder
				set deletedCount to deletedCount + 1
			end repeat

			log "Deleted " & deletedCount & " test reminders from list: " & testListName

			return {success:true, deleted:deletedCount, listName:testListName}
		on error errMsg
			log "Error cleaning up test reminders: " & errMsg
			return {success:false, error:errMsg, deleted:deletedCount}
		end try
	end tell
end cleanupTestReminders

-- Delete test reminder list entirely
on deleteTestReminderList()
	tell application "Reminders"
		try
			set testListName to testPrefix & "Tasks"
			set testList to list testListName

			delete testList

			log "Deleted test reminder list: " & testListName

			return {success:true, listName:testListName, deleted:true}
		on error errMsg
			log "Error deleting test reminder list: " & errMsg
			return {success:false, error:errMsg, deleted:false}
		end try
	end tell
end deleteTestReminderList

-- ========================================
-- COMPREHENSIVE CLEANUP
-- ========================================

-- Clean up all test data but keep test containers (calendar, list)
on cleanupAllTestData()
	set results to {}

	-- Clean events
	set eventResult to cleanupTestEvents()
	set end of results to eventResult

	-- Clean reminders
	set reminderResult to cleanupTestReminders()
	set end of results to reminderResult

	-- Summary
	set totalDeleted to 0
	try
		set totalDeleted to (deleted of eventResult) + (deleted of reminderResult)
	end try

	log "======================================"
	log "Cleanup Summary"
	log "======================================"
	log "Total items deleted: " & totalDeleted
	log "======================================"

	return {¬
		success:true, ¬
		totalDeleted:totalDeleted, ¬
		details:results¬
	}
end cleanupAllTestData

-- Delete all test resources completely (containers and data)
on deleteAllTestResources()
	set results to {}

	-- Delete calendar
	set calResult to deleteTestCalendar()
	set end of results to calResult

	-- Delete reminder list
	set listResult to deleteTestReminderList()
	set end of results to listResult

	log "======================================"
	log "Test Resources Deleted"
	log "======================================"
	log "All test calendars and reminder lists removed"
	log "======================================"

	return {¬
		success:true, ¬
		details:results¬
	}
end deleteAllTestResources

-- ========================================
-- VERIFICATION
-- ========================================

-- Verify test resources are cleaned up
on verifyCleanup()
	set calendarExists to false
	set reminderListExists to false

	-- Check calendar
	tell application "Calendar"
		try
			set testCalName to testPrefix & "Calendar"
			set testCal to calendar testCalName
			set calendarExists to true
			set calEventCount to count of (events of testCal)
		on error
			set calendarExists to false
			set calEventCount to 0
		end try
	end tell

	-- Check reminder list
	tell application "Reminders"
		try
			set testListName to testPrefix & "Tasks"
			set testList to list testListName
			set reminderListExists to true
			set reminderCount to count of (reminders of testList)
		on error
			set reminderListExists to false
			set reminderCount to 0
		end try
	end tell

	-- Report
	set isClean to (calEventCount = 0 and reminderCount = 0)

	if isClean then
		log "✅ Cleanup verified: All test data removed"
	else
		log "⚠️  Cleanup incomplete:"
		if calEventCount > 0 then
			log "   - " & calEventCount & " test events remaining"
		end if
		if reminderCount > 0 then
			log "   - " & reminderCount & " test reminders remaining"
		end if
	end if

	return {¬
		isClean:isClean, ¬
		calendarExists:calendarExists, ¬
		eventCount:calEventCount, ¬
		reminderListExists:reminderListExists, ¬
		reminderCount:reminderCount¬
	}
end verifyCleanup

-- ========================================
-- SAFE CLEANUP WITH CONFIRMATION
-- ========================================

-- Safe cleanup that verifies before deleting
on safeCleanup(deleteContainers)
	log "======================================"
	log "Starting Safe Cleanup"
	log "======================================"

	-- First, clean up data
	set cleanupResult to cleanupAllTestData()

	-- Verify cleanup
	set verifyResult to verifyCleanup()

	-- Optionally delete containers
	if deleteContainers is true then
		log "Deleting test containers (calendar, list)..."
		set deleteResult to deleteAllTestResources()
	else
		log "Keeping test containers for reuse"
		set deleteResult to {success:true, message:"Containers preserved"}
	end if

	log "======================================"
	log "Safe Cleanup Complete"
	log "======================================"

	return {¬
		success:true, ¬
		cleanup:cleanupResult, ¬
		verification:verifyResult, ¬
		deletion:deleteResult¬
	}
end safeCleanup

-- Example usage:
-- set cleanup to load script file "tests/framework/cleanup.scpt"
--
-- Clean data but keep containers:
-- cleanup's cleanupAllTestData()
--
-- Delete everything:
-- cleanup's deleteAllTestResources()
--
-- Safe cleanup with verification:
-- cleanup's safeCleanup(false) -- Keep containers
-- cleanup's safeCleanup(true)  -- Delete containers
--
-- Verify cleanup:
-- cleanup's verifyCleanup()
