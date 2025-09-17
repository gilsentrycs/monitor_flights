#!/usr/bin/env python3
"""
Flight Search Demo Script

This script demonstrates how the Google Flights API works using SerpApi
with example data, showing the expected output format.

This demo shows the structure and functionality without requiring an API key.
"""

import json
from datetime import datetime

def demo_flight_search():
    """Demonstrate flight search with mock data"""
    
    print("Tel Aviv to Paris Flight Search - DEMO MODE")
    print("="*60)
    print("This demo shows how the script works with example data")
    print("For real searches, get a SerpApi key from https://serpapi.com/")
    print()
    
    # Mock API response data (based on real SerpApi structure)
    mock_response = {
        "search_metadata": {
            "id": "demo_search_123456",
            "status": "Success",
            "created_at": "2025-09-17 10:30:00 UTC",
            "total_time_taken": 1.2
        },
        "search_parameters": {
            "engine": "google_flights",
            "departure_id": "TLV",
            "arrival_id": "CDG,ORY",
            "outbound_date": "2025-05-15",
            "return_date": "2025-05-20",
            "currency": "USD",
            "type": "1"
        },
        "price_insights": {
            "lowest_price": 485,
            "price_level": "typical",
            "typical_price_range": [420, 650]
        },
        "best_flights": [
            {
                "flights": [
                    {
                        "departure_airport": {
                            "name": "Ben Gurion Airport",
                            "id": "TLV",
                            "time": "2025-05-15 14:30"
                        },
                        "arrival_airport": {
                            "name": "Paris Charles de Gaulle Airport",
                            "id": "CDG",
                            "time": "2025-05-15 19:55"
                        },
                        "duration": 325,
                        "airplane": "Airbus A330",
                        "airline": "Air France",
                        "flight_number": "AF 2042",
                        "travel_class": "Economy"
                    }
                ],
                "total_duration": 325,
                "price": 485,
                "type": "Round trip",
                "carbon_emissions": {
                    "this_flight": 890000,
                    "typical_for_this_route": 850000,
                    "difference_percent": 5
                }
            },
            {
                "flights": [
                    {
                        "departure_airport": {
                            "name": "Ben Gurion Airport",
                            "id": "TLV",
                            "time": "2025-05-15 09:15"
                        },
                        "arrival_airport": {
                            "name": "Istanbul Airport",
                            "id": "IST",
                            "time": "2025-05-15 12:45"
                        },
                        "duration": 210,
                        "airplane": "Boeing 737",
                        "airline": "Turkish Airlines",
                        "flight_number": "TK 1596"
                    },
                    {
                        "departure_airport": {
                            "name": "Istanbul Airport",
                            "id": "IST",
                            "time": "2025-05-15 15:20"
                        },
                        "arrival_airport": {
                            "name": "Paris Charles de Gaulle Airport",
                            "id": "CDG",
                            "time": "2025-05-15 18:15"
                        },
                        "duration": 235,
                        "airplane": "Airbus A321",
                        "airline": "Turkish Airlines",
                        "flight_number": "TK 1827"
                    }
                ],
                "layovers": [
                    {
                        "duration": 155,
                        "name": "Istanbul Airport",
                        "id": "IST",
                        "overnight": False
                    }
                ],
                "total_duration": 600,
                "price": 520,
                "type": "Round trip",
                "carbon_emissions": {
                    "this_flight": 920000,
                    "typical_for_this_route": 850000,
                    "difference_percent": 8
                }
            },
            {
                "flights": [
                    {
                        "departure_airport": {
                            "name": "Ben Gurion Airport",
                            "id": "TLV",
                            "time": "2025-05-15 23:55"
                        },
                        "arrival_airport": {
                            "name": "Frankfurt Airport",
                            "id": "FRA",
                            "time": "2025-05-16 04:20"
                        },
                        "duration": 265,
                        "airplane": "Boeing 787",
                        "airline": "Lufthansa",
                        "flight_number": "LH 687",
                        "overnight": True
                    },
                    {
                        "departure_airport": {
                            "name": "Frankfurt Airport",
                            "id": "FRA", 
                            "time": "2025-05-16 07:40"
                        },
                        "arrival_airport": {
                            "name": "Paris Charles de Gaulle Airport",
                            "id": "CDG",
                            "time": "2025-05-16 09:05"
                        },
                        "duration": 85,
                        "airplane": "Airbus A319",
                        "airline": "Lufthansa",
                        "flight_number": "LH 1040"
                    }
                ],
                "layovers": [
                    {
                        "duration": 200,
                        "name": "Frankfurt Airport",
                        "id": "FRA",
                        "overnight": True
                    }
                ],
                "total_duration": 550,
                "price": 575,
                "type": "Round trip",
                "carbon_emissions": {
                    "this_flight": 780000,
                    "typical_for_this_route": 850000,
                    "difference_percent": -8
                }
            }
        ],
        "airports": [
            {
                "departure": [
                    {
                        "airport": {
                            "name": "Ben Gurion Airport",
                            "id": "TLV"
                        },
                        "city": "Tel Aviv",
                        "country": "Israel",
                        "country_code": "IL"
                    }
                ],
                "arrival": [
                    {
                        "airport": {
                            "name": "Paris Charles de Gaulle Airport",
                            "id": "CDG"
                        },
                        "city": "Paris",
                        "country": "France",
                        "country_code": "FR"
                    },
                    {
                        "airport": {
                            "name": "Paris Orly Airport",
                            "id": "ORY"
                        },
                        "city": "Paris",
                        "country": "France",
                        "country_code": "FR"
                    }
                ]
            }
        ]
    }
    
    # Import and use the FlightSearcher display method
    # We'll recreate the display logic here for the demo
    display_demo_results(mock_response)
    
    # Show API structure
    print("\\n" + "="*80)
    print("API STRUCTURE EXAMPLE")
    print("="*80)
    print("This is how the actual SerpApi response looks:")
    print(json.dumps(mock_response, indent=2)[:800] + "\\n... (truncated)")
    
    print("\\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("1. Get a free SerpApi account: https://serpapi.com/users/sign_up")
    print("2. Get your API key: https://serpapi.com/manage-api-key")
    print("3. Copy .env.example to .env and add your key")
    print("4. Run: python tel_aviv_paris_flights.py")
    print("\\nFree accounts get 100 searches per month!")

def display_demo_results(response_data):
    """Display formatted demo results"""
    
    search_meta = response_data.get('search_metadata', {})
    search_params = response_data.get('search_parameters', {})
    
    print("\\n" + "="*80)
    print("GOOGLE FLIGHTS SEARCH RESULTS - DEMO")
    print("="*80)
    print(f"Search ID: {search_meta.get('id', 'N/A')}")
    print(f"Status: {search_meta.get('status', 'N/A')}")
    print(f"Route: {search_params.get('departure_id', 'N/A')} → {search_params.get('arrival_id', 'N/A')}")
    print(f"Dates: {search_params.get('outbound_date', 'N/A')} to {search_params.get('return_date', 'N/A')}")
    print(f"Currency: {search_params.get('currency', 'N/A')}")
    
    # Display price insights
    if 'price_insights' in response_data:
        insights = response_data['price_insights']
        lowest_price = insights.get('lowest_price', 'N/A')
        price_level = insights.get('price_level', 'N/A')
        typical_range = insights.get('typical_price_range', [])
        
        print(f"\\nPRICE INSIGHTS:")
        print(f"  Lowest Price: ${lowest_price}")
        print(f"  Price Level: {price_level.title()}")
        if typical_range and len(typical_range) >= 2:
            print(f"  Typical Range: ${typical_range[0]} - ${typical_range[1]}")
    
    # Display flights
    best_flights = response_data.get('best_flights', [])
    if best_flights:
        print(f"\\nBEST FLIGHTS ({len(best_flights)} found):")
        print("-" * 80)
        for i, flight in enumerate(best_flights, 1):
            price = flight.get('price', 'N/A')
            total_duration = flight.get('total_duration', 0)
            
            # Convert duration
            hours = total_duration // 60
            minutes = total_duration % 60
            duration_str = f"{hours}h {minutes}m"
            
            # Carbon info
            carbon_info = ""
            if 'carbon_emissions' in flight:
                carbon = flight['carbon_emissions']
                this_flight_kg = carbon.get('this_flight', 0) / 1000
                diff_percent = carbon.get('difference_percent', 0)
                carbon_info = f" | Carbon: {this_flight_kg:.1f}kg ({diff_percent:+d}%)"
            
            print(f"{i}. ${price} USD | Duration: {duration_str}{carbon_info}")
            
            # Show flight segments
            if 'flights' in flight:
                for j, segment in enumerate(flight['flights']):
                    dep = segment.get('departure_airport', {})
                    arr = segment.get('arrival_airport', {})
                    airline = segment.get('airline', 'Unknown')
                    flight_num = segment.get('flight_number', 'N/A')
                    
                    print(f"   Segment {j+1}: {dep.get('id', 'N/A')} → {arr.get('id', 'N/A')} | "
                          f"{airline} {flight_num} | {dep.get('time', 'N/A')} → {arr.get('time', 'N/A')}")
            
            # Show layovers
            if 'layovers' in flight:
                for layover in flight['layovers']:
                    duration = layover.get('duration', 0)
                    airport = layover.get('id', 'N/A')
                    layover_hours = duration // 60
                    layover_minutes = duration % 60
                    overnight = " (overnight)" if layover.get('overnight', False) else ""
                    print(f"   Layover: {airport} - {layover_hours}h {layover_minutes}m{overnight}")
            
            print()
    
    # Display airports
    airports = response_data.get('airports', [])
    if airports:
        print("AIRPORT INFORMATION:")
        print("-" * 40)
        for airport_group in airports:
            if 'departure' in airport_group:
                for dep in airport_group['departure']:
                    airport_info = dep.get('airport', {})
                    city = dep.get('city', 'N/A')
                    country = dep.get('country', 'N/A')
                    print(f"Departure: {airport_info.get('name', 'N/A')} ({airport_info.get('id', 'N/A')}) - {city}, {country}")
            
            if 'arrival' in airport_group:
                for arr in airport_group['arrival']:
                    airport_info = arr.get('airport', {})
                    city = arr.get('city', 'N/A')
                    country = arr.get('country', 'N/A')
                    print(f"Arrival: {airport_info.get('name', 'N/A')} ({airport_info.get('id', 'N/A')}) - {city}, {country}")

if __name__ == "__main__":
    demo_flight_search()
