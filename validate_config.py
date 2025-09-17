#!/usr/bin/env python3
"""
Configuration Validator
Simple script to validate your config.env setup before deployment
"""

import os
from datetime import datetime
from dotenv import load_dotenv

def validate_config():
    """Validate the configuration file"""
    print("🔧 Flight Monitor Configuration Validator")
    print("=" * 50)
    
    # Load config
    if not os.path.exists('config.env'):
        print("❌ ERROR: config.env file not found!")
        print("   Please copy config.env.example to config.env and edit it")
        return False
    
    load_dotenv('config.env')
    
    # Check required fields
    required_fields = [
        'DEPARTURE_CITY', 'DEPARTURE_CODE', 
        'ARRIVAL_CITY', 'ARRIVAL_CODES',
        'START_MONTH', 'END_MONTH', 'DEPARTURE_DAYS', 'TRIP_DURATION_DAYS'
    ]
    
    missing_fields = []
    for field in required_fields:
        if not os.getenv(field):
            missing_fields.append(field)
    
    if missing_fields:
        print(f"❌ Missing required fields: {', '.join(missing_fields)}")
        return False
    
    # Validate configuration values
    departure_city = os.getenv('DEPARTURE_CITY')
    departure_code = os.getenv('DEPARTURE_CODE')
    arrival_city = os.getenv('ARRIVAL_CITY')
    arrival_codes = os.getenv('ARRIVAL_CODES')
    
    start_month = int(os.getenv('START_MONTH', 1))
    end_month = int(os.getenv('END_MONTH', 12))
    departure_days = os.getenv('DEPARTURE_DAYS', '2,3')
    trip_duration = int(os.getenv('TRIP_DURATION_DAYS', 4))
    
    print(f"✅ Route: {departure_city} ({departure_code}) → {arrival_city} ({arrival_codes})")
    print(f"✅ Travel Period: Month {start_month} to {end_month}")
    print(f"✅ Departure Days: {departure_days}")
    print(f"✅ Trip Duration: {trip_duration} days")
    
    # Validate month range
    if not (1 <= start_month <= 12) or not (1 <= end_month <= 12):
        print("❌ ERROR: Months must be between 1-12")
        return False
    
    # Validate departure days
    try:
        days = [int(d.strip()) for d in departure_days.split(',')]
        if not all(0 <= day <= 6 for day in days):
            print("❌ ERROR: Departure days must be 0-6 (Monday=0, Sunday=6)")
            return False
    except ValueError:
        print("❌ ERROR: Departure days must be comma-separated numbers (e.g., '2,3')")
        return False
    
    # Validate trip duration
    if not (1 <= trip_duration <= 30):
        print("❌ ERROR: Trip duration should be 1-30 days")
        return False
    
    # Airport code validation
    if len(departure_code) != 3:
        print(f"⚠️  WARNING: '{departure_code}' doesn't look like a standard airport code")
    
    for code in arrival_codes.split(','):
        code = code.strip()
        if len(code) != 3:
            print(f"⚠️  WARNING: '{code}' doesn't look like a standard airport code")
    
    # Estimate API usage
    print("\n📊 Estimated API Usage:")
    
    # Calculate date range
    if start_month <= end_month:
        month_count = end_month - start_month + 1
    else:
        month_count = (12 - start_month + 1) + end_month
    
    # Rough estimation: ~4 weeks per month, departure days count
    estimated_dates = month_count * 4 * len(days)
    print(f"   Estimated dates to search: ~{estimated_dates}")
    print(f"   API calls per run: ~{estimated_dates}")
    print(f"   Monthly quota usage (7 runs): ~{estimated_dates * 7}")
    
    if estimated_dates * 7 > 250:
        print("⚠️  WARNING: High quota usage! Consider:")
        print("   - Narrowing date range (fewer months)")
        print("   - Fewer departure days")
        print("   - Upgrading SerpApi plan")
    elif estimated_dates * 7 > 100:
        print("⚠️  Note: Will need paid SerpApi plan for monthly monitoring")
    else:
        print("✅ Should work with free SerpApi tier!")
    
    print("\n🎯 Configuration looks good!")
    print("\nNext steps:")
    print("1. Set up GitHub secrets (SERPAPI_KEY, EMAIL_USER, EMAIL_PASS, EMAIL_TO)")
    print("2. Push to GitHub to trigger first run")
    print("3. Check Actions tab for monitoring status")
    
    return True

if __name__ == "__main__":
    validate_config()
