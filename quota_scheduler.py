#!/usr/bin/env python3
"""
Quota Schedule Calculator for Flight Monitoring
Calculate optimal run schedule to maximize quota usage until month end
"""

from datetime import datetime, timedelta
import calendar

def calculate_quota_schedule():
    """Calculate optimal schedule for remaining quota"""
    
    # Current situation
    remaining_calls = 216
    calls_per_run = 26
    today = datetime.now()
    
    # Calculate days remaining in September 2025
    _, last_day = calendar.monthrange(2025, 9)
    month_end = datetime(2025, 9, last_day)
    days_remaining = (month_end - today).days + 1  # Include today
    
    # Calculate possible runs
    max_possible_runs = remaining_calls // calls_per_run
    
    print("🎯 QUOTA OPTIMIZATION SCHEDULE - SEPTEMBER 2025")
    print("=" * 60)
    print(f"📅 Today: {today.strftime('%Y-%m-%d')}")
    print(f"📅 Month ends: {month_end.strftime('%Y-%m-%d')}")
    print(f"⏰ Days remaining: {days_remaining}")
    print(f"📞 Calls remaining: {remaining_calls}")
    print(f"🔄 Calls per complete run: {calls_per_run}")
    print(f"🎲 Maximum possible runs: {max_possible_runs}")
    print(f"📊 Calls that would be used: {max_possible_runs * calls_per_run}")
    print(f"📊 Calls that would remain: {remaining_calls - (max_possible_runs * calls_per_run)}")
    print()
    
    # Calculate different scheduling strategies
    strategies = []
    
    # Strategy 1: Even distribution
    if max_possible_runs > 0:
        days_between_runs = days_remaining // max_possible_runs
        strategies.append({
            'name': 'Even Distribution',
            'runs': max_possible_runs,
            'frequency': f"Every {days_between_runs} days",
            'calls_used': max_possible_runs * calls_per_run,
            'efficiency': f"{((max_possible_runs * calls_per_run) / remaining_calls) * 100:.1f}%"
        })
    
    # Strategy 2: Weekly runs
    weekly_runs = min(days_remaining // 7, max_possible_runs)
    if weekly_runs > 0:
        strategies.append({
            'name': 'Weekly Runs',
            'runs': weekly_runs,
            'frequency': "Every 7 days",
            'calls_used': weekly_runs * calls_per_run,
            'efficiency': f"{((weekly_runs * calls_per_run) / remaining_calls) * 100:.1f}%"
        })
    
    # Strategy 3: Bi-weekly runs
    biweekly_runs = min(days_remaining // 14, max_possible_runs)
    if biweekly_runs > 0:
        strategies.append({
            'name': 'Bi-weekly Runs',
            'runs': biweekly_runs,
            'frequency': "Every 14 days",
            'calls_used': biweekly_runs * calls_per_run,
            'efficiency': f"{((biweekly_runs * calls_per_run) / remaining_calls) * 100:.1f}%"
        })
    
    # Strategy 4: End-of-month burst
    strategies.append({
        'name': 'End-of-Month Burst',
        'runs': max_possible_runs,
        'frequency': f"All {max_possible_runs} runs in final days",
        'calls_used': max_possible_runs * calls_per_run,
        'efficiency': f"{((max_possible_runs * calls_per_run) / remaining_calls) * 100:.1f}%"
    })
    
    print("📋 SCHEDULING STRATEGIES:")
    print("=" * 50)
    for i, strategy in enumerate(strategies, 1):
        print(f"{i}. {strategy['name']}")
        print(f"   🔄 Runs: {strategy['runs']}")
        print(f"   ⏰ Frequency: {strategy['frequency']}")
        print(f"   📞 API calls used: {strategy['calls_used']}")
        print(f"   📊 Quota efficiency: {strategy['efficiency']}")
        print()
    
    # Generate specific schedule for even distribution (recommended)
    print("🗓️  RECOMMENDED SCHEDULE (Even Distribution):")
    print("=" * 50)
    
    if max_possible_runs > 0:
        schedule_dates = []
        current_date = today
        
        for run_num in range(max_possible_runs):
            schedule_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=days_between_runs)
            
            # Don't go past month end
            if current_date > month_end:
                break
        
        for i, date in enumerate(schedule_dates, 1):
            day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
            print(f"Run {i:2d}: {day_name} {date} ({calls_per_run} API calls)")
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total runs: {len(schedule_dates)}")
        print(f"   Total API calls: {len(schedule_dates) * calls_per_run}")
        print(f"   Quota utilization: {((len(schedule_dates) * calls_per_run) / remaining_calls) * 100:.1f}%")
        print(f"   Remaining calls: {remaining_calls - (len(schedule_dates) * calls_per_run)}")
        
        return schedule_dates
    else:
        print("❌ Not enough quota for even one complete run")
        return []

def generate_github_actions_schedule(schedule_dates):
    """Generate GitHub Actions cron schedule"""
    
    print("\n🤖 GITHUB ACTIONS AUTOMATION:")
    print("=" * 40)
    
    # Convert dates to cron expressions
    cron_expressions = []
    for date in schedule_dates:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        # Run at 9 AM UTC on scheduled dates
        cron = f"0 9 {date_obj.day} {date_obj.month} *"
        cron_expressions.append(cron)
        print(f"📅 {date}: {cron}")
    
    print(f"\n📋 GitHub Actions Configuration:")
    print("```yaml")
    print("name: Flight Price Monitor")
    print("on:")
    print("  schedule:")
    for cron in cron_expressions:
        print(f"    - cron: '{cron}'")
    print("  workflow_dispatch:  # Allow manual trigger")
    print("```")
    
    return cron_expressions

if __name__ == "__main__":
    schedule = calculate_quota_schedule()
    if schedule:
        generate_github_actions_schedule(schedule)
        
        print(f"\n🎯 NEXT STEPS:")
        print("1. Set up GitHub repository with Actions")
        print("2. Configure email notifications")
        print("3. Store SerpApi key as GitHub secret")
        print("4. Deploy automated monitoring")
        print("\nReady to proceed? 🚀")
