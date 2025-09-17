#!/usr/bin/env python3
"""
Enhanced Multi-Destination Weekend Flight Finder

This script finds the best weekend flights from Tel Aviv to both Paris and London
for 5-day trips during April-June 2026. It compares options and shows the best deals.

Features:
- Searches multiple destinations (Paris, London)
- Finds weekend departures (Friday/Saturday)
- 5-day trips including weekends
- Compares prices across destinations
- Optimizes API usage

Author: Flight Checker Enhanced
Date: September 2025
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

# Load environment variables
load_dotenv()

@dataclass
class FlightOption:
    """Data class to store flight information for comparison"""
    destination: str
    destination_city: str
    departure_date: str
    return_date: str
    price: int
    duration_minutes: int
    carbon_kg: float
    airline: str
    direct_flight: bool
    layovers: List[str]
    search_data: Dict

class WeekendFlightFinder:
    """Enhanced flight searcher for weekend trips to multiple destinations"""
    
    def __init__(self, api_key=None):
        """Initialize the WeekendFlightFinder with API key"""
        self.api_key = api_key or os.getenv('SERPAPI_KEY')
        if not self.api_key:
            raise ValueError("SerpApi API key is required. Set SERPAPI_KEY environment variable.")
        
        self.base_url = "https://serpapi.com/search"
        self.api_calls_used = 0
        
        # Define destinations
        self.destinations = {
            'paris': {
                'codes': 'CDG,ORY',
                'city': 'Paris',
                'country': 'France'
            },
            'london': {
                'codes': 'LHR,LGW,STN',
                'city': 'London', 
                'country': 'United Kingdom'
            }
        }
    
    def get_weekend_dates(self, start_month: int, end_month: int, year: int) -> List[Tuple[str, str]]:
        """
        Generate extended weekend departure dates (Wed/Thu/Fri/Sat) with 5-day returns
        
        Args:
            start_month: Starting month (e.g., 4 for April)
            end_month: Ending month (e.g., 6 for June)
            year: Year (e.g., 2026)
            
        Returns:
            List of (departure_date, return_date) tuples
        """
        weekend_trips = []
        
        # Start from the first day of start_month
        current_date = datetime(year, start_month, 1)
        end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)
        
        while current_date <= end_date:
            weekday = current_date.weekday()  # 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday
            
            # Check if it's Wednesday (2), Thursday (3), Friday (4) or Saturday (5)
            if weekday in [2, 3, 4, 5]:  # Wed, Thu, Fri, Sat
                departure = current_date.strftime('%Y-%m-%d')
                return_date = (current_date + timedelta(days=5)).strftime('%Y-%m-%d')
                
                # Make sure return date is not beyond our end month
                return_datetime = datetime.strptime(return_date, '%Y-%m-%d')
                if return_datetime.month <= end_month:
                    weekend_trips.append((departure, return_date))
            
            current_date += timedelta(days=1)
        
        return weekend_trips
    
    def select_distributed_dates(self, all_dates: List[Tuple[str, str]], max_dates: int) -> List[Tuple[str, str]]:
        """
        Select dates distributed across the entire period instead of just the first dates
        
        Args:
            all_dates: List of all possible (departure, return) date tuples
            max_dates: Maximum number of dates to select
            
        Returns:
            List of distributed date tuples across April-June period
        """
        if len(all_dates) <= max_dates:
            return all_dates
        
        # Group dates by month for better distribution
        dates_by_month = {}
        for dep_date, ret_date in all_dates:
            month = dep_date[:7]  # YYYY-MM format
            if month not in dates_by_month:
                dates_by_month[month] = []
            dates_by_month[month].append((dep_date, ret_date))
        
        selected_dates = []
        months = sorted(dates_by_month.keys())
        dates_per_month = max_dates // len(months)
        remaining_dates = max_dates % len(months)
        
        print(f"  Distributing across months: {months}")
        
        # Select dates from each month
        for i, month in enumerate(months):
            month_dates = dates_by_month[month]
            # Give extra date to first months if there's a remainder
            num_from_month = dates_per_month + (1 if i < remaining_dates else 0)
            
            # Select evenly spaced dates from this month
            if len(month_dates) <= num_from_month:
                selected_from_month = month_dates
            else:
                # Select evenly distributed dates
                step = len(month_dates) // num_from_month
                selected_from_month = []
                for j in range(num_from_month):
                    idx = j * step
                    if idx < len(month_dates):
                        selected_from_month.append(month_dates[idx])
            
            selected_dates.extend(selected_from_month)
            print(f"    {month}: Selected {len(selected_from_month)} dates from {len(month_dates)} available")
        
        return selected_dates[:max_dates]  # Ensure we don't exceed max_dates
    
    def search_flights(self, departure_id: str, arrival_id: str, outbound_date: str, 
                      return_date: str, destination_name: str) -> Optional[Dict]:
        """
        Search for flights with error handling and API call tracking
        """
        params = {
            'engine': 'google_flights',
            'departure_id': departure_id,
            'arrival_id': arrival_id,
            'outbound_date': outbound_date,
            'return_date': return_date,
            'currency': 'USD',
            'hl': 'en',
            'type': '1',  # Round trip
            'adults': '1',
            'api_key': self.api_key
        }
        
        try:
            print(f"  Searching {destination_name} ({outbound_date} to {return_date})...")
            response = requests.get(self.base_url, params=params, timeout=30)
            self.api_calls_used += 1
            
            if response.status_code == 200:
                data = response.json()
                if 'error' in data:
                    print(f"    ⚠️  API Error: {data['error']}")
                    return None
                return data
            else:
                print(f"    ❌ HTTP Error {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"    ❌ Request Error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"    ❌ JSON Error: {e}")
            return None
    
    def extract_best_flight(self, search_data: Dict, destination: str, destination_city: str, 
                          departure_date: str, return_date: str) -> Optional[FlightOption]:
        """Extract the best flight option from search results"""
        
        # Try best_flights first, then other_flights
        flights = search_data.get('best_flights', [])
        if not flights:
            flights = search_data.get('other_flights', [])
        
        if not flights:
            return None
        
        # Get the cheapest flight
        best_flight = min(flights, key=lambda x: x.get('price', float('inf')))
        
        # Extract flight details
        price = best_flight.get('price', 0)
        duration = best_flight.get('total_duration', 0)
        
        # Carbon emissions
        carbon_info = best_flight.get('carbon_emissions', {})
        carbon_kg = carbon_info.get('this_flight', 0) / 1000 if carbon_info.get('this_flight') else 0
        
        # Check if it's a direct flight
        flight_segments = best_flight.get('flights', [])
        direct_flight = len(flight_segments) == 1
        
        # Get airline from first segment
        airline = flight_segments[0].get('airline', 'Unknown') if flight_segments else 'Unknown'
        
        # Get layovers
        layovers = []
        for layover in best_flight.get('layovers', []):
            layovers.append(layover.get('id', 'Unknown'))
        
        return FlightOption(
            destination=destination,
            destination_city=destination_city,
            departure_date=departure_date,
            return_date=return_date,
            price=price,
            duration_minutes=duration,
            carbon_kg=carbon_kg,
            airline=airline,
            direct_flight=direct_flight,
            layovers=layovers,
            search_data=best_flight
        )
    
    def find_best_weekend_flights(self, max_options_per_destination: int = 3) -> List[FlightOption]:
        """
        Find the best weekend flight options for all destinations
        
        Args:
            max_options_per_destination: Maximum number of weekend options to try per destination
            
        Returns:
            List of FlightOption objects sorted by price
        """
        print("🔍 Finding Best Extended Weekend Flights: Tel Aviv → Paris & London")
        print("📅 Period: April-June 2026")
        print("🗓️  Extended weekend departures (Wed/Thu/Fri/Sat) with 5-day returns")
        print("   Wed→Sun | Thu→Mon | Fri→Tue | Sat→Wed")
        print("="*70)
        
        # Get extended weekend dates for April-June 2026
        weekend_dates = self.get_weekend_dates(4, 6, 2026)
        print(f"Found {len(weekend_dates)} possible extended weekend departure dates")
        
        # Distribute dates across the entire period for better coverage
        selected_dates = self.select_distributed_dates(weekend_dates, max_options_per_destination)
        print(f"Testing {len(selected_dates)} dates per destination distributed across Apr-Jun")
        print()
        
        all_flight_options = []
        
        # Search each destination
        for dest_key, dest_info in self.destinations.items():
            print(f"🌍 Searching {dest_info['city']}, {dest_info['country']}")
            print("-" * 40)
            
            destination_options = []
            
            # Try each extended weekend date across the period
            for i, (departure_date, return_date) in enumerate(selected_dates):
                # Convert date to day name for display
                dep_datetime = datetime.strptime(departure_date, '%Y-%m-%d')
                ret_datetime = datetime.strptime(return_date, '%Y-%m-%d')
                dep_day = dep_datetime.strftime('%A')
                ret_day = ret_datetime.strftime('%A')
                dep_month = dep_datetime.strftime('%B')
                
                print(f"  Option {i+1}: {dep_day} {departure_date} → {ret_day} {return_date} ({dep_month})")
                
                # Search flights
                search_result = self.search_flights(
                    departure_id='TLV',
                    arrival_id=dest_info['codes'],
                    outbound_date=departure_date,
                    return_date=return_date,
                    destination_name=dest_info['city']
                )
                
                if search_result:
                    flight_option = self.extract_best_flight(
                        search_result, dest_key, dest_info['city'], 
                        departure_date, return_date
                    )
                    
                    if flight_option:
                        destination_options.append(flight_option)
                        print(f"    ✅ Found: ${flight_option.price} USD ({flight_option.airline})")
                    else:
                        print(f"    ❌ No flights found")
                else:
                    print(f"    ❌ Search failed")
                
                print()
            
            all_flight_options.extend(destination_options)
            print(f"Found {len(destination_options)} options for {dest_info['city']}")
            print()
        
        # Sort all options by price
        all_flight_options.sort(key=lambda x: x.price)
        
        print(f"📊 Total API calls used: {self.api_calls_used}")
        print(f"🎯 Found {len(all_flight_options)} total flight options")
        
        return all_flight_options
    
    def display_comparison_results(self, flight_options: List[FlightOption]):
        """Display comparison results in a user-friendly format"""
        
        if not flight_options:
            print("❌ No flight options found")
            return
        
        print("\n" + "="*80)
        print("🏆 BEST EXTENDED WEEKEND FLIGHT OPTIONS - TEL AVIV TO EUROPE")
        print("="*80)
        
        # Group by destination for better display
        by_destination = {}
        for option in flight_options:
            if option.destination not in by_destination:
                by_destination[option.destination] = []
            by_destination[option.destination].append(option)
        
        # Display overall best options first
        print(f"\n🥇 TOP 5 CHEAPEST OPTIONS (All Destinations)")
        print("-" * 60)
        
        for i, option in enumerate(flight_options[:5], 1):
            duration_hours = option.duration_minutes // 60
            duration_mins = option.duration_minutes % 60
            direct_status = "Direct" if option.direct_flight else f"Via {', '.join(option.layovers)}"
            
            dep_date = datetime.strptime(option.departure_date, '%Y-%m-%d')
            ret_date = datetime.strptime(option.return_date, '%Y-%m-%d')
            dep_day = dep_date.strftime('%A')
            ret_day = ret_date.strftime('%A')
            
            print(f"{i}. 🌍 {option.destination_city.upper()}")
            print(f"   💰 ${option.price} USD")
            print(f"   📅 {dep_day} {option.departure_date} → {ret_day} {option.return_date}")
            print(f"   ✈️  {option.airline} | {duration_hours}h {duration_mins}m | {direct_status}")
            print(f"   🌱 {option.carbon_kg:.1f}kg CO₂")
            print()
        
        # Display by destination
        for dest_key, options in by_destination.items():
            dest_city = options[0].destination_city
            print(f"\n📍 {dest_city.upper()} OPTIONS")
            print("-" * 40)
            
            for i, option in enumerate(options, 1):
                duration_hours = option.duration_minutes // 60
                duration_mins = option.duration_minutes % 60
                direct_status = "Direct" if option.direct_flight else f"Via {', '.join(option.layovers)}"
                
                dep_date = datetime.strptime(option.departure_date, '%Y-%m-%d')
                ret_date = datetime.strptime(option.return_date, '%Y-%m-%d')
                dep_day = dep_date.strftime('%A')
                ret_day = ret_date.strftime('%A')
                
                print(f"  {i}. ${option.price} USD | {dep_day} {option.departure_date} → {ret_day} {option.return_date}")
                print(f"     {option.airline} | {duration_hours}h {duration_mins}m | {direct_status}")
                print()
        
        # Show summary statistics
        prices = [opt.price for opt in flight_options]
        print(f"\n📈 PRICE ANALYSIS")
        print("-" * 30)
        print(f"💰 Cheapest: ${min(prices)} USD")
        print(f"💸 Most Expensive: ${max(prices)} USD")
        print(f"📊 Average: ${sum(prices) // len(prices)} USD")
        
        # Compare destinations
        if len(by_destination) > 1:
            print(f"\n🆚 DESTINATION COMPARISON")
            print("-" * 30)
            for dest_key, options in by_destination.items():
                if options:
                    dest_prices = [opt.price for opt in options]
                    avg_price = sum(dest_prices) // len(dest_prices)
                    min_price = min(dest_prices)
                    print(f"🌍 {options[0].destination_city}: From ${min_price} USD (avg: ${avg_price})")
    
    def save_results(self, flight_options: List[FlightOption], filename: str = None):
        """Save search results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"weekend_flights_comparison_{timestamp}.json"
        
        # Convert flight options to serializable format
        results = {
            'search_metadata': {
                'search_date': datetime.now().isoformat(),
                'api_calls_used': self.api_calls_used,
                'destinations_searched': list(self.destinations.keys()),
                'period': 'April-June 2026',
                'trip_type': '5-day extended weekend trips (Wed/Thu/Fri/Sat departures)'
            },
            'flight_options': []
        }
        
        for option in flight_options:
            results['flight_options'].append({
                'destination': option.destination,
                'destination_city': option.destination_city,
                'departure_date': option.departure_date,
                'return_date': option.return_date,
                'price_usd': option.price,
                'duration_minutes': option.duration_minutes,
                'carbon_kg': option.carbon_kg,
                'airline': option.airline,
                'direct_flight': option.direct_flight,
                'layovers': option.layovers,
                'raw_search_data': option.search_data
            })
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")
        return filename

