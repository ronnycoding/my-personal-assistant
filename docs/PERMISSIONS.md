# macOS Permissions Setup Guide

This guide walks you through configuring macOS permissions for the Personal Productivity Assistant to access Apple Mail, Calendar, and Reminders via AppleScript automation.

## Overview

The productivity agent requires permission to automate three macOS applications:
- **Apple Mail** - Read and organize emails
- **Calendar** - Read events and manage scheduling
- **Reminders** - Read and manage tasks

These permissions are granted through macOS System Settings and are required for the AppleScript skills to function.

## Prerequisites

- macOS 10.14 (Mojave) or later
- Terminal app or Claude Code CLI
- Apple Mail, Calendar, and Reminders apps installed

## Step-by-Step Setup

### 1. Open System Settings

1. Click the Apple menu () in the top-left corner
2. Select **System Settings** (macOS Ventura+) or **System Preferences** (earlier versions)

### 2. Navigate to Privacy & Security

1. In the left sidebar, click **Privacy & Security**
2. Scroll down to find the **Automation** section
3. Click **Automation**

### 3. Grant Automation Permissions

You'll need to grant permissions for the application you're using to run the scripts (Terminal or Claude Code).

#### For Terminal:

1. Find **Terminal** in the list
2. Enable the following checkboxes:
   - ✅ **Mail**
   - ✅ **Calendar**
   - ✅ **Reminders**

#### For Claude Code:

1. Find **Claude** (or the Claude Code app name) in the list
2. Enable the following checkboxes:
   - ✅ **Mail**
   - ✅ **Calendar**
   - ✅ **Reminders**

**Note:** If you don't see Terminal or Claude in the list, you may need to run the verification script first (see step 4), which will trigger permission prompts.

### 4. Full Disk Access (Optional)

For advanced Mail features (like accessing Mail database directly), you may need to grant Full Disk Access:

1. In **Privacy & Security**, click **Full Disk Access**
2. Click the **+** button
3. Navigate to and select **Terminal** or **Claude**
4. Enable the checkbox next to the app

**Note:** This is only required for certain advanced Mail operations and may not be necessary for basic functionality.

### 5. Verify Permissions

Run the permission verification script to confirm all permissions are set correctly:

```bash
cd /Users/ronnycoding/projects/my-agents
./tests/framework/verify_permissions.sh
```

Expected output:
```
Testing Apple Mail access...
✅ Mail access granted

Testing Calendar access...
✅ Calendar access granted

Testing Reminders access...
✅ Reminders access granted

All permissions verified successfully!
```

## Permission Prompts

The first time you run an AppleScript that accesses Mail, Calendar, or Reminders, macOS will display permission prompt dialogs:

### Example Prompt:
```
"Terminal" would like to control "Mail".
Allowing control will provide access to documents and data in "Mail",
and to perform actions within that app.

[Don't Allow]  [OK]
```

**Click "OK"** for each prompt to grant the necessary permissions.

## Troubleshooting

### Permission Denied Errors

If you see errors like:
```
execution error: Mail got an error: Not authorized to send Apple events to Mail.
```

**Solutions:**
1. Check that the app (Terminal/Claude) has Automation permissions for Mail
2. Try resetting permissions:
   - Remove the app from Automation settings
   - Re-add it by running the verification script
3. Restart the Terminal or Claude Code app

### Permissions Not Appearing in System Settings

If Terminal or Claude doesn't appear in the Automation list:

1. Run any AppleScript command manually to trigger the prompt:
   ```bash
   osascript -e 'tell application "Mail" to get name of inbox'
   ```
2. Click "OK" on the permission prompt
3. The app should now appear in System Settings → Privacy & Security → Automation

### Calendar/Reminders Not Accessible

If Calendar or Reminders permissions aren't working:

1. Verify the apps are installed and have been launched at least once
2. Check that iCloud sync is enabled (if using iCloud for Calendar/Reminders)
3. Try accessing the apps manually first to ensure they're set up correctly

### Script Timeout Issues

If scripts are timing out:

1. Reduce the time range for data queries (e.g., last 24 hours instead of 7 days)
2. Close and reopen Mail, Calendar, or Reminders apps
3. Restart your Mac if issues persist

## Security Considerations

### What Access Do These Permissions Grant?

- **Mail**: Read email content, sender/recipient info, modify flags, move messages
- **Calendar**: Read events, create/modify/delete events, access all calendars
- **Reminders**: Read tasks, create/modify/delete reminders, access all lists

### Best Practices

1. **Review Scripts Before Running**: Always review AppleScript files before execution
2. **Use Test Data**: Set up test calendars, reminder lists, and mail folders for development
3. **Limit Scope**: Skills should only access necessary data (e.g., inbox only, not all mail folders)
4. **Regular Audits**: Periodically review which apps have automation permissions
5. **Revoke When Not Needed**: Disable permissions when not actively using the agent

### Privacy Notes

- Scripts run locally on your Mac - no data is sent to external servers
- All email, calendar, and reminder data stays on your device
- Test data and personal data are separated via `.gitignore`
- Consider using separate Mail accounts or Calendar calendars for testing

## Timezone Configuration

The productivity assistant uses the **America/Costa_Rica** timezone by default.

To verify your system timezone:
```bash
sudo systemsetup -gettimezone
```

To change timezone (if needed):
```bash
sudo systemsetup -settimezone America/Costa_Rica
```

**Note:** AppleScript uses the system timezone for all date/time operations.

## Permission Reset (Advanced)

If you need to completely reset permissions for troubleshooting:

1. Open Terminal
2. Run the following command:
   ```bash
   tccutil reset AppleEvents
   ```
3. Restart your Mac
4. Re-grant permissions using the steps above

**Warning:** This will reset ALL Apple Events permissions, not just for Mail/Calendar/Reminders.

## Testing Permissions

### Manual Tests

Test each app individually:

**Mail:**
```bash
osascript -e 'tell application "Mail" to get name of inbox'
```
Expected: Returns your inbox name (e.g., "Inbox")

**Calendar:**
```bash
osascript -e 'tell application "Calendar" to get name of calendars'
```
Expected: Returns list of calendar names

**Reminders:**
```bash
osascript -e 'tell application "Reminders" to get name of lists'
```
Expected: Returns list of reminder list names

### Automated Verification

Run the comprehensive test suite:
```bash
cd tests/framework
./verify_permissions.sh
```

## Next Steps

Once permissions are verified:

1. Proceed to [Skills API Framework Setup](../README.md#skills-api-framework)
2. Review [Usage Guide](USAGE.md) for workflow examples
3. Start testing individual skills in `.claude/skills/`

## Support

If you continue to experience permission issues:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review macOS Console app for detailed error messages
3. Create an issue in the repository with error details

## Version History

- **v1.0** (2025-10-26): Initial permissions setup guide
