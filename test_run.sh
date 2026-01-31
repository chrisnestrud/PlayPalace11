#!/usr/bin/env bash
# Quick test - runs server for 10 seconds to verify it works

echo "Testing PlayPalace server..."
timeout 10 ./run_server.sh &
SERVER_PID=$!

sleep 3
if ps -p $SERVER_PID > /dev/null; then
    echo "✓ Server started successfully!"
    kill $SERVER_PID 2>/dev/null
    exit 0
else
    echo "✗ Server failed to start"
    exit 1
fi
