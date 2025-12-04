#!/bin/bash
# Note: set -e is not used so we can test all examples even if some fail

# Install dependencies
apt-get update && apt-get install -y --no-install-recommends curl unzip ca-certificates

TEST_COUNT=0
PASSED=0
FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_dir="$2"
    local test_cmd="$3"
    
    TEST_COUNT=$((TEST_COUNT + 1))
    echo ""
    echo "=========================================="
    echo "TEST $TEST_COUNT: $test_name"
    echo "=========================================="
    
    if [ -d "$test_dir" ]; then
        # Copy to temp to avoid writing to read-only image location
        local temp_dir="/tmp/$(basename $test_dir)"
        cp -r "$test_dir" "$temp_dir"
        cd "$temp_dir"
        
        echo "Running: $test_cmd"
        if eval "$test_cmd"; then
            echo "✓ TEST $TEST_COUNT PASSED"
            PASSED=$((PASSED + 1))
        else
            echo "✗ TEST $TEST_COUNT FAILED"
            FAILED=$((FAILED + 1))
        fi
    else
        echo "✗ TEST $TEST_COUNT SKIPPED (directory not found: $test_dir)"
    fi
}

# Test 1: Basic D-Flow FM simulation (downloaded example)
TEST_COUNT=$((TEST_COUNT + 1))
echo ""
echo "=========================================="
echo "TEST $TEST_COUNT: Basic D-Flow FM simulation"
echo "=========================================="
curl -L -o /tmp/delft3dfm-input-example.zip https://storage.googleapis.com/inductiva-api-demo-files/delft3dfm-input-example.zip
unzip -q /tmp/delft3dfm-input-example.zip -d /tmp
cd /tmp/delft3dfm-input-example
if dflowfm --autostartstop f34.mdu; then
    echo "✓ TEST $TEST_COUNT PASSED"
    PASSED=$((PASSED + 1))
else
    echo "✗ TEST $TEST_COUNT FAILED"
    FAILED=$((FAILED + 1))
fi

# Test all dflowfm examples (sequential only)
run_test "D-Flow FM Sequential" \
    "/home/examples/dflowfm/01_dflowfm_sequential" \
    "dimr dimr_config.xml"

run_test "D-Flow FM + D-WAQ Sequential" \
    "/home/examples/dflowfm/03_dflowfm_dwaq_sequential" \
    "dimr dimr_config.xml"

run_test "D-Flow FM + D-WAQ-BLOOM Sequential" \
    "/home/examples/dflowfm/05_dflowfm_dwaq-BLOOM_sequential" \
    "dimr dimr_config.xml"

run_test "D-Waves Standalone" \
    "/home/examples/dflowfm/07_dwaves" \
    "dimr dimr_config.xml"

run_test "D-Flow FM + D-Waves Sequential" \
    "/home/examples/dflowfm/08_dflowfm_sequential_dwaves" \
    "dimr dimr_config.xml"

run_test "D-Flow FM + D-RTC + D-Waves Sequential" \
    "/home/examples/dflowfm/10_dflowfm_sequential_drtc_dwaves" \
    "dimr dimr_config.xml"

# Test delft3d4 examples
# run_test "Standalone D-WAQ (delwaq)" \
#     "/home/examples/delft3d4/06_delwaq" \
#     "delwaq com-tut_fti_waq.inp -p $PROC_DEF_DIR/proc_def.dat"

run_test "Delft3D4 Wave (DIMR)" \
    "/home/examples/delft3d4/07_wave" \
    "dimr dimr_config.xml"

# Note: Some examples need special handling, skipping them

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "Total tests: $TEST_COUNT"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo "=========================================="

if [ $FAILED -eq 0 ]; then
    echo "All tests completed successfully!"
    exit 0
else
    echo "Some tests failed!"
    exit 1
fi
