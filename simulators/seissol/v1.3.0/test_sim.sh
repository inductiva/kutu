#!/bin/bash
set -euo pipefail

# Function to check if a port is in use
check_port() {
    local port=$1
    if command -v ss >/dev/null 2>&1; then
        ss -tuln | grep -q ":${port}"
    elif command -v netstat >/dev/null 2>&1; then
        netstat -tuln | grep -q ":${port}"
    elif command -v lsof >/dev/null 2>&1; then
        lsof -i ":${port}" >/dev/null 2>&1
    else
        echo "No suitable command found to check ports (ss, netstat, or lsof). Installing netstat..."
        apt-get update && apt-get install -y net-tools
        netstat -tuln | grep -q ":${port}"
    fi
}

# Start Jupyter Lab in the background
echo "Starting Jupyter Lab..."
jupyter lab --ip=0.0.0.0 --port=53155 --no-browser --allow-root &
JUPYTER_PID=$!

# Wait for Jupyter Lab to start
echo "Waiting for Jupyter Lab to confirm startup..."
for i in {1..30}; do
    if check_port 53155; then
        echo "Jupyter Lab is running on port 53155."
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Jupyter Lab failed to start within the timeout period."
        kill $JUPYTER_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Proceed to the next job
echo "Jupyter Lab confirmed. Proceeding to the next job."

# Kill the Jupyter Lab process once confirmed running
echo "Killing Jupyter Lab process..."
kill $JUPYTER_PID 2>/dev/null || true

# Wait for process to terminate with timeout
for i in {1..10}; do
    if ! ps -p $JUPYTER_PID >/dev/null 2>&1; then
        echo "Jupyter Lab process terminated successfully."
        exit 0
    fi
    if [ $i -eq 10 ]; then
        echo "Force killing Jupyter Lab process..."
        kill -9 $JUPYTER_PID 2>/dev/null || true
    fi
    sleep 1
done

# Final check
if ps -p $JUPYTER_PID >/dev/null 2>&1; then
    echo "Failed to terminate Jupyter Lab process."
    exit 1
else
    echo "Test done."
    exit 0
fi