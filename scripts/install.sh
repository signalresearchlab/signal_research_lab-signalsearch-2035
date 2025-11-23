#!/bin/bash

echo "📡 Installing RF Signal Detector..."
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo "🔄 Creating virtual environment..."
python3 -m venv rf_detector_venv

# Activate virtual environment
echo "📦 Activating virtual environment..."
source rf_detector_venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install package
echo "🚀 Installing RF Signal Detector..."
pip install -e .

# Make script executable
chmod +x rf_detector_venv/bin/rf-detector

echo ""
echo "🎉 Installation complete!"
echo "======================================"
echo "To use the RF Signal Detector:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source rf_detector_venv/bin/activate"
echo ""
echo "2. Run the detector:"
echo "   rf-detector scan --help"
echo ""
echo "3. Example commands:"
echo "   rf-detector scan -b 2.4G -t 30"
echo "   rf-detector monitor -c 6 -t 60"
echo "   rf-detector analyze -f results.json -p"
echo ""
echo "For development:"
echo "   pip install -e .[dev]"
