#!/usr/bin/env python3
"""
Test script for the Image Selector API
Usage: python test_api.py "your search keyword"
"""

import requests
import json
import sys

def test_api(keyword):
    """Test the image selector API with a given keyword."""
    url = 'http://localhost:5000/api/select-image'
    data = {'keyword': keyword}
    
    try:
        response = requests.post(url, json=data, timeout=60)
        result = response.json()
        
        print(f"Keyword: {keyword}")
        print(f"Status: {'Success' if result.get('success') else 'Failed'}")
        
        if result.get('success'):
            print(f"Image URL: {result.get('image_url')}")
        else:
            print(f"Error: {result.get('error')}")
            
        return result
        
    except Exception as e:
        print(f"Error testing API: {e}")
        return None

if __name__ == '__main__':
    # Use command line argument or default
    keyword = sys.argv[1] if len(sys.argv) > 1 else "Ormond Beach oceanfront house"
    test_api(keyword)