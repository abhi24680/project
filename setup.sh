#!/bin/bash

# Smart Energy Saver Setup Script
echo "🔧 Setting up Smart Energy Saver System..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv energy_saver_env

# Activate virtual environment
source energy_saver_env/bin/activate

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📋 Installing dependencies..."
pip install -r requirements.txt

# Check if camera is available
echo "📷 Checking camera availability..."
python3 -c "
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print('✅ Camera 0 is available')
    cap.release()
else:
    print('⚠️  Camera 0 is not available. Please check your camera connection.')
"

# Make the main script executable
chmod +x smart_energy_saver.py

echo "🎉 Setup completed successfully!"
echo ""
echo "To run the Smart Energy Saver system:"
echo "1. Activate the virtual environment: source energy_saver_env/bin/activate"
echo "2. Run the system: python3 smart_energy_saver.py"
echo ""
echo "For help with command line options: python3 smart_energy_saver.py --help"