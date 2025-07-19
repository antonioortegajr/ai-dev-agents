#!/bin/bash

# AI Dev Agents Startup Script

echo "🤖 AI Dev Agents - Startup Script"
echo "=================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please copy env.example to .env and configure your settings:"
    echo "  cp env.example .env"
    echo "  # Then edit .env with your GitHub token and OpenAI API key"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed or not in PATH"
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    echo "✅ Dependencies installed"
fi

# Function to start MCP server
start_server() {
    echo "🚀 Starting MCP server..."
    python3 main.py server &
    SERVER_PID=$!
    echo "✅ MCP server started with PID: $SERVER_PID"
    
    # Wait a moment for server to start
    sleep 3
    
    # Check if server is running
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ MCP server is responding"
    else
        echo "⚠️  MCP server may not be ready yet, continuing..."
    fi
}

# Function to stop MCP server
stop_server() {
    if [ ! -z "$SERVER_PID" ]; then
        echo "🛑 Stopping MCP server (PID: $SERVER_PID)..."
        kill $SERVER_PID 2>/dev/null
        echo "✅ MCP server stopped"
    fi
}

# Function to run the main application
run_app() {
    echo "🎯 Running AI Dev Agents application..."
    python3 main.py
}

# Handle command line arguments
case "${1:-}" in
    "server")
        start_server
        echo "MCP server is running. Press Ctrl+C to stop."
        trap stop_server EXIT
        wait $SERVER_PID
        ;;
    "app")
        run_app
        ;;
    "both")
        start_server
        echo "Starting application in 5 seconds..."
        sleep 5
        run_app
        stop_server
        ;;
    *)
        echo "Usage: $0 {server|app|both}"
        echo ""
        echo "Commands:"
        echo "  server  - Start only the MCP server"
        echo "  app     - Run only the main application"
        echo "  both    - Start server and run application"
        echo ""
        echo "Examples:"
        echo "  $0 server    # Start MCP server only"
        echo "  $0 app       # Run application (requires server running)"
        echo "  $0 both      # Start server and run app together"
        ;;
esac 