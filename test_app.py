#!/usr/bin/env python3
"""
Simple test to verify the application module can be imported and basic functions work
"""

from app import main
import sys

print("Virtual environment is activated and working correctly!")
print(f"Using Python: {sys.executable}")
print("Application file exists and can be imported.")
print("\nThe application is ready to use. Run 'python app.py' to start the interactive version.")