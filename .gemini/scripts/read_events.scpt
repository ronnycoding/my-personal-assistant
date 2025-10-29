-- read_events.scpt
-- Read calendar events for date range

on run argv
	if (count of argv) < 2 then
		return {success:false, errorMessage:"Start and end dates required (YYYY-MM-DD format)"}
	end if

	set startDateStr to item 1 of argv
	set endDateStr to item 2 of argv

	try
		set startDate to parseDate(startDateStr)
		set endDate to parseDate(endDateStr)
		set result to readEvents(startDate, endDate)
		return result
	on error errMsg number errNum
		return {success:false, errorMessage:errMsg, errorNumber:errNum}
	end try
end run

on readEvents(startDate, endDate)
	tell application "Calendar"
		set allCalendars to calendars
		set eventList to {}

		repeat with cal in allCalendars
			try
				-- Get regular events in date range
				set allCalEvents to events of cal

				repeat with evt in allCalEvents
					set evtStartDate to start date of evt
					if evtStartDate is greater than or equal to startDate and evtStartDate is less than or equal to endDate then
						set eventData to {summary:(summary of evt), startDate:evtStartDate, endDate:(end date of evt), location:(location of evt), calendarName:(name of cal), isRecurring:false}
						set end of eventList to eventData
					end if
				end repeat

				-- Also check for recurring events that might apply to this date range
				-- Get events from slightly before the range to catch recurring patterns
				set extendedStart to startDate - (90 * days)
				set recurringCandidates to events of cal

				repeat with evt in recurringCandidates
					try
						set evtRecurrence to recurrence of evt
						if evtRecurrence is not missing value and evtRecurrence is not "" then
							-- This is a recurring event, check if any instance falls in our range
							set evtStartDate to start date of evt
							set evtEndDate to end date of evt
							set duration to evtEndDate - evtStartDate

							-- Check if the event's recurrence pattern intersects with our date range
							-- For weekly events, check each week in the range
							if evtRecurrence contains "FREQ=WEEKLY" then
								set currentDate to startDate
								repeat while currentDate is less than or equal to endDate
									set daysDiff to (currentDate - evtStartDate) / days as integer
									if daysDiff mod 7 = 0 and daysDiff ≥ 0 then
										set projectedStart to evtStartDate + (daysDiff * days)
										if projectedStart ≥ startDate and projectedStart ≤ endDate then
											set projectedEnd to projectedStart + duration
											set eventData to {summary:(summary of evt), startDate:projectedStart, endDate:projectedEnd, location:(location of evt), calendarName:(name of cal), isRecurring:true}
											set end of eventList to eventData
										end if
									end if
									set currentDate to currentDate + (1 * days)
								end repeat
							end if
						end if
					end try
				end repeat
			end try
		end repeat

		return {success:true, events:eventList, eventCount:(count of eventList)}
	end tell
end readEvents

on parseDate(dateStr)
	set {year:y, month:m, day:d} to current date
	set dateComponents to my split(dateStr, "-")
	set y to item 1 of dateComponents as integer
	set m to item 2 of dateComponents as integer
	set d to item 3 of dateComponents as integer

	set newDate to current date
	set year of newDate to y
	set month of newDate to m
	set day of newDate to d
	set hours of newDate to 0
	set minutes of newDate to 0
	set seconds of newDate to 0

	return newDate
end parseDate

on split(theString, theDelimiter)
	set oldDelimiters to AppleScript's text item delimiters
	set AppleScript's text item delimiters to theDelimiter
	set theArray to every text item of theString
	set AppleScript's text item delimiters to oldDelimiters
	return theArray
end split
