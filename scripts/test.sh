#!/bin/bash

# Simple test script for VPN detector package (Linux/macOS)

echo "VPN Detector Package Test Script"
echo "================================="

# Change to the project root directory
cd "$(dirname "$0")/.."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed or not in PATH"
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"

# Install the package in development mode
echo ""
echo "Installing package in development mode..."
pip install -e . || {
    echo "❌ Failed to install package"
    exit 1
}

echo "✓ Package installed successfully"

# Run the Python test script
echo ""
echo "Running functional tests..."
python3 scripts/test.py || {
    echo "❌ Functional tests failed"
    exit 1
}

# Run unit tests if pytest is available
echo ""
echo "Running unit tests..."
if command -v pytest &> /dev/null; then
    pytest tests/ -v || {
        echo "❌ Unit tests failed"
        exit 1
    }
    echo "✓ Unit tests passed"
else
    echo "⚠️  pytest not found, skipping unit tests"
    echo "   Install with: pip install pytest"
fi

echo ""
echo "================================="
echo "✓ All tests completed successfully!"