-- test_data_generator.scpt
-- Generate test data for Calendar, Reminders, and Mail
-- Provides functions to create test resources safely

-- Test resource naming convention
property testPrefix : "TEST-PersonalAgents-"

-- Generate unique test identifier
on generateTestId()
	set now to current date
	set timeStamp to (year of now as string) & ¬
		((month of now as integer) as string) & ¬
		(day of now as string) & "-" & ¬
		(time of now as string)
	return testPrefix & timeStamp
end generateTestId

-- ========================================
-- CALENDAR TEST DATA
-- ========================================

-- Create test calendar
on createTestCalendar()
	set calendarName to testPrefix & "Calendar"

	tell application "Calendar"
		try
			-- Check if test calendar already exists
			set existingCal to calendar calendarName
			log "Test calendar already exists: " & calendarName
			return {success:true, calendar:calendarName, created:false}
		on error
			-- Calendar doesn't exist, create it
			make new calendar with properties {name:calendarName}
			log "Created test calendar: " & calendarName
			return {success:true, calendar:calendarName, created:true}
		end try
	end tell
end createTestCalendar

-- Create test event in test calendar
on createTestEvent(eventSummary, startDate, endDate)
	set calInfo to createTestCalendar()
	set calendarName to calendar of calInfo

	tell application "Calendar"
		set testCal to calendar calendarName
		set newEvent to make new event at testCal with properties {¬
			summary:eventSummary, ¬
			start date:startDate, ¬
			end date:endDate¬
		}

		return {¬
			success:true, ¬
			eventId:uid of newEvent, ¬
			summary:summary of newEvent, ¬
			calendar:calendarName¬
		}
	end tell
end createTestEvent

-- Create multiple test events with gaps
on createTestSchedule(baseDate, eventCount)
	set events to {}
	set currentTime to baseDate

	repeat with i from 1 to eventCount
		set startTime to currentTime
		set endTime to currentTime + (1 * hours)

		set eventResult to createTestEvent("Test Event " & i, startTime, endTime)
		set end of events to eventResult

		-- Add 2 hour gap between events
		set currentTime to endTime + (2 * hours)
	end repeat

	return {success:true, events:events, count:eventCount}
end createTestSchedule

-- ========================================
-- REMINDERS TEST DATA
-- ========================================

-- Create test reminder list
on createTestReminderList()
	set listName to testPrefix & "Tasks"

	tell application "Reminders"
		try
			-- Check if test list already exists
			set existingList to list listName
			log "Test reminder list already exists: " & listName
			return {success:true, listName:listName, created:false}
		on error
			-- List doesn't exist, create it
			make new list with properties {name:listName}
			log "Created test reminder list: " & listName
			return {success:true, listName:listName, created:true}
		end try
	end tell
end createTestReminderList

-- Create test reminder
on createTestReminder(reminderName, dueDate, priority)
	set listInfo to createTestReminderList()
	set listName to listName of listInfo

	tell application "Reminders"
		set testList to list listName

		if dueDate is missing value then
			set newReminder to make new reminder at testList with properties {¬
				name:reminderName, ¬
				priority:priority¬
			}
		else
			set newReminder to make new reminder at testList with properties {¬
				name:reminderName, ¬
				due date:dueDate, ¬
				priority:priority¬
			}
		end if

		return {¬
			success:true, ¬
			reminderId:id of newReminder, ¬
			name:name of newReminder, ¬
			listName:listName¬
		}
	end tell
end createTestReminder

-- Create multiple test reminders
on createTestReminders(count)
	set reminders to {}
	set baseDate to current date

	repeat with i from 1 to count
		set dueDate to baseDate + (i * days)
		set priorityLevel to (i mod 10) -- Priorities 0-9

		set reminderResult to createTestReminder("Test Task " & i, dueDate, priorityLevel)
		set end of reminders to reminderResult
	end repeat

	return {success:true, reminders:reminders, count:count}
end createTestReminders

-- ========================================
-- DATE/TIME HELPERS
-- ========================================

-- Get date for testing (today + offset days)
on getTestDate(offsetDays)
	set testDate to (current date) + (offsetDays * days)
	return testDate
end getTestDate

