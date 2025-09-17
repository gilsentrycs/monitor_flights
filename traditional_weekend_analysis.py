#!/usr/bin/env python3
"""
Analyze traditional weekend dates (Wed/Thu only) for quota planning
"""

from datetime import datetime, timedelta

def get_traditional_weekend_dates(start_month: int, end_month: int, year: int):
    """Get Wed→Sun and Thu→Mon dates only"""
    weekend_trips = []
    
    current_date = datetime(year, start_month, 1)
    end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)
    
    while current_date <= end_date:
        weekday = current_date.weekday()  # 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday
        
        # Only Wednesday (2) or Thursday (3)
        if weekday in [2, 3]:
            departure = current_date.strftime('%Y-%m-%d')
            return_date = (current_date + timedelta(days=4)).strftime('%Y-%m-%d')
            
            return_datetime = datetime.strptime(return_date, '%Y-%m-%d')
            if return_datetime.month <= end_month:
                weekend_trips.append((departure, return_date))
        
        current_date += timedelta(days=1)
    
    return weekend_trips

if __name__ == "__main__":
    print("🔍 TRADITIONAL WEEKEND ANALYSIS - April to June 2026")
    print("=" * 60)
    print("📋 Wed→Sun (4 days) and Thu→Mon (4 days) trips only")
    print()
    
    dates = get_traditional_weekend_dates(4, 6, 2026)
    
    # Group by month and day type
    by_month = {}
    wed_count = 0
    thu_count = 0
    
    for dep_date, ret_date in dates:
        month = dep_date[:7]  # YYYY-MM
        if month not in by_month:
            by_month[month] = {'wed': [], 'thu': []}
        
        dep_datetime = datetime.strptime(dep_date, '%Y-%m-%d')
        if dep_datetime.weekday() == 2:  # Wednesday
            by_month[month]['wed'].append((dep_date, ret_date))
            wed_count += 1
        else:  # Thursday
            by_month[month]['thu'].append((dep_date, ret_date))
            thu_count += 1
    
    print(f"📊 TOTAL TRADITIONAL WEEKEND DATES: {len(dates)}")
    print(f"   Wednesdays: {wed_count} dates")
    print(f"   Thursdays: {thu_count} dates")
    print()
    
    # Show by month
    for month in sorted(by_month.keys()):
        month_name = datetime.strptime(month + '-01', '%Y-%m-%d').strftime('%B %Y')
        wed_dates = by_month[month]['wed']
        thu_dates = by_month[month]['thu']
        
        print(f"📅 {month_name.upper()} ({len(wed_dates + thu_dates)} dates)")
        print("-" * 30)
        
        if wed_dates:
            print(f"  Wednesdays ({len(wed_dates)} dates):")
            for dep, ret in wed_dates:
                dep_day = datetime.strptime(dep, '%Y-%m-%d').strftime('%b %d')
                ret_day = datetime.strptime(ret, '%Y-%m-%d').strftime('%b %d')
                print(f"    {dep_day} → {ret_day}")
        
        if thu_dates:
            print(f"  Thursdays ({len(thu_dates)} dates):")
            for dep, ret in thu_dates:
                dep_day = datetime.strptime(dep, '%Y-%m-%d').strftime('%b %d')
                ret_day = datetime.strptime(ret, '%Y-%m-%d').strftime('%b %d')
                print(f"    {dep_day} → {ret_day}")
        print()
    
    print("🎯 API USAGE STRATEGIES:")
    print("=" * 40)
    print(f"Conservative (1 per month): 3 calls")
    print(f"Balanced (half of dates): {len(dates)//2} calls")
    print(f"Complete coverage: {len(dates)} calls")
    print()
    print("💡 RECOMMENDATION:")
    print(f"   With {len(dates)} total dates, you could test every")
    print(f"   traditional weekend and still use only {len(dates)} API calls!")
    print(f"   That's just {len(dates)/250*100:.1f}% of your monthly quota.")
