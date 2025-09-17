#!/usr/bin/env python3
"""
Smart Monthly Flight Monitoring Scheduler
Optimally distributes API quota over a full month for maximum market insight
"""

from datetime import datetime, timedelta
import json

def calculate_smart_schedule():
    """Calculate optimal schedule for flight monitoring over a full month"""
    
    # Starting parameters
    start_date = datetime(2025, 9, 17)  # Today
    end_date = start_date + timedelta(days=30)  # Full month
    available_calls = 216
    calls_per_run = 26  # Complete traditional weekend coverage
    
    print("📅 SMART MONTHLY FLIGHT MONITORING SCHEDULE")
    print("=" * 60)
    print(f"Period: {start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}")
    print(f"Available API calls: {available_calls}")
    print(f"Calls per complete scan: {calls_per_run}")
    print()
    
    # Calculate maximum possible runs
    max_runs = available_calls // calls_per_run
    remaining_calls = available_calls % calls_per_run
    
    print(f"🎯 OPTIMIZATION ANALYSIS:")
    print(f"   Maximum possible runs: {max_runs}")
    print(f"   Total calls used: {max_runs * calls_per_run}")
    print(f"   Remaining calls: {remaining_calls}")
    print(f"   Quota utilization: {(max_runs * calls_per_run / available_calls * 100):.1f}%")
    print()
    
    # Smart distribution strategies
    print("📊 DISTRIBUTION STRATEGIES:")
    print("-" * 40)
    
    strategies = {
        "Conservative": {
            "runs": 6,
            "description": "Bi-weekly monitoring with buffer",
            "frequency_days": 5
        },
        "Balanced": {
            "runs": 7,
            "description": "Every 4 days for good coverage",
            "frequency_days": 4.3
        },
        "Aggressive": {
            "runs": 8,
            "description": "Maximum coverage, every 3-4 days",
            "frequency_days": 3.75
        }
    }
    
    recommended_strategy = "Balanced"
    
    for name, strategy in strategies.items():
        calls_used = strategy["runs"] * calls_per_run
        quota_percent = (calls_used / available_calls) * 100
        remaining = available_calls - calls_used
        
        indicator = "👑" if name == recommended_strategy else "  "
        print(f"{indicator} {name}:")
        print(f"     Runs: {strategy['runs']} ({strategy['description']})")
        print(f"     Frequency: Every {strategy['frequency_days']:.1f} days")
        print(f"     API calls: {calls_used} ({quota_percent:.1f}% of quota)")
        print(f"     Remaining: {remaining} calls for other uses")
        print()
    
    # Generate recommended schedule
    selected_strategy = strategies[recommended_strategy]
    num_runs = selected_strategy["runs"]
    
    print(f"🗓️  RECOMMENDED SCHEDULE: {recommended_strategy.upper()}")
    print("=" * 50)
    
    # Calculate optimal spacing
    total_days = 30
    interval_days = total_days / (num_runs - 1) if num_runs > 1 else total_days
    
    schedule = []
    current_date = start_date
    
    for run_num in range(1, num_runs + 1):
        # Add some smart timing considerations
        if run_num == 1:
            # First run: Start immediately for baseline
            run_date = current_date
        elif run_num == num_runs:
            # Last run: End of period
            run_date = end_date
        else:
            # Distribute evenly with slight randomization for market dynamics
            days_to_add = interval_days * (run_num - 1)
            # Add small offset to avoid always running same day of week
            offset = (run_num % 3) - 1  # -1, 0, or 1 day offset
            run_date = start_date + timedelta(days=days_to_add + offset)
        
        # Prefer Tuesday-Thursday for better market data (avoid weekend API limits)
        while run_date.weekday() in [5, 6]:  # Saturday, Sunday
            run_date += timedelta(days=1)
        
        schedule.append({
            "run_number": run_num,
            "date": run_date,
            "day_name": run_date.strftime("%A"),
            "date_str": run_date.strftime("%Y-%m-%d"),
            "calls_used": calls_per_run,
            "purpose": get_run_purpose(run_num, num_runs)
        })
        
        current_date = run_date + timedelta(days=interval_days)
    
    # Display schedule
    total_scheduled_calls = 0
    for run in schedule:
        total_scheduled_calls += run["calls_used"]
        print(f"Run {run['run_number']:2d}: {run['day_name']} {run['date_str']} "
              f"({run['calls_used']} calls) - {run['purpose']}")
    
    print()
    print(f"📈 SCHEDULE SUMMARY:")
    print(f"   Total runs: {len(schedule)}")
    print(f"   Total API calls: {total_scheduled_calls}")
    print(f"   Remaining calls: {available_calls - total_scheduled_calls}")
    print(f"   Average interval: {interval_days:.1f} days")
    print()
    
    # Market analysis benefits
    print("🎯 MARKET ANALYSIS BENEFITS:")
    print("-" * 35)
    print("✅ Capture weekly price fluctuations")
    print("✅ Detect seasonal trends (Sep→Oct)")
    print("✅ Monitor demand changes approaching peak season")
    print("✅ Identify booking windows for best deals")
    print("✅ Track airline pricing strategies")
    print()
    
    # GitHub Actions cron schedule
    print("⏰ GITHUB ACTIONS CRON SCHEDULE:")
    print("-" * 40)
    for i, run in enumerate(schedule):
        # Convert to UTC cron (assuming user timezone is relevant)
        cron_time = f"{run['date'].hour} {run['date'].day} {run['date'].month} * *"
        print(f"# Run {run['run_number']}: {run['date_str']}")
        print(f"- cron: '0 {run['date'].hour} {run['date'].day} {run['date'].month} * *'")
    
    print()
    print("💡 BONUS RECOMMENDATIONS:")
    print("-" * 30)
    remaining_after_schedule = available_calls - total_scheduled_calls
    print(f"With {remaining_after_schedule} calls remaining, you could:")
    print(f"• Add London monitoring (13 calls per scan)")
    print(f"• Test specific holiday dates (5-10 calls)")
    print(f"• Monitor last-minute deals (15-20 calls)")
    print(f"• Keep buffer for urgent searches")
    
    return schedule

