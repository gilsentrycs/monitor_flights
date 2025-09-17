#!/usr/bin/env python3
"""
Weekend Date Analysis Script
Shows exactly what weekend dates are available and what we're testing
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def analyze_weekend_dates():
    """Analyze all possible weekend dates in April-June 2026"""
    
    print("🔍 WEEKEND DATE ANALYSIS - April to June 2026")
    print("="*60)
    
    # Generate all possible extended weekend dates
    weekend_trips = []
    current_date = datetime(2026, 4, 1)  # April 1, 2026
    end_date = datetime(2026, 6, 30)     # June 30, 2026
    
    while current_date <= end_date:
        weekday = current_date.weekday()  # 0=Monday, 2=Wed, 3=Thu, 4=Fri, 5=Sat
        
        if weekday in [2, 3, 4, 5]:  # Wed, Thu, Fri, Sat
            departure = current_date.strftime('%Y-%m-%d')
            return_date = (current_date + timedelta(days=5)).strftime('%Y-%m-%d')
            
            # Make sure return date is still in June or earlier
            return_datetime = datetime.strptime(return_date, '%Y-%m-%d')
            if return_datetime.month <= 6:
                weekend_trips.append((departure, return_date, current_date.strftime('%A')))
        
        current_date += timedelta(days=1)
    
    # Group by month
    by_month = {'April': [], 'May': [], 'June': []}
    month_names = {4: 'April', 5: 'May', 6: 'June'}
    
    for dep, ret, day in weekend_trips:
        month = datetime.strptime(dep, '%Y-%m-%d').month
        by_month[month_names[month]].append((dep, ret, day))
    
    # Display analysis
    total_dates = len(weekend_trips)
    print(f"📊 TOTAL POSSIBLE WEEKEND DEPARTURE DATES: {total_dates}")
    print()
    
    for month_name, dates in by_month.items():
        print(f"📅 {month_name.upper()} 2026 ({len(dates)} dates)")
        print("-" * 40)
        
        # Group by day of week
        by_day = {'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': []}
        for dep, ret, day in dates:
            by_day[day].append((dep, ret))
        
        for day, day_dates in by_day.items():
            if day_dates:
                print(f"  {day}s ({len(day_dates)} dates):")
                for dep, ret in day_dates:
                    dep_date = datetime.strptime(dep, '%Y-%m-%d')
                    ret_date = datetime.strptime(ret, '%Y-%m-%d')
                    print(f"    {dep} → {ret} ({dep_date.strftime('%b %d')} → {ret_date.strftime('%b %d')})")
        print()
    
    # Show what current script tests vs all available
    print("🎯 CURRENT SCRIPT BEHAVIOR")
    print("-" * 40)
    print("Currently testing: 3 dates total (1 per month)")
    print("Available dates: 50 total")
    print("Coverage: 6% of all possible dates")
    print()
    
    print("💡 OPTIONS FOR COMPLETE COVERAGE")
    print("-" * 40)
    print("Option 1: Test ALL 50 dates (50 API calls per destination = 100 total)")
    print("Option 2: Test 2-3 dates per month (18-24 API calls total)")  
    print("Option 3: Test 1 date per week (12-15 API calls total)")
    print("Option 4: Keep current sampling (6 API calls total)")
    print()
    
    # Calculate API costs
    print("📞 API CALL ESTIMATES")
    print("-" * 40)
    print("Current (3 dates × 2 destinations): 6 calls")
    print("Weekly sampling (13 dates × 2 destinations): 26 calls")
    print("Monthly detailed (24 dates × 2 destinations): 48 calls") 
    print("Complete coverage (50 dates × 2 destinations): 100 calls")
    print()
    print(f"Your remaining quota: {250 - 6} calls")
    
    return weekend_trips, by_month

def show_recommended_sampling():
    """Show recommended sampling strategies"""
    
    print("🎯 RECOMMENDED SAMPLING STRATEGIES")
    print("="*50)
    
    strategies = [
        {
            'name': 'Conservative (Current)',
            'description': '1 date per month, distributed',
            'api_calls': 6,
            'coverage': '6%',
            'pros': 'Very low API usage, quick overview',
            'cons': 'Might miss better deals'
        },
        {
            'name': 'Weekly Sampling',
            'description': '1 date per week across the period',
            'api_calls': 26,
            'coverage': '26%',
            'pros': 'Good coverage, reasonable API usage',
            'cons': 'Still might miss some deals'
        },
        {
            'name': 'Comprehensive',
            'description': '6-8 dates per month, mixed days',
            'api_calls': 48,
            'coverage': '48%',
            'pros': 'Very good coverage, finds best deals',
            'cons': 'Higher API usage'
        },
        {
            'name': 'Complete',
            'description': 'All 50 possible weekend dates',
            'api_calls': 100,
            'coverage': '100%',
            'pros': 'Guaranteed to find absolute best deals',
            'cons': 'Uses 40% of monthly quota'
        }
    ]
    
    for i, strategy in enumerate(strategies, 1):
        print(f"{i}. {strategy['name']}")
        print(f"   📋 {strategy['description']}")
        print(f"   📞 API calls: {strategy['api_calls']}")
        print(f"   📊 Coverage: {strategy['coverage']}")
        print(f"   ✅ Pros: {strategy['pros']}")
        print(f"   ⚠️  Cons: {strategy['cons']}")
        print()

if __name__ == "__main__":
    weekend_trips, by_month = analyze_weekend_dates()
    show_recommended_sampling()
    
    print("🤔 WHAT WOULD YOU LIKE TO DO?")
    print("-" * 30)
    print("A. Keep current conservative approach (6 calls)")
    print("B. Try weekly sampling (26 calls)")  
    print("C. Go comprehensive (48 calls)")
    print("D. Test everything (100 calls)")
    print()
    print("The choice depends on how thorough you want to be vs API quota conservation!")
