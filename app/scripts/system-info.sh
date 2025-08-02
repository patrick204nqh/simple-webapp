#!/bin/bash

echo "=== System Information ==="
echo ""
echo "Hostname: $(hostname)"
echo "Date: $(date)"
echo ""

echo "=== Network Interfaces ==="
ip -4 addr show | grep -E "^[0-9]+:|inet"
echo ""

echo "=== Active Connections ==="
ss -tuln | head -20
echo ""

echo "=== System Resources ==="
echo "CPU: $(grep -c processor /proc/cpuinfo) cores"
free -h | grep -E "^Mem:|^Swap:"
df -h | grep -E "^/dev/|^Filesystem"
echo ""

echo "=== Running Services ==="
ps aux | grep -E "(docker|glances|python)" | grep -v grep