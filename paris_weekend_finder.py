#!/usr/bin/env python3
"""
Paris-Only Weekend Flight Finder (Optimized for API Quota)

This script finds the best weekend flights from Tel Aviv to Paris only
for 5-day trips during April-June 2026. Single destination to reduce API usage.

Features:
- Paris only (CDG, ORY airports)
- Weekend departures (Wed/Thu/Fri/Sat)
- 5-day trips including weekends
- Optimized API usage (half the calls of multi-destination)
- Smart date distribution

Author: Flight Checker Paris Edition
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
    """Data class to store flight information"""
    departure_date: str
    return_date: str
    price: int
    duration_minutes: int
    carbon_kg: float
    airline: str
    direct_flight: bool
    layovers: List[str]
    search_data: Dict

class ParisWeekendFinder:
    """Paris-focused flight searcher for weekend trips"""
    
    def __init__(self, api_key=None):
        """Initialize with API key"""
        self.api_key = api_key or os.getenv('SERPAPI_KEY')
        if not self.api_key:
            raise ValueError("SerpApi API key is required. Set SERPAPI_KEY environment variable.")
        
        self.base_url = "https://serpapi.com/search"
        self.api_calls_used = 0
        
        # Paris airports only
        self.paris_airports = 'CDG,ORY'
    
    def get_weekend_dates(self, start_month: int, end_month: int, year: int) -> List[Tuple[str, str]]:
        """
        Generate traditional weekend departure dates (Wed/Thu only) with 5-day returns
        Wed→Sun (4 days) and Thu→Mon (4 days)
        """
        weekend_trips = []
        
        # Start from the first day of start_month
        current_date = datetime(year, start_month, 1)
        end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)
        
        while current_date <= end_date:
            weekday = current_date.weekday()  # 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday
            
            # Check if it's Wednesday (2) or Thursday (3) only
            if weekday in [2, 3]:  # Wed, Thu only
                departure = current_date.strftime('%Y-%m-%d')
                
                # Wed→Sun = 4 days, Thu→Mon = 4 days
                return_date = (current_date + timedelta(days=4)).strftime('%Y-%m-%d')
                
                # Make sure return date is not beyond our end month
                return_datetime = datetime.strptime(return_date, '%Y-%m-%d')
                if return_datetime.month <= end_month:
                    weekend_trips.append((departure, return_date))
            
            current_date += timedelta(days=1)
        
        return weekend_trips
    
    def select_smart_dates(self, all_dates: List[Tuple[str, str]], strategy: str = 'weekly') -> List[Tuple[str, str]]:
        """
        Smart date selection strategies for API quota optimization
        
        Args:
            all_dates: All possible weekend dates
            strategy: 'conservative' (3 dates), 'weekly' (13 dates), 'comprehensive' (24 dates)
        """
        if strategy == 'conservative':
            max_dates = 3
        elif strategy == 'weekly':
            max_dates = 13
        elif strategy == 'comprehensive':
            max_dates = 24
        else:
            max_dates = 13  # Default to weekly
        
        if len(all_dates) <= max_dates:
            return all_dates
        
        # Group dates by month for even distribution
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
        
        print(f"📊 Using '{strategy}' strategy: {max_dates} dates distributed across {len(months)} months")
        
        # Select dates from each month
        for i, month in enumerate(months):
            month_dates = dates_by_month[month]
            # Give extra dates to first months if there's a remainder
            num_from_month = dates_per_month + (1 if i < remaining_dates else 0)
            
            # Select evenly spaced dates from this month
            if len(month_dates) <= num_from_month:
                selected_from_month = month_dates
            else:
                # Select evenly distributed dates within the month
                step = len(month_dates) / num_from_month
                selected_from_month = []
                for j in range(num_from_month):
                    idx = int(j * step)
                    if idx < len(month_dates):
                        selected_from_month.append(month_dates[idx])
            
            selected_dates.extend(selected_from_month)
            month_name = datetime.strptime(month + '-01', '%Y-%m-%d').strftime('%B')
            print(f"   {month_name}: {len(selected_from_month)} dates from {len(month_dates)} available")
        
        return selected_dates[:max_dates]
    
    def search_flights(self, departure_id: str, arrival_id: str, outbound_date: str, 
                      return_date: str) -> Optional[Dict]:
        """Search for flights with error handling and API call tracking"""
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
            print(f"     Searching {outbound_date} to {return_date}...")
            response = requests.get(self.base_url, params=params, timeout=30)
            self.api_calls_used += 1
            
            if response.status_code == 200:
                data = response.json()
                if 'error' in data:
                    print(f"       ⚠️  API Error: {data['error']}")
                    return None
                return data
            else:
                print(f"       ❌ HTTP Error {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"       ❌ Request Error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"       ❌ JSON Error: {e}")
            return None
    
    def extract_best_flight(self, search_data: Dict, departure_date: str, return_date: str) -> Optional[FlightOption]:
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
    
    def find_best_paris_flights(self, strategy: str = 'weekly') -> List[FlightOption]:
        """
        Find the best weekend flight options to Paris
        
        Args:
            strategy: 'conservative' (3 calls), 'weekly' (13 calls), 'comprehensive' (24 calls)
            
        Returns:
            List of FlightOption objects sorted by price
        """
        print("🗼 Finding Best Traditional Weekend Flights: Tel Aviv → Paris")
        print("📅 Period: April-June 2026")
        print("🗓️  Traditional weekend departures only:")
        print("   Wed→Sun (4 days) | Thu→Mon (4 days)")
        print("="*70)
        
        # Get traditional weekend dates for April-June 2026
        weekend_dates = self.get_weekend_dates(4, 6, 2026)
        print(f"🔍 Found {len(weekend_dates)} possible traditional weekend departure dates (Wed/Thu only)")
        
        # Select dates based on strategy
        selected_dates = self.select_smart_dates(weekend_dates, strategy)
        print(f"🎯 Testing {len(selected_dates)} dates with '{strategy}' strategy")
        print()
        
        flight_options = []
        
        print(f"🌍 Searching Paris (CDG, ORY)")
        print("-" * 40)
        
        # Try each selected weekend date
        for i, (departure_date, return_date) in enumerate(selected_dates):
            # Convert date to day name for display
            dep_datetime = datetime.strptime(departure_date, '%Y-%m-%d')
            ret_datetime = datetime.strptime(return_date, '%Y-%m-%d')
            dep_day = dep_datetime.strftime('%a')
            ret_day = ret_datetime.strftime('%a')
            dep_month = dep_datetime.strftime('%b')
            
            print(f"  {i+1:2d}. {dep_day} {departure_date} → {ret_day} {return_date} ({dep_month})")
            
            # Search flights
            search_result = self.search_flights(
                departure_id='TLV',
                arrival_id=self.paris_airports,
                outbound_date=departure_date,
                return_date=return_date
            )
            
            if search_result:
                flight_option = self.extract_best_flight(
                    search_result, departure_date, return_date
                )
                
                if flight_option:
                    flight_options.append(flight_option)
                    print(f"       ✅ ${flight_option.price} USD ({flight_option.airline})")
                else:
                    print(f"       ❌ No flights found")
            else:
                print(f"       ❌ Search failed")
        
        # Sort options by price
        flight_options.sort(key=lambda x: x.price)
        
        print()
        print(f"📊 API calls used: {self.api_calls_used}")
        print(f"🎯 Found {len(flight_options)} flight options")
        
        return flight_options
    
    def display_results(self, flight_options: List[FlightOption]):
        """Display results in a user-friendly format"""
        
        if not flight_options:
            print("❌ No flight options found")
            return
        
        print("\n" + "="*70)
        print("🏆 BEST TRADITIONAL WEEKEND FLIGHTS: TEL AVIV → PARIS")
        print("="*70)
        
        print(f"\n🥇 TOP {min(len(flight_options), 10)} CHEAPEST OPTIONS")
        print("-" * 50)
        
        for i, option in enumerate(flight_options[:10], 1):
            duration_hours = option.duration_minutes // 60
            duration_mins = option.duration_minutes % 60
            direct_status = "Direct" if option.direct_flight else f"Via {', '.join(option.layovers)}"
            
            dep_date = datetime.strptime(option.departure_date, '%Y-%m-%d')
            ret_date = datetime.strptime(option.return_date, '%Y-%m-%d')
            dep_day = dep_date.strftime('%A')
            ret_day = ret_date.strftime('%A')
            dep_month = dep_date.strftime('%B')
            
            print(f"{i:2d}. 💰 ${option.price} USD")
            print(f"    📅 {dep_day} {option.departure_date} → {ret_day} {option.return_date}")
            print(f"    ✈️  {option.airline} | {duration_hours}h {duration_mins}m | {direct_status}")
            print(f"    🌱 {option.carbon_kg:.1f}kg CO₂ | 📍 {dep_month}")
            print()
        
        # Show summary statistics
        prices = [opt.price for opt in flight_options]
        print(f"\n📈 PRICE ANALYSIS ({len(flight_options)} options)")
        print("-" * 40)
        print(f"💰 Cheapest: ${min(prices)} USD")
        print(f"💸 Most Expensive: ${max(prices)} USD")
        print(f"📊 Average: ${sum(prices) // len(prices)} USD")
        
        # Group by month
        by_month = {}
        for option in flight_options:
            month = datetime.strptime(option.departure_date, '%Y-%m-%d').strftime('%B')
            if month not in by_month:
                by_month[month] = []
            by_month[month].append(option.price)
        
        print(f"\n📅 BY MONTH")
        print("-" * 20)
        for month, prices in by_month.items():
            avg_price = sum(prices) // len(prices)
            min_price = min(prices)
            print(f"{month}: From ${min_price} USD (avg: ${avg_price}, {len(prices)} options)")
    
    def save_results(self, flight_options: List[FlightOption], strategy: str, filename: str = None):
        """Save search results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"paris_flights_{strategy}_{timestamp}.json"
        
        # Convert flight options to serializable format
        results = {
            'search_metadata': {
                'destination': 'Paris (CDG, ORY)',
                'search_date': datetime.now().isoformat(),
                'strategy': strategy,
                'api_calls_used': self.api_calls_used,
                'period': 'April-June 2026',
                'trip_type': '4-day traditional weekend trips (Wed/Thu departures only)',
                'coverage_percentage': f"{(self.api_calls_used/50)*100:.1f}%" if self.api_calls_used <= 50 else "100%"
            },
            'flight_options': []
        }
        
        for option in flight_options:
            results['flight_options'].append({
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
    """Main function with strategy selection"""
    
    print("🗼 Paris-Only Traditional Weekend Flight Finder")
    print("Tel Aviv → Paris | April-June 2026 | Wed→Sun & Thu→Mon Only")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv('SERPAPI_KEY')
    if not api_key:
        print("\n❌ ERROR: SerpApi API key not found!")
        print("Please check your .env file and make sure SERPAPI_KEY is set.")
        sys.exit(1)
    
    try:
        # Initialize flight finder
        finder = ParisWeekendFinder(api_key)
        
        print(f"🔑 API Key: Found (ending in ...{api_key[-8:]})")
        
        # Strategy selection
        print("\n🎯 SEARCH STRATEGY OPTIONS:")
        print("1. Conservative  - 3 dates   (3 API calls)   | 6% coverage")
        print("2. Weekly       - 13 dates  (13 API calls)  | 26% coverage")  
        print("3. Comprehensive - 24 dates  (24 API calls)  | 48% coverage")
        print()
        
        # Default to weekly for good balance
        strategy = 'weekly'
        
        print(f"🚀 Using '{strategy}' strategy for optimal balance of coverage vs API usage")
        print()
        
        # Find best weekend flights
        flight_options = finder.find_best_paris_flights(strategy)
        
        # Display results
        finder.display_results(flight_options)
        
        # Save results
        if flight_options:
            filename = finder.save_results(flight_options, strategy)
            
            print("\n" + "="*70)
            print("✅ PARIS SEARCH COMPLETE!")
            print(f"📞 API calls used: {finder.api_calls_used}")
            print(f"📊 Remaining calls this month: {250 - finder.api_calls_used}")
            print(f"💾 Detailed results saved to: {filename}")
            
            # Quota efficiency summary
            coverage = (finder.api_calls_used / 50) * 100
            print(f"\n🎯 QUOTA EFFICIENCY:")
            print(f"   Coverage: {coverage:.1f}% of all possible weekend dates")
            print(f"   Efficiency: {len(flight_options)/finder.api_calls_used:.1f} options per API call")
            
        else:
            print("\n❌ No flights found. Try different dates or check API connectivity.")
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
