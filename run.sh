#!/bin/bash

# ================================
# Real-City Path Visualizer Runner
# ================================

# Colors
GREEN="\033[0;32m"
NC="\033[0m"

echo -e "${GREEN}Starting Real-City Path Visualizer...${NC}"

# ----------------------------
# Cleanup on exit
# ----------------------------
cleanup() {
    echo -e "\n${GREEN}Shutting down...${NC}"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}
trap cleanup INT TERM

# ----------------------------
# Check backend dependencies
# ----------------------------
echo -e "${GREEN}[CHECK] Python backend dependencies${NC}"
if ! command -v python3 &> /dev/null; then
    echo "Python3 not installed. Install it first."
    exit 1
fi

if ! python3 -c "import fastapi, uvicorn, osmnx, networkx, geopy" 2>/dev/null; then
    echo "Missing Python dependencies. Installing..."
    pip install fastapi uvicorn osmnx networkx geopy
fi

# ----------------------------
# Check frontend dependencies
# ----------------------------
echo -e "${GREEN}[CHECK] Frontend dependencies${NC}"
if [ ! -d "./frontend/node_modules" ]; then
    echo "Installing frontend packages..."
    cd frontend || exit
    npm install
    cd ..
fi

# ----------------------------
# Start backend
# ----------------------------
echo -e "${GREEN}[START] Backend (FastAPI)${NC}"
cd backend || exit
uvicorn main:app --reload --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# ----------------------------
# Start frontend
# ----------------------------
echo -e "${GREEN}[START] Frontend (React + Vite)${NC}"
cd frontend || exit
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# ----------------------------
# Wait for processes to exit
# ----------------------------
wait $BACKEND_PID
wait $FRONTEND_PID