def main():
    """Main function to run the enhanced weekend flight search"""
    
    print("Enhanced Extended Weekend Flight Finder")
    print("Tel Aviv → Paris & London | April-June 2026")
    print("Wed→Sun | Thu→Mon | Fri→Tue | Sat→Wed Options")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv('SERPAPI_KEY')
    if not api_key:
        print("\n❌ ERROR: SerpApi API key not found!")
        print("Please check your .env file and make sure SERPAPI_KEY is set.")
        sys.exit(1)
    
    try:
        # Initialize flight finder
        finder = WeekendFlightFinder(api_key)
        
        print(f"🔑 API Key: Found (ending in ...{api_key[-8:]})")
        print("🎯 Searching for extended weekend flights (conserving API calls)...")
        print("   Includes: Wed→Sun, Thu→Mon, Fri→Tue, Sat→Wed")
        print()
        
        # Find best weekend flights (test 3 dates per destination to get better coverage)
        flight_options = finder.find_best_weekend_flights(max_options_per_destination=3)
        
        # Display results
        finder.display_comparison_results(flight_options)
        
        # Save results
        if flight_options:
            filename = finder.save_results(flight_options)
            
            print("\n" + "="*80)
            print("✅ SEARCH COMPLETE!")
            print(f"📞 API calls used: {finder.api_calls_used} out of your 250/month limit")
            print(f"📊 Remaining calls: {250 - finder.api_calls_used}")
            print(f"💾 Detailed results saved to: {filename}")
        else:
            print("\n❌ No flights found. Try different dates or destinations.")
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
