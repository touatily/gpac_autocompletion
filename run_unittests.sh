#!/bin/bash

# Directory containing the unit tests
TEST_DIR="./unittests"

# Check if the test directory exists
if [ ! -d "$TEST_DIR" ]; then
    echo "Test directory $TEST_DIR does not exist."
    exit 1
fi

# delete cache file
rm -f ~/.cache/gpac/gpac_autocomplete.json

# Run the unit tests
echo "Running unit tests..."
python3 -m unittest discover -s "$TEST_DIR" -p "*_test.py"

if [ $? -ne 0 ]; then
    echo "Some tests failed."
    exit 1
fi

echo "All tests passed successfully."
