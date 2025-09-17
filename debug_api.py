#!/usr/bin/env python3
"""
Debug script to test SerpApi connection and find working parameters
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

def test_api_connection():
    """Test basic API connection"""
    api_key = os.getenv('SERPAPI_KEY')
    
    # Try a simple search first
    params = {
        'engine': 'google_flights',
        'departure_id': 'TLV',
        'arrival_id': 'CDG',
        'outbound_date': '2024-12-15',  # Try closer date
        'return_date': '2024-12-20',
        'currency': 'USD',
        'type': '1',
        'adults': '1',
        'api_key': api_key
    }
    
    print("Testing API connection...")
    print(f"URL: https://serpapi.com/search")
    print(f"Parameters: {params}")
    print()
    
    try:
        response = requests.get('https://serpapi.com/search', params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS! API working correctly.")
            print(f"Search ID: {data.get('search_metadata', {}).get('id', 'N/A')}")
            
            # Check if we got flight results
            best_flights = data.get('best_flights', [])
            other_flights = data.get('other_flights', [])
            total_flights = len(best_flights) + len(other_flights)
            print(f"Found {total_flights} flights")
            
            if total_flights > 0:
                print("\\nSample flight:")
                sample_flight = best_flights[0] if best_flights else other_flights[0]
                print(f"  Price: ${sample_flight.get('price', 'N/A')}")
                print(f"  Duration: {sample_flight.get('total_duration', 0)} minutes")
            
        else:
            print(f"ERROR: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error text: {response.text[:500]}")
                
    except Exception as e:
        print(f"Exception: {e}")

def test_different_dates():
    """Test with different date ranges"""
    api_key = os.getenv('SERPAPI_KEY')
    
    # Test dates - try current year first
    test_dates = [
        ('2024-11-15', '2024-11-20'),  # November 2024
        ('2024-12-15', '2024-12-20'),  # December 2024
        ('2025-02-15', '2025-02-20'),  # February 2025
        ('2025-05-15', '2025-05-20'),  # May 2025 (original)
    ]
    
    for outbound, return_date in test_dates:
        print(f"\\nTesting dates: {outbound} to {return_date}")
        
        params = {
            'engine': 'google_flights',
            'departure_id': 'TLV',
            'arrival_id': 'CDG',
            'outbound_date': outbound,
            'return_date': return_date,
            'currency': 'USD',
            'type': '1',
            'adults': '1',
            'api_key': api_key
        }
        
        try:
            response = requests.get('https://serpapi.com/search', params=params, timeout=20)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                flights = len(data.get('best_flights', [])) + len(data.get('other_flights', []))
                print(f"  ✓ Success! Found {flights} flights")
                return outbound, return_date  # Return working dates
            else:
                try:
                    error_data = response.json()
                    print(f"  ✗ Error: {error_data.get('error', response.text[:100])}")
                except:
                    print(f"  ✗ Error: {response.status_code} - {response.text[:100]}")
                    
        except Exception as e:
            print(f"  ✗ Exception: {e}")
    
    return None, None

if __name__ == "__main__":
    print("SerpApi Google Flights API Debug Tool")
    print("="*50)
    
    # Check API key
    if not os.getenv('SERPAPI_KEY'):
        print("ERROR: No API key found!")
        exit(1)
    
    print("Step 1: Testing basic API connection...")
    test_api_connection()
    
    print("\\n" + "="*50)
    print("Step 2: Testing different date ranges...")
    working_dates = test_different_dates()
    
    if working_dates[0]:
        print(f"\\n✓ Working dates found: {working_dates[0]} to {working_dates[1]}")
        print("You can use these dates in the main script!")
    else:
        print("\\n✗ No working dates found. Check API key or try different parameters.")
