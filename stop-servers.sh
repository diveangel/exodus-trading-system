#!/bin/bash

# Exodus Trading System - Server Stop Script
# This script stops all running servers

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# PID file locations
BACKEND_PID_FILE="$BACKEND_DIR/.backend.pid"
FRONTEND_PID_FILE="$FRONTEND_DIR/.frontend.pid"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Stopping Exodus Trading System${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to check if a process is running
is_process_running() {
    local pid=$1
    if [ -z "$pid" ]; then
        return 1
    fi
    if ps -p "$pid" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to kill process by port
kill_by_port() {
    local port=$1
    local service_name=$2

    echo -e "${YELLOW}Checking for processes on port $port...${NC}"

    # Find PIDs using the port
    local pids=$(lsof -ti:$port 2>/dev/null)

    if [ -z "$pids" ]; then
        echo -e "${GREEN}✓ No process running on port $port${NC}"
        return 0
    fi

    echo -e "${YELLOW}Found process(es) on port $port: $pids${NC}"
    echo -e "${YELLOW}Killing $service_name processes...${NC}"

    # Kill each PID
    for pid in $pids; do
        kill -9 "$pid" 2>/dev/null || true
        echo -e "${GREEN}✓ Killed process $pid${NC}"
    done

    sleep 1
    echo -e "${GREEN}✓ Stopped $service_name${NC}"
}

# Stop backend server
echo -e "${BLUE}[1/2] Stopping Backend Server...${NC}"
if [ -f "$BACKEND_PID_FILE" ]; then
    local pid=$(cat "$BACKEND_PID_FILE")
    if is_process_running "$pid"; then
        echo -e "${YELLOW}Stopping backend process (PID: $pid)...${NC}"
        kill -15 "$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null || true
        sleep 2
    fi
    rm -f "$BACKEND_PID_FILE"
fi
kill_by_port 8000 "backend"

# Stop frontend server
echo ""
echo -e "${BLUE}[2/2] Stopping Frontend Server...${NC}"
if [ -f "$FRONTEND_PID_FILE" ]; then
    local pid=$(cat "$FRONTEND_PID_FILE")
    if is_process_running "$pid"; then
        echo -e "${YELLOW}Stopping frontend process (PID: $pid)...${NC}"
        kill -15 "$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null || true
        sleep 2
    fi
    rm -f "$FRONTEND_PID_FILE"
fi
kill_by_port 3000 "frontend"
kill_by_port 3001 "frontend"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✓ All servers stopped successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
