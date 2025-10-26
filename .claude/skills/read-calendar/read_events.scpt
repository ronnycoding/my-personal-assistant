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
		set allEvents to events whose (start date ≥ startDate and start date ≤ endDate)
		set eventList to {}

		repeat with evt in allEvents
			set eventData to {¬
				summary:summary of evt, ¬
				startDate:start date of evt, ¬
				endDate:end date of evt, ¬
				location:location of evt, ¬
				calendarName:name of calendar of evt¬
			}
			set end of eventList to eventData
		end repeat

		return {success:true, events:eventList, count:(count of eventList)}
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
