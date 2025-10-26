#!/bin/bash

# verify_permissions.sh
# Verifies macOS automation permissions for Mail, Calendar, and Reminders

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================"
echo "  macOS Permissions Verification"
echo "======================================"
echo ""

# Track overall status
ALL_PASSED=true

# Test Apple Mail Access
echo -n "Testing Apple Mail access... "
MAIL_RESULT=$(osascript -e 'tell application "Mail" to get name of inbox' 2>&1)
MAIL_EXIT_CODE=$?

if [ $MAIL_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "   Inbox name: $MAIL_RESULT"
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   Error: $MAIL_RESULT"
    echo "   → Check System Settings → Privacy & Security → Automation"
    ALL_PASSED=false
fi
echo ""

# Test Calendar Access
echo -n "Testing Calendar access... "
CALENDAR_RESULT=$(osascript -e 'tell application "Calendar" to get name of calendars' 2>&1)
CALENDAR_EXIT_CODE=$?

if [ $CALENDAR_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "   Calendars found: $CALENDAR_RESULT"
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   Error: $CALENDAR_RESULT"
    echo "   → Check System Settings → Privacy & Security → Automation"
    ALL_PASSED=false
fi
echo ""

# Test Reminders Access
echo -n "Testing Reminders access... "
REMINDERS_RESULT=$(osascript -e 'tell application "Reminders" to get name of lists' 2>&1)
REMINDERS_EXIT_CODE=$?

if [ $REMINDERS_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "   Reminder lists found: $REMINDERS_RESULT"
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "   Error: $REMINDERS_RESULT"
    echo "   → Check System Settings → Privacy & Security → Automation"
    ALL_PASSED=false
fi
echo ""

# Test Timezone
echo -n "Checking system timezone... "
TIMEZONE=$(sudo systemsetup -gettimezone 2>/dev/null | sed 's/Time Zone: //')

if [ -z "$TIMEZONE" ]; then
    # Fallback if systemsetup requires sudo and fails
    TIMEZONE=$(date +%Z)
    echo -e "${YELLOW}⚠️  WARNING${NC}"
    echo "   Could not read timezone with systemsetup (may require sudo)"
    echo "   Current timezone appears to be: $TIMEZONE"
else
    echo -e "${GREEN}✅ INFO${NC}"
    echo "   System timezone: $TIMEZONE"

    if [ "$TIMEZONE" != "America/Costa_Rica" ]; then
        echo -e "${YELLOW}   ⚠️  Note: Expected timezone is America/Costa_Rica${NC}"
        echo "   To change: sudo systemsetup -settimezone America/Costa_Rica"
    fi
fi
echo ""

# Summary
echo "======================================"
if [ "$ALL_PASSED" = true ]; then
    echo -e "${GREEN}✅ All permissions verified successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review skills in .claude/skills/"
    echo "  2. Run individual skill tests"
    echo "  3. Start using the productivity agent"
    exit 0
else
    echo -e "${RED}❌ Some permissions are missing${NC}"
    echo ""
    echo "Required actions:"
    echo "  1. Open System Settings → Privacy & Security → Automation"
    echo "  2. Enable permissions for Terminal or Claude app:"
    echo "     - Mail"
    echo "     - Calendar"
    echo "     - Reminders"
    echo "  3. Re-run this script to verify"
    echo ""
    echo "For detailed setup instructions, see:"
    echo "  docs/PERMISSIONS.md"
    exit 1
fi
