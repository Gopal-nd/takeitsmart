#!/bin/bash

# Visual styling
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================================${NC}"
echo -e "${CYAN}        🚀 AI SOFTWARE TEAM PLATFORM INITIALIZER        ${NC}"
echo -e "${CYAN}========================================================${NC}"

# Check for .env file
if [ ! -f .env ]; then
    echo -e "${YELLOW}[!] Warning: .env file is missing! Make sure to set AWS Bedrock keys.${NC}"
fi

# Clean exit handler
cleanup() {
    echo -e "\n${YELLOW}[!] Shutting down services cleanly...${NC}"
    # Kill background backend process
    if [ ! -z "$BACKEND_PID" ]; then
        echo -e "${slate}[-] Stopping FastAPI backend (PID: $BACKEND_PID)...${NC}"
        kill $BACKEND_PID 2>/dev/null
    fi
    echo -e "${GREEN}[✓] Cleanup successful. Goodbye!${NC}"
    exit 0
}

# Trap Ctrl+C (SIGINT) and SIGTERM
trap cleanup SIGINT SIGTERM

# Start FastAPI Backend
echo -e "${CYAN}[1/2] Launching stateful FastAPI backend server...${NC}"
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend database setup to initiate
sleep 2.5

# Check if backend successfully started
if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}[✓] FastAPI running in background on http://localhost:8000 (PID: $BACKEND_PID)${NC}"
    echo -e "${CYAN}    Logs are written to 'backend.log'${NC}"
else
    echo -e "${RED}[✗] Failed to launch backend. Check your poetry environment or credentials!${NC}"
    exit 1
fi

# Start React Frontend
echo -e "${CYAN}[2/2] Launching React Dev Server with Tailwind CSS...${NC}"
if [ -d frontend ]; then
    cd frontend
    # Start npm run dev
    npm run dev
else
    echo -e "${RED}[✗] Folder 'frontend' not found! Make sure you are in the repository root.${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
