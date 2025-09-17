#!/usr/bin/env python3
"""
Tel Aviv to Paris Flight Search Script

This script uses the SerpApi Google Flights API to search for flights
from Tel Aviv (TLV) to Paris (CDG, ORY) for a 5-day trip in May 2025.

Author: Flight Checker
Date: September 2025
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FlightSearcher:
    """Class to handle Google Flights API searches using SerpApi"""
    
    def __init__(self, api_key=None):
        """Initialize the FlightSearcher with API key"""
        self.api_key = api_key or os.getenv('SERPAPI_KEY')
        if not self.api_key:
            raise ValueError("SerpApi API key is required. Set SERPAPI_KEY environment variable or pass api_key parameter.")
        
        self.base_url = "https://serpapi.com/search"
        
    def search_flights(self, departure_id, arrival_id, outbound_date, return_date, 
                      currency="USD", language="en", deep_search=False):
        """
        Search for flights using Google Flights API
        
        Args:
            departure_id (str): Departure airport code (e.g., 'TLV')
            arrival_id (str): Arrival airport code(s) (e.g., 'CDG,ORY')
            outbound_date (str): Outbound date in YYYY-MM-DD format
            return_date (str): Return date in YYYY-MM-DD format
            currency (str): Currency code (default: USD)
            language (str): Language code (default: en)
            deep_search (bool): Enable deep search for more accurate results
            
        Returns:
            dict: API response containing flight data
        """
        
        params = {
            'engine': 'google_flights',
            'departure_id': departure_id,
            'arrival_id': arrival_id,
            'outbound_date': outbound_date,
            'return_date': return_date,
            'currency': currency,
            'hl': language,
            'type': '1',  # Round trip
            'adults': '1',  # 1 adult passenger
            'api_key': self.api_key
        }
        
        if deep_search:
            params['deep_search'] = 'true'
            
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return None

    def format_flight_info(self, flight_data):
        """
        Format flight information for display
        
        Args:
            flight_data (dict): Single flight object from API response
            
        Returns:
            str: Formatted flight information
        """
        if not flight_data:
            return "No flight data available"
        
        # Extract basic info
        price = flight_data.get('price', 'N/A')
        total_duration = flight_data.get('total_duration', 0)
        flight_type = flight_data.get('type', 'N/A')
        
        # Convert duration from minutes to hours and minutes
        hours = total_duration // 60
        minutes = total_duration % 60
        duration_str = f"{hours}h {minutes}m" if total_duration > 0 else "N/A"
        
        # Format carbon emissions
        carbon_info = ""
        if 'carbon_emissions' in flight_data:
            carbon = flight_data['carbon_emissions']
            this_flight = carbon.get('this_flight', 0)
            typical = carbon.get('typical_for_this_route', 0)
            diff_percent = carbon.get('difference_percent', 0)
            
            # Convert grams to kg
            this_flight_kg = this_flight / 1000 if this_flight else 0
            typical_kg = typical / 1000 if typical else 0
            
            carbon_info = f"\\n    Carbon: {this_flight_kg:.1f}kg ({diff_percent:+d}% vs typical {typical_kg:.1f}kg)"
        
        # Format flight segments
        segments_info = ""
        if 'flights' in flight_data:
            segments_info = "\\n    Segments:"
            for i, flight in enumerate(flight_data['flights']):
                dep_airport = flight.get('departure_airport', {})
                arr_airport = flight.get('arrival_airport', {})
                airline = flight.get('airline', 'Unknown')
                flight_num = flight.get('flight_number', 'N/A')
                
                dep_code = dep_airport.get('id', 'N/A')
                dep_time = dep_airport.get('time', 'N/A')
                arr_code = arr_airport.get('id', 'N/A')
                arr_time = arr_airport.get('time', 'N/A')
                
                segments_info += f"\\n      {i+1}. {dep_code} → {arr_code} | {airline} {flight_num} | {dep_time} → {arr_time}"
        
        # Format layovers
        layover_info = ""
        if 'layovers' in flight_data and flight_data['layovers']:
            layover_info = "\\n    Layovers:"
            for layover in flight_data['layovers']:
                duration = layover.get('duration', 0)
                airport = layover.get('id', 'N/A')
                layover_hours = duration // 60
                layover_minutes = duration % 60
                overnight = " (overnight)" if layover.get('overnight', False) else ""
                layover_info += f"\\n      {airport}: {layover_hours}h {layover_minutes}m{overnight}"
        
        return f"""
  Price: ${price} {flight_data.get('currency', 'USD')} | Duration: {duration_str} | Type: {flight_type}{carbon_info}{segments_info}{layover_info}
