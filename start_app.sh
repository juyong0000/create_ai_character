#!/bin/bash

# Function to kill processes on exit
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID
    exit
}

# Trap Ctrl+C
trap cleanup SIGINT

# Start Backend
echo "🚀 Starting Backend (FastAPI)..."
source venv/bin/activate
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to initialize
sleep 2

# Start Frontend
echo "✨ Starting Frontend (Next.js)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "------------------------------------------------"
echo "✅ App is running!"
echo "🌍 Frontend: http://localhost:3000"
echo "🔌 Backend:  http://localhost:8000"
echo "------------------------------------------------"
echo "Press Ctrl+C to stop."

wait