-- Get date range for testing
on getTestDateRange(startOffset, endOffset)
	set startDate to getTestDate(startOffset)
	set endDate to getTestDate(endOffset)
	return {startDate:startDate, endDate:endDate}
end getTestDateRange

-- Create datetime with specific time
on createDateTime(baseDate, hour, minute)
	set newDate to baseDate
	set hours of newDate to hour
	set minutes of newDate to minute
	set seconds of newDate to 0
	return newDate
end createDateTime

-- ========================================
-- MOCK DATA GENERATION
-- ========================================

-- Generate mock email data (returns structured record, doesn't actually create emails)
on generateMockEmail(subject, sender, hasDeadline)
	set mockEmail to {¬
		subject:subject, ¬
		sender:sender, ¬
		dateReceived:(current date), ¬
		readStatus:false, ¬
		hasDeadline:hasDeadline¬
	}

	if hasDeadline then
		set deadline of mockEmail to (current date) + (3 * days)
	end if

	return mockEmail
end generateMockEmail

-- Generate multiple mock emails
on generateMockEmails(count)
	set emails to {}
	set senders to {"test@example.com", "important@company.com", "team@project.org"}

	repeat with i from 1 to count
		set senderIndex to ((i mod 3) + 1)
		set sender to item senderIndex of senders
		set hasDeadline to (i mod 2 = 0)

		set mockEmail to generateMockEmail("Test Email " & i, sender, hasDeadline)
		set end of emails to mockEmail
	end repeat

	return {success:true, emails:emails, count:count}
end generateMockEmails

-- ========================================
-- PRESET TEST SCENARIOS
-- ========================================

-- Create a busy day scenario
on createBusyDayScenario()
	set today to current date
	set morningStart to createDateTime(today, 9, 0)

	-- Create 6 meetings throughout the day
	set meeting1 to createTestEvent("Morning Standup", morningStart, morningStart + (30 * minutes))
	set meeting2 to createTestEvent("Project Review", morningStart + (2 * hours), morningStart + (3 * hours))
	set meeting3 to createTestEvent("Client Call", morningStart + (4 * hours), morningStart + (5 * hours))
	set meeting4 to createTestEvent("Lunch", morningStart + (3 * hours) + (30 * minutes), morningStart + (4 * hours))
	set meeting5 to createTestEvent("Team Sync", morningStart + (6 * hours), morningStart + (6 * hours) + (30 * minutes))
	set meeting6 to createTestEvent("EOD Wrap-up", morningStart + (8 * hours), morningStart + (8 * hours) + (30 * minutes))

	return {¬
		success:true, ¬
		scenario:"Busy Day", ¬
		eventCount:6, ¬
		date:today¬
	}
end createBusyDayScenario

-- Create a sparse schedule scenario
on createSparseScheduleScenario()
	set today to current date
	set morningStart to createDateTime(today, 10, 0)

	-- Only 2 meetings with large gaps
	set meeting1 to createTestEvent("Quick Sync", morningStart, morningStart + (30 * minutes))
	set meeting2 to createTestEvent("Afternoon Check-in", morningStart + (5 * hours), morningStart + (5 * hours) + (30 * minutes))

	return {¬
		success:true, ¬
		scenario:"Sparse Schedule", ¬
		eventCount:2, ¬
		date:today¬
	}
end createSparseScheduleScenario

-- Create conflicting events scenario
on createConflictingEventsScenario()
	set today to current date
	set conflictTime to createDateTime(today, 14, 0)

	-- Create two overlapping events
	set event1 to createTestEvent("Meeting A", conflictTime, conflictTime + (1 * hours))
	set event2 to createTestEvent("Meeting B (CONFLICT)", conflictTime + (30 * minutes), conflictTime + (1 * hours) + (30 * minutes))

	return {¬
		success:true, ¬
		scenario:"Conflicting Events", ¬
		eventCount:2, ¬
		hasConflict:true¬
	}
end createConflictingEventsScenario

-- Example usage:
-- set generator to load script file "tests/framework/test_data_generator.scpt"
-- set calResult to generator's createTestCalendar()
-- set eventResult to generator's createTestEvent("Test Meeting", (current date), (current date) + (1 * hours))
-- set busyDay to generator's createBusyDayScenario()
