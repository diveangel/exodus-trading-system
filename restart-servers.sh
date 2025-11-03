#!/bin/bash

# Exodus Trading System - Server Restart Script
# This script stops running servers and starts fresh instances

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
echo -e "${BLUE}  Exodus Trading System Server Manager${NC}"
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

    # Wait a moment for ports to be released
    sleep 2

    # Verify port is free
    if lsof -ti:$port > /dev/null 2>&1; then
        echo -e "${RED}✗ Failed to free port $port${NC}"
        return 1
    else
        echo -e "${GREEN}✓ Port $port is now free${NC}"
        return 0
    fi
}

# Function to stop backend server
stop_backend() {
    echo ""
    echo -e "${BLUE}[1/4] Stopping Backend Server...${NC}"

    # Check PID file
    if [ -f "$BACKEND_PID_FILE" ]; then
        local pid=$(cat "$BACKEND_PID_FILE")
        if is_process_running "$pid"; then
            echo -e "${YELLOW}Stopping backend process (PID: $pid)...${NC}"
            kill -15 "$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null || true
            sleep 2
        fi
        rm -f "$BACKEND_PID_FILE"
    fi

    # Kill any process on port 8000
    kill_by_port 8000 "backend"
}

# Function to stop frontend server
stop_frontend() {
    echo ""
    echo -e "${BLUE}[2/4] Stopping Frontend Server...${NC}"

    # Check PID file
    if [ -f "$FRONTEND_PID_FILE" ]; then
        local pid=$(cat "$FRONTEND_PID_FILE")
        if is_process_running "$pid"; then
            echo -e "${YELLOW}Stopping frontend process (PID: $pid)...${NC}"
            kill -15 "$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null || true
            sleep 2
        fi
        rm -f "$FRONTEND_PID_FILE"
    fi

    # Kill any process on ports 3000 and 3001
    kill_by_port 3000 "frontend"
    kill_by_port 3001 "frontend"
}

# Function to start backend server
start_backend() {
    echo ""
    echo -e "${BLUE}[3/4] Starting Backend Server...${NC}"

    cd "$BACKEND_DIR"

    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo -e "${RED}✗ Virtual environment not found!${NC}"
        echo -e "${YELLOW}Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt${NC}"
        exit 1
    fi

    # Start backend server in background
    echo -e "${YELLOW}Starting uvicorn server on port 8000...${NC}"
    source venv/bin/activate
    nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
    local backend_pid=$!
    echo "$backend_pid" > "$BACKEND_PID_FILE"

    # Wait and check if server started successfully
    sleep 3

    if is_process_running "$backend_pid"; then
        echo -e "${GREEN}✓ Backend server started successfully (PID: $backend_pid)${NC}"
        echo -e "${GREEN}  URL: http://localhost:8000${NC}"
        echo -e "${GREEN}  Docs: http://localhost:8000/docs${NC}"
        echo -e "${YELLOW}  Logs: $BACKEND_DIR/backend.log${NC}"
    else
        echo -e "${RED}✗ Failed to start backend server${NC}"
        echo -e "${YELLOW}Check logs: tail -f $BACKEND_DIR/backend.log${NC}"
        exit 1
    fi
}

# Function to start frontend server
start_frontend() {
    echo ""
    echo -e "${BLUE}[4/4] Starting Frontend Server...${NC}"

    cd "$FRONTEND_DIR"

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo -e "${RED}✗ node_modules not found!${NC}"
        echo -e "${YELLOW}Please run: npm install${NC}"
        exit 1
    fi

    # Start frontend server in background
    echo -e "${YELLOW}Starting Next.js dev server...${NC}"
    nohup npm run dev > frontend.log 2>&1 &
    local frontend_pid=$!
    echo "$frontend_pid" > "$FRONTEND_PID_FILE"

    # Wait and check if server started successfully
    sleep 5

    if is_process_running "$frontend_pid"; then
        echo -e "${GREEN}✓ Frontend server started successfully (PID: $frontend_pid)${NC}"
        echo -e "${GREEN}  URL: http://localhost:3001${NC}"
        echo -e "${YELLOW}  Logs: $FRONTEND_DIR/frontend.log${NC}"
    else
        echo -e "${RED}✗ Failed to start frontend server${NC}"
        echo -e "${YELLOW}Check logs: tail -f $FRONTEND_DIR/frontend.log${NC}"
        exit 1
    fi
}

# Main execution
main() {
    # Stop servers
    stop_backend
    stop_frontend

    # Start servers
    start_backend
    start_frontend

    # Summary
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  ✓ All servers started successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${BLUE}Backend:${NC}  http://localhost:8000"
    echo -e "${BLUE}Frontend:${NC} http://localhost:3001"
    echo -e "${BLUE}API Docs:${NC} http://localhost:8000/docs"
    echo ""
    echo -e "${YELLOW}To view logs:${NC}"
    echo -e "  Backend:  tail -f $BACKEND_DIR/backend.log"
    echo -e "  Frontend: tail -f $FRONTEND_DIR/frontend.log"
    echo ""
    echo -e "${YELLOW}To stop servers:${NC}"
    echo -e "  ./stop-servers.sh"
    echo ""
}

# Run main function
main
