#!/usr/bin/env python3
"""
Quick start script for RF Signal Detector
Run with: python run.py
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from rf_detector.cli import main
    print("✓ RF Signal Detector loaded successfully!")
    print("✓ Starting scan...\n")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're in the correct directory and all files are in place.")
    sys.exit(1)

if __name__ == '__main__':
    main()
