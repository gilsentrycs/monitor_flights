#!/usr/bin/env python3
"""
Enhanced Weekly Sampling Flight Finder

Tests approximately 1 weekend date per week across April-June 2026
for much better coverage while conserving API calls.

Coverage: ~26% of all possible dates (13 dates vs 50 total)
API Usage: ~26 calls (13 dates × 2 destinations)
"""

import os
import sys
from weekend_flight_finder import WeekendFlightFinder
from datetime import datetime, timedelta
from typing import List, Tuple

def get_weekly_sampled_dates(start_month: int, end_month: int, year: int) -> List[Tuple[str, str]]:
    """
    Get weekly sampled weekend dates for better coverage
    
    Returns approximately 1 date per week across the entire period
    """
    # Get all possible dates first
    all_dates = []
    current_date = datetime(year, start_month, 1)
    end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)
    
    while current_date <= end_date:
        weekday = current_date.weekday()  # 0=Monday, 2=Wed, 3=Thu, 4=Fri, 5=Sat
        
        if weekday in [2, 3, 4, 5]:  # Wed, Thu, Fri, Sat
            departure = current_date.strftime('%Y-%m-%d')
            return_date = (current_date + timedelta(days=5)).strftime('%Y-%m-%d')
            
            return_datetime = datetime.strptime(return_date, '%Y-%m-%d')
            if return_datetime.month <= end_month:
                all_dates.append((departure, return_date))
        
        current_date += timedelta(days=1)
    
    # Sample approximately every 4 dates (weekly sampling)
    sampled_dates = []
    step = max(1, len(all_dates) // 13)  # Target ~13 dates
    
    for i in range(0, len(all_dates), step):
        if len(sampled_dates) < 13:  # Cap at 13 dates
            sampled_dates.append(all_dates[i])
    
    return sampled_dates

class WeeklyFlightFinder(WeekendFlightFinder):
    """Enhanced version with weekly sampling"""
    
    def find_weekly_sampled_flights(self) -> List:
        """Find flights using weekly sampling strategy"""
        
        print("🔍 Enhanced Weekly Sampling Search: Tel Aviv → Paris & London")
        print("📅 Period: April-June 2026")
        print("🗓️  Extended weekend departures (Wed/Thu/Fri/Sat) - Weekly sampling")
        print("📊 Coverage: ~26% of all possible dates for better deal discovery")
        print("="*70)
        
        # Get weekly sampled dates
        sampled_dates = get_weekly_sampled_dates(4, 6, 2026)
        print(f"Testing {len(sampled_dates)} strategically sampled dates per destination")
        print(f"This covers ~{len(sampled_dates)*2:.0f}% of all possible weekend dates")
        print()
        
        all_flight_options = []
        
        # Search each destination
        for dest_key, dest_info in self.destinations.items():
            print(f"🌍 Searching {dest_info['city']}, {dest_info['country']}")
            print("-" * 50)
            
            destination_options = []
            
            # Try each sampled date
            for i, (departure_date, return_date) in enumerate(sampled_dates):
                dep_datetime = datetime.strptime(departure_date, '%Y-%m-%d')
                ret_datetime = datetime.strptime(return_date, '%Y-%m-%d')
                dep_day = dep_datetime.strftime('%A')
                ret_day = ret_datetime.strftime('%A')
                dep_month = dep_datetime.strftime('%B')
                
                print(f"  {i+1:2d}. {dep_day} {departure_date} → {ret_day} {return_date} ({dep_month})")
                
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
                        print(f"      ✅ ${flight_option.price} USD ({flight_option.airline})")
                    else:
                        print(f"      ❌ No flights found")
                else:
                    print(f"      ❌ Search failed")
            
            all_flight_options.extend(destination_options)
            print(f"\n✨ Found {len(destination_options)} options for {dest_info['city']}")
            print()
        
        # Sort all options by price
        all_flight_options.sort(key=lambda x: x.price)
        
        print(f"📊 Total API calls used: {self.api_calls_used}")
        print(f"🎯 Found {len(all_flight_options)} total flight options")
        print(f"📈 Coverage: Much better than basic sampling!")
        
        return all_flight_options

def main():
    """Main function for weekly sampling search"""
    
    print("Enhanced Weekly Sampling Flight Finder")
    print("Tel Aviv → Paris & London | April-June 2026")
    print("Better Coverage Strategy - Weekly Sampling")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv('SERPAPI_KEY')
    if not api_key:
        print("\n❌ ERROR: SerpApi API key not found!")
        sys.exit(1)
    
    try:
        # Initialize enhanced flight finder
        finder = WeeklyFlightFinder(api_key)
        
        print(f"🔑 API Key: Found")
        print(f"📊 Remaining quota: 244 calls")
        print(f"🎯 This search will use ~26 calls (much better coverage!)")
        print()
        
        # Ask for confirmation
        response = input("Proceed with weekly sampling search? (y/N): ").lower()
        if response != 'y':
            print("Search cancelled.")
            return
        
        print("\n🚀 Starting enhanced weekly sampling search...")
        
        # Find flights with weekly sampling
        flight_options = finder.find_weekly_sampled_flights()
        
        # Display results
        finder.display_comparison_results(flight_options)
        
        # Save results
        if flight_options:
            filename = finder.save_results(flight_options, "weekly_sampled_flights.json")
            
            print("\n" + "="*80)
            print("✅ ENHANCED SEARCH COMPLETE!")
            print(f"📞 API calls used: {finder.api_calls_used}")
            print(f"📊 Remaining calls: {244 - finder.api_calls_used}")
            print(f"📈 Coverage: {len(flight_options)//2} dates tested vs 50 possible (~{(len(flight_options)//2)*2}%)")
            print(f"💾 Results saved to: {filename}")
        else:
            print("\n❌ No flights found.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