def get_run_purpose(run_num, total_runs):
    """Get descriptive purpose for each run"""
    if run_num == 1:
        return "Baseline market scan"
    elif run_num == total_runs:
        return "Final month analysis"
    elif run_num <= 3:
        return "Early trend detection"
    elif run_num >= total_runs - 2:
        return "Peak season preparation"
    else:
        return "Market trend monitoring"

def generate_github_schedule(schedule):
    """Generate GitHub Actions workflow schedule"""
    print("\n🤖 GITHUB ACTIONS IMPLEMENTATION:")
    print("=" * 45)
    
    workflow_yml = """name: Smart Flight Monitoring
on:
  schedule:"""
    
    for run in schedule:
        # GitHub Actions cron: minute hour day month day_of_week
        cron_expr = f"    - cron: '0 {run['date'].hour} {run['date'].day} {run['date'].month} * *'"
        workflow_yml += f"\n{cron_expr}  # Run {run['run_number']}: {run['date_str']}"
    
    workflow_yml += """
  workflow_dispatch:  # Allow manual runs

jobs:
  flight-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run flight scan
      env:
        SERPAPI_KEY: ${{ secrets.SERPAPI_KEY }}
        EMAIL_USER: ${{ secrets.EMAIL_USER }}
        EMAIL_PASS: ${{ secrets.EMAIL_PASS }}
        EMAIL_TO: ${{ secrets.EMAIL_TO }}
      run: python automated_flight_monitor.py
"""
    
    print("📁 Save this as .github/workflows/flight-monitor.yml:")
    print("-" * 50)
    print(workflow_yml)
    
    return workflow_yml

if __name__ == "__main__":
    schedule = calculate_smart_schedule()
    generate_github_schedule(schedule)
    
    print("\n🚀 NEXT STEPS:")
    print("=" * 20)
    print("1. Initialize git repository")
    print("2. Create GitHub repo and add secrets")
    print("3. Set up email notification script")
    print("4. Deploy workflow file")
    print("5. Test with manual run")
