-- scan_inbox.scpt
-- Scan Apple Mail inbox for unread and actionable messages
-- Part of Issue #5: Skill: Scan & Summarize Apple Mail

on run argv
	-- Parse parameters with defaults
	if (count of argv) > 0 then
		set timeRange to item 1 of argv as integer
	else
		set timeRange to 24 -- Default: last 24 hours
	end if

	if (count of argv) > 1 then
		set priorityOnly to item 2 of argv as boolean
	else
		set priorityOnly to false
	end if

	-- Execute skill
	try
		set skillResult to scanInbox(timeRange, priorityOnly)
		return skillResult
	on error errMsg number errNum
		return {¬
			success:false, ¬
			errorMessage:errMsg, ¬
			errorNumber:errNum, ¬
			suggestion:"Check Mail automation permissions in System Settings"¬
		}
	end try
end run

-- Main skill logic
on scanInbox(timeRange, priorityOnly)
	tell application "Mail"
		-- Calculate time boundary
		set now to current date
		set cutoffDate to now - (timeRange * hours)

		-- Collections for different message types
		set unreadMessages to {}
		set actionableMessages to {}
		set priorityMessages to {}

		-- Actionable keywords to detect
		set actionableKeywords to {"deadline", "urgent", "action required", "meeting", "request", "please review", "asap", "todo", "action item"}

		-- Get all inbox accounts
		set allInboxes to mailbox "INBOX" of every account

		-- Scan each inbox
		repeat with anInbox in allInboxes
			try
				set inboxMessages to messages of anInbox

				repeat with msg in inboxMessages
					try
						-- Only process messages within time range
						if date received of msg >= cutoffDate then
							-- Check if unread
							if read status of msg is false then
								set end of unreadMessages to msg

								-- Check for actionable keywords in subject
								set msgSubject to subject of msg
								set isActionable to false

								repeat with keyword in actionableKeywords
									if msgSubject contains keyword then
										set isActionable to true
										exit repeat
									end if
								end repeat

								if isActionable then
									set end of actionableMessages to msg
								end if

								-- Check for priority (VIP sender or flagged)
								try
									if flagged status of msg is true then
										set end of priorityMessages to msg
									end if
								end try
							end if
						end if
					end try
				end repeat
			end try
		end repeat

		-- Build result structure (return counts only for now to avoid extraction issues)
		if priorityOnly then
			-- Return only priority messages
			return {¬
				success:true, ¬
				unreadCount:count of unreadMessages, ¬
				actionableCount:count of actionableMessages, ¬
				priorityCount:count of priorityMessages, ¬
				timeRange:timeRange, ¬
				priorityOnly:true¬
			}
		else
			-- Return all categorized messages with details
			set unreadDetails to my extractEmailData(unreadMessages)
			set actionableDetails to my extractEmailData(actionableMessages)
			set priorityDetails to my extractEmailData(priorityMessages)

			return {¬
				success:true, ¬
				unreadCount:count of unreadMessages, ¬
				actionableCount:count of actionableMessages, ¬
				priorityCount:count of priorityMessages, ¬
				unreadList:unreadDetails, ¬
				actionableList:actionableDetails, ¬
				priorityList:priorityDetails, ¬
				timeRange:timeRange, ¬
				priorityOnly:false¬
			}
		end if
	end tell
end scanInbox

-- Extract relevant data from messages
on extractEmailData(messageList)
	set dataList to {}

	tell application "Mail"
		repeat with msg in messageList
			try
				-- Build email data record (without snippet to avoid permission issues)
				set emailData to {¬
					sender:sender of msg, ¬
					subject:subject of msg, ¬
					dateReceived:date received of msg, ¬
					isFlagged:flagged status of msg¬
				}

				set end of dataList to emailData
			on error errMsg
				-- Skip messages that error
				log "Skipping message due to error: " & errMsg
			end try
		end repeat
	end tell

	return dataList
end extractEmailData

-- Helper: Extract email address from sender string
on extractEmailAddress(senderString)
	try
		-- Sender format is usually "Name <email@domain.com>"
		if senderString contains "<" and senderString contains ">" then
			set AppleScript's text item delimiters to "<"
			set tempList to text items of senderString
			set emailPart to item 2 of tempList
			set AppleScript's text item delimiters to ">"
			set emailAddress to item 1 of (text items of emailPart)
			set AppleScript's text item delimiters to ""
			return emailAddress
		else
			return senderString
		end if
	on error
		return senderString
	end try
end extractEmailAddress

-- Example usage:
-- osascript scan_inbox.scpt 24 false
-- Returns: {success:true, unreadCount:X, actionableCount:Y, ...}
