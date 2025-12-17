#!/bin/bash
# ==============================================================================
# Task 6: Automated Test Runner Script
# ==============================================================================
# This script automates the execution of the test suite for the 
# Quantium Soul Foods Dashboard application.
#
# Usage: ./run_tests.sh
#
# Exit Codes:
#   0 - All tests passed successfully
#   1 - One or more tests failed or an error occurred
# ==============================================================================

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR" || exit 1

echo "=========================================="
echo "   Quantium Test Suite Runner"
echo "=========================================="
echo ""

# Step 1: Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found."
    echo "   Please create a virtual environment first:"
    echo "   python3 -m venv venv"
    exit 1
fi

echo "📁 Project directory: $SCRIPT_DIR"
echo ""

# Step 2: Activate the virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to activate virtual environment."
    exit 1
fi

echo "✅ Virtual environment activated"
echo ""

# Step 3: Execute the test suite using pytest
echo "🧪 Running test suite with pytest..."
echo "------------------------------------------"
echo ""

python -m pytest test_app.py -v

# Capture the exit code from pytest
TEST_EXIT_CODE=$?

echo ""
echo "------------------------------------------"

# Step 4: Return appropriate exit code
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed successfully!"
    echo "=========================================="
    exit 0
else
    echo "❌ Some tests failed."
    echo "=========================================="
    exit 1
fi
