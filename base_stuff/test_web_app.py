#!/usr/bin/env python3
"""
Web application test script for the Hugging Face Model Security Scanner
"""

import sys
import os
import json

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import patch, MagicMock
from web_app import app

def test_web_app_routes():
    """Test the web application routes"""
    print("Testing web application routes...")

    # Create a test client
    app.config['TESTING'] = True
    client = app.test_client()

    # Test the main route
    print("1. Testing main route (/)...")
    try:
        response = client.get('/')
        print(f"   Status code: {response.status_code}")
        print(f"   Success: Main route accessible")
    except Exception as e:
        print(f"   Error: {e}")

    # Test the scan_specific route with empty data
    print("2. Testing scan_specific route with empty data...")
    try:
        response = client.post('/scan_specific', data={})
        print(f"   Status code: {response.status_code}")
        data = json.loads(response.data.decode())
        print(f"   Response: {data}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test the scan_by_criteria route with minimal data
    print("3. Testing scan_by_criteria route with minimal data...")
    try:
        response = client.post('/scan_by_criteria', data={'tag': 'text-classification', 'author': 'google'})
        print(f"   Status code: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.data.decode())
            print(f"   Response: Received {data.get('models_scanned', 0)} results")
        else:
            print(f"   Response: {response.data.decode()}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test the scan_by_criteria route with extended parameters
    print("4. Testing scan_by_criteria route with extended parameters...")
    try:
        response = client.post('/scan_by_criteria', data={
            'tag': 'text-classification',
            'author': 'google',
            'library': 'transformers',
            'sort': 'downloads',
            'direction': 'desc',
            'limit': '2'
        })
        print(f"   Status code: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.data.decode())
            print(f"   Response: Received {data.get('models_scanned', 0)} results")
        else:
            print(f"   Response: {response.data.decode()}")
    except Exception as e:
        print(f"   Error: {e}")

    print("Web application tests completed.")

if __name__ == "__main__":
    test_web_app_routes()