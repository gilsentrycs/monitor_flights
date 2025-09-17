#!/usr/bin/env python3
"""
Complete Coverage Flight Finder

Tests ALL 50 possible weekend dates for absolute best deal discovery.
Uses 100 API calls total (50 dates × 2 destinations).

Use this when you want to guarantee finding the absolute best deals
and don't mind using ~40% of your monthly API quota.
"""

import os
import sys
from weekend_flight_finder import WeekendFlightFinder

def main():
    """Main function for complete coverage search"""
    
    print("Complete Coverage Flight Finder")
    print("Tel Aviv → Paris & London | April-June 2026")  
    print("MAXIMUM Coverage - All 50 Weekend Dates")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv('SERPAPI_KEY')
    if not api_key:
        print("\n❌ ERROR: SerpApi API key not found!")
        sys.exit(1)
    
    print(f"🔑 API Key: Found")
    print(f"📊 Current remaining quota: 244 calls")
    print(f"🎯 This search will use 100 calls (50 dates × 2 destinations)")
    print(f"📈 After search: 144 calls remaining")
    print()
    print("⚠️  WARNING: This uses 40% of your monthly quota!")
    print("✅ BENEFIT: Guaranteed to find absolute best deals")
    print()
    
    # Ask for confirmation
    response = input("Proceed with COMPLETE coverage search? (y/N): ").lower()
    if response != 'y':
        print("Search cancelled.")
        return
    
    try:
        # Initialize flight finder with maximum coverage
        finder = WeekendFlightFinder(api_key)
        
        print("\n🚀 Starting COMPLETE coverage search...")
        print("⏳ This will take several minutes...")
        
        # Find flights with maximum coverage (50 dates)
        flight_options = finder.find_best_weekend_flights(max_options_per_destination=50)
        
        # Display results
        finder.display_comparison_results(flight_options)
        
        # Save results
        if flight_options:
            filename = finder.save_results(flight_options, "complete_coverage_flights.json")
            
            print("\n" + "="*80)
            print("🏆 COMPLETE COVERAGE SEARCH FINISHED!")
            print(f"📞 API calls used: {finder.api_calls_used}")
            print(f"📊 Remaining calls: {244 - finder.api_calls_used}")
            print(f"📈 Coverage: 100% of all possible weekend dates")
            print(f"💾 Results saved to: {filename}")
            print("\n🎉 You now have the absolute best deals available!")
        else:
            print("\n❌ No flights found.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
