#!/bin/bash

# TACTIK AI MVP - Startup Script

echo "════════════════════════════════════════════════════════════════"
echo "  TACTIK AI 5.3 Premium - MVP Startup"
echo "  Strategic Intelligence with Scientific Validation"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "✓ Python version: $python_version"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠ No .env file found. Creating from template..."
    cp .env.example .env
    echo "⚠ Please edit .env and add your OPENAI_API_KEY or ANTHROPIC_API_KEY"
    echo ""
    read -p "Press Enter after configuring .env file..."
fi

# Create directories
echo "✓ Creating directories..."
mkdir -p data
mkdir -p reports
mkdir -p static

# Install dependencies
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  Starting TACTIK AI MVP"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "  Web Interface: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop"
echo ""

# Start the server
python api.py
