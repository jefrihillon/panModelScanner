#!/usr/bin/env python3
"""
Test script for the Hugging Face Model Security Scanner
"""

import sys
import os
from unittest.mock import patch, MagicMock

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scan_hf_models import scan_models_by_criteria

def test_scan_models_by_criteria_with_various_parameters():
    """Test the scan_models_by_criteria function with different parameter combinations"""
    print("Testing scan_models_by_criteria function...")

    # Test with minimal parameters
    print("1. Testing with minimal parameters...")
    try:
        results = scan_models_by_criteria(limit=2)
        print(f"   Success: Returned {len(results)} results")
    except Exception as e:
        print(f"   Error: {e}")

    # Test with task type
    print("2. Testing with task type parameter...")
    try:
        results = scan_models_by_criteria(tag="text-classification", limit=2)
        print(f"   Success: Returned {len(results)} results")
    except Exception as e:
        print(f"   Error: {e}")

    # Test with author
    print("3. Testing with author parameter...")
    try:
        results = scan_models_by_criteria(author="google", limit=2)
        print(f"   Success: Returned {len(results)} results")
    except Exception as e:
        print(f"   Error: {e}")

    # Test with multiple parameters
    print("4. Testing with multiple parameters...")
    try:
        results = scan_models_by_criteria(
            tag="text-classification",
            author="google",
            limit=2
        )
        print(f"   Success: Returned {len(results)} results")
    except Exception as e:
        print(f"   Error: {e}")

    print("Tests completed.")

if __name__ == "__main__":
    test_scan_models_by_criteria_with_various_parameters()