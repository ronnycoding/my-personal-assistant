-- example_get_inbox_count.scpt
-- Example skill: Get count of inbox messages
-- Demonstrates basic Mail automation

on run argv
	try
		set skillResult to getInboxCount()
		return skillResult
	on error errMsg number errNum
		return {¬
			success:false, ¬
			errorMessage:errMsg, ¬
			errorNumber:errNum, ¬
			suggestion:"Check Mail automation permissions"¬
		}
	end try
end run

on getInboxCount()
	tell application "Mail"
		set allInboxes to mailbox "INBOX" of every account
		set totalMessages to 0
		set totalUnread to 0

		repeat with anInbox in allInboxes
			try
				set inboxMessages to messages of anInbox
				set totalMessages to totalMessages + (count of inboxMessages)

				set unreadMessages to (messages of anInbox whose read status is false)
				set totalUnread to totalUnread + (count of unreadMessages)
			end try
		end repeat

		return {¬
			success:true, ¬
			total_messages:totalMessages, ¬
			unread_messages:totalUnread, ¬
			timestamp:(current date) as string¬
		}
	end tell
end getInboxCount
