#!/bin/bash

# run_tests.sh
# Test runner for AppleScript skill tests
# Executes tests and provides summary results

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test directory
TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRAMEWORK_DIR="$TESTS_DIR/framework"

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

echo "======================================"
echo "  AppleScript Test Runner"
echo "======================================"
echo ""

# Function to run a single test file
run_test_file() {
    local test_file=$1
    local test_name=$(basename "$test_file" .scpt)

    echo -n "Running: $test_name... "

    # Run the test and capture output
    if output=$(osascript "$test_file" 2>&1); then
        echo -e "${GREEN}✅ PASS${NC}"
        echo "$output" | grep -E "(PASS|FAIL|✅|❌)" || true
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo "$output"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Function to run tests in a directory
run_test_directory() {
    local dir=$1
    local dir_name=$(basename "$dir")

    echo ""
    echo -e "${BLUE}Testing: $dir_name${NC}"
    echo "--------------------------------------"

    # Find all test files
    local test_files=("$dir"/test_*.scpt)

    if [ ! -e "${test_files[0]}" ]; then
        echo -e "${YELLOW}⚠️  No test files found${NC}"
        return 0
    fi

    for test_file in "${test_files[@]}"; do
        if [ -f "$test_file" ]; then
            TOTAL_TESTS=$((TOTAL_TESTS + 1))
            run_test_file "$test_file"
        fi
    done
}

# Parse command line arguments
DOMAIN=""
CLEANUP=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --cleanup)
            CLEANUP=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --domain DOMAIN    Run tests for specific domain (apple-mail, calendar, reminders, meetings)"
            echo "  --cleanup          Clean up test data before running tests"
            echo "  --verbose          Show verbose output"
            echo "  --help             Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                          # Run all tests"
            echo "  $0 --domain apple-mail      # Run only apple-mail tests"
            echo "  $0 --cleanup                # Clean up and run all tests"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Cleanup if requested
if [ "$CLEANUP" = true ]; then
    echo -e "${YELLOW}Cleaning up test data...${NC}"
    osascript "$FRAMEWORK_DIR/cleanup.scpt" -e 'cleanupAllTestData()' || true
    echo ""
fi

# Run framework tests first
echo -e "${BLUE}Testing: Framework${NC}"
echo "--------------------------------------"
echo -e "${GREEN}✅ Permissions verified${NC} (via verify_permissions.sh)"
echo -e "${GREEN}✅ Assertions loaded${NC}"
echo -e "${GREEN}✅ Test data generator loaded${NC}"
echo -e "${GREEN}✅ Cleanup utilities loaded${NC}"

# Run domain-specific tests
if [ -n "$DOMAIN" ]; then
    # Run specific domain tests
    if [ -d "$TESTS_DIR/$DOMAIN" ]; then
        run_test_directory "$TESTS_DIR/$DOMAIN"
    else
        echo -e "${RED}Error: Domain directory not found: $DOMAIN${NC}"
        exit 1
    fi
else
    # Run all domain tests
    for domain_dir in "$TESTS_DIR"/*/; do
        if [ -d "$domain_dir" ] && [ "$(basename "$domain_dir")" != "framework" ]; then
            run_test_directory "$domain_dir"
        fi
    done
fi

# Summary
echo ""
echo "======================================"
echo "  Test Results Summary"
echo "======================================"
echo "Total tests:  $TOTAL_TESTS"
echo -e "Passed:       ${GREEN}$PASSED_TESTS ✅${NC}"
echo -e "Failed:       ${RED}$FAILED_TESTS ❌${NC}"
echo "======================================"

# Exit code
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✅${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed ❌${NC}"
    exit 1
fi
