-- list_tasks.scpt
-- List reminders from macOS Reminders

on run argv
	try
		set result to listTasks()
		return result
	on error errMsg number errNum
		return {success:false, errorMessage:errMsg, errorNumber:errNum}
	end try
end run

on listTasks()
	tell application "Reminders"
		set allLists to lists
		set allTasks to {}
		set overdueTasks to {}
		set todayTasks to {}

		set today to current date
		set hours of today to 0
		set minutes of today to 0
		set seconds of today to 0

		repeat with reminderList in allLists
			set listName to name of reminderList
			set reminderItems to reminders of reminderList

			repeat with aReminder in reminderItems
				if completed of aReminder is false then
					set taskData to {taskName:(name of aReminder), listName:listName, taskPriority:(priority of aReminder), isCompleted:(completed of aReminder)}

					try
						set taskDueDate to due date of aReminder
						set taskData to taskData & {dueDate:taskDueDate}

						if taskDueDate < today then
							set end of overdueTasks to taskData
						else if taskDueDate is greater than or equal to today and taskDueDate < (today + (1 * days)) then
							set end of todayTasks to taskData
						end if
					on error
						-- No due date
					end try

					set end of allTasks to taskData
				end if
			end repeat
		end repeat

		return {success:true, totalTasks:(count of allTasks), overdueCount:(count of overdueTasks), todayCount:(count of todayTasks), tasks:allTasks, overdue:overdueTasks, todayTasks:todayTasks}
	end tell
end listTasks