"""

    def display_results(self, response_data):
        """
        Display formatted flight search results
        
        Args:
            response_data (dict): Complete API response
        """
        if not response_data:
            print("No data to display")
            return
        
        # Display search metadata
        search_meta = response_data.get('search_metadata', {})
        search_params = response_data.get('search_parameters', {})
        
        print("\\n" + "="*80)
        print("GOOGLE FLIGHTS SEARCH RESULTS")
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
        
        # Display best flights
        best_flights = response_data.get('best_flights', [])
        if best_flights:
            print(f"\\nBEST FLIGHTS ({len(best_flights)} found):")
            print("-" * 80)
            for i, flight in enumerate(best_flights[:5], 1):  # Show top 5
                print(f"{i}.{self.format_flight_info(flight)}")
        
        # Display other flights (if any)
        other_flights = response_data.get('other_flights', [])
        if other_flights:
            print(f"\\nOTHER FLIGHTS ({len(other_flights)} found):")
            print("-" * 80)
            for i, flight in enumerate(other_flights[:3], 1):  # Show top 3
                print(f"{i}.{self.format_flight_info(flight)}")
        
        # Display airports information
        airports = response_data.get('airports', [])
        if airports:
            print("\\nAIRPORT INFORMATION:")
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


def main():
    """Main function to run the flight search"""
    
    print("Tel Aviv to Paris Flight Search")
    print("="*50)
    
    # Check for API key
    api_key = os.getenv('SERPAPI_KEY')
    if not api_key:
        print("\\nERROR: SerpApi API key not found!")
        print("Please:")
        print("1. Copy .env.example to .env")
        print("2. Get your API key from https://serpapi.com/manage-api-key")
        print("3. Add your API key to .env file")
        print("4. Run the script again")
        sys.exit(1)
    
    # Initialize flight searcher
    try:
        searcher = FlightSearcher(api_key)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Define search parameters for Tel Aviv to Paris, 5 days in October 2025
    departure_id = "TLV"  # Tel Aviv Ben Gurion Airport
    arrival_id = "CDG,ORY"  # Paris Charles de Gaulle and Orly
    
    # October 2025 dates for a 5-day trip (adjusted to work with API)
    outbound_date = "2025-10-15"  # Tuesday
    return_date = "2025-10-20"    # Sunday (5 days later)
    
    print(f"\\nSearching for flights...")
    print(f"Route: {departure_id} → {arrival_id}")
    print(f"Outbound: {outbound_date}")
    print(f"Return: {return_date}")
    print(f"Duration: 5 days")
    print("\\nPlease wait, this may take 10-30 seconds...")
    
    # Search for flights
    results = searcher.search_flights(
        departure_id=departure_id,
        arrival_id=arrival_id,
        outbound_date=outbound_date,
        return_date=return_date,
        currency="USD",
        language="en",
        deep_search=False  # Set to True for more accurate results (but slower)
    )
    
    # Display results
    if results:
        # Check for errors in the response
        if 'error' in results:
            print(f"\\nAPI Error: {results['error']}")
            return
        
        searcher.display_results(results)
        
        # Save results to file
        output_file = f"flight_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\\nResults saved to: {output_file}")
        
    else:
        print("\\nFailed to retrieve flight data. Please check your API key and internet connection.")

if __name__ == "__main__":
    main()
