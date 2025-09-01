#!/usr/bin/env python3
"""Test script to verify environment variables are loading correctly"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test if variables are loaded
wordsapi_key = os.getenv('WORDSAPI_KEY')
debug_mode = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

print("Environment Variables Test")
print("=" * 30)
print(f"WORDSAPI_KEY loaded: {'Yes' if wordsapi_key else 'No'}")
print(f"DEBUG_MODE: {debug_mode}")

if wordsapi_key and wordsapi_key != '5bbff71087msh7c7adca1f3ce410p1db26bjsnc9c3d7c46794':
    print("✅ WORDSAPI_KEY is properly set!")
else:
    print("❌ Please set WORDSAPI_KEY in your .env file")
    print("Get it from: https://rapidapi.com/dpventures/api/wordsapi/")