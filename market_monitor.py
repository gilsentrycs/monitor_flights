#!/usr/bin/env python3
"""
Smart Market Monitoring Strategy for Flight Prices
Optimized for regular use with SerpApi quota management
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FlightMarketMonitor:
    def __init__(self):
        self.api_key = os.getenv('SERPAPI_KEY')
        self.base_url = "https://serpapi.com/search"
        
        # Monitoring configuration
        self.destinations = {
            'paris': ['CDG', 'ORY'],
            'london': ['LHR', 'LGW', 'STN']
        }
        
        # Smart sampling strategies
        self.strategies = {
            'daily_pulse': {
                'description': 'Quick daily check - 1 weekend per destination',
                'api_calls': 2,
                'coverage': '4%',
                'use_case': 'Daily price alerts'
            },
            'weekly_overview': {
                'description': 'Weekly market scan - strategic sampling',
                'api_calls': 26,
                'coverage': '26%', 
                'use_case': 'Weekly market analysis'
            },
            'monthly_deep_dive': {
                'description': 'Comprehensive monthly analysis',
                'api_calls': 100,
                'coverage': '100%',
                'use_case': 'Trip planning & best deal guarantee'
            }
        }

    def get_quota_recommendation(self, frequency: str) -> Dict:
        """
        Get smart quota usage recommendations based on monitoring frequency
        """
        recommendations = {
            'daily': {
                'strategy': 'daily_pulse',
                'monthly_usage': 60,  # 2 calls × 30 days
                'quota_percentage': 24,
                'pros': ['Real-time price alerts', 'Catch flash sales', 'Very low usage'],
                'cons': ['Limited coverage', 'Might miss better deals']
            },
            'weekly': {
                'strategy': 'weekly_overview', 
                'monthly_usage': 104,  # 26 calls × 4 weeks
                'quota_percentage': 42,
                'pros': ['Good market coverage', 'Reasonable usage', 'Trend detection'],
                'cons': ['Weekly commitment needed']
            },
            'bi_weekly': {
                'strategy': 'weekly_overview',
                'monthly_usage': 52,  # 26 calls × 2 times
                'quota_percentage': 21,
                'pros': ['Conservative usage', 'Still good coverage'],
                'cons': ['Less frequent updates']
            },
            'monthly': {
                'strategy': 'monthly_deep_dive',
                'monthly_usage': 100,
                'quota_percentage': 40,
                'pros': ['Complete coverage', 'Guaranteed best deals', 'Perfect for planning'],
                'cons': ['Single monthly snapshot']
            }
        }
        
        return recommendations.get(frequency, recommendations['weekly'])

    def get_strategic_dates(self, strategy: str, start_date: str, end_date: str) -> List[Tuple[str, str]]:
        """
        Get strategically selected dates based on monitoring strategy
        """
        if strategy == 'daily_pulse':
            # Just get next available weekend
            return self._get_next_weekend()
        elif strategy == 'weekly_overview':
            # Strategic weekly sampling
            return self._get_weekly_sampled_dates(start_date, end_date)
        elif strategy == 'monthly_deep_dive':
            # All possible weekends
            return self._get_all_weekend_dates(start_date, end_date)
            
    def _get_next_weekend(self) -> List[Tuple[str, str]]:
        """Get the next available weekend for daily pulse monitoring"""
        from datetime import datetime, timedelta
        
        today = datetime.now()
        # Find next Friday
        days_until_friday = (4 - today.weekday()) % 7
        if days_until_friday == 0 and today.hour > 12:  # If it's Friday afternoon, get next Friday
            days_until_friday = 7
            
        friday = today + timedelta(days=days_until_friday)
        tuesday = friday + timedelta(days=4)
        
        return [(friday.strftime('%Y-%m-%d'), tuesday.strftime('%Y-%m-%d'))]

    def _get_weekly_sampled_dates(self, start_date: str, end_date: str) -> List[Tuple[str, str]]:
        """Strategic weekly sampling for better coverage"""
        # This would use the logic from weekly_flight_finder.py
        # Simplified version here
        dates = []
        current = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        week_count = 0
        while current <= end:
            if current.weekday() in [2, 3, 4, 5]:  # Wed, Thu, Fri, Sat
                if week_count % 2 == 0:  # Every other week for sampling
                    departure = current.strftime('%Y-%m-%d')
                    return_date = (current + timedelta(days=4)).strftime('%Y-%m-%d')
                    dates.append((departure, return_date))
                week_count += 1
            current += timedelta(days=1)
            
        return dates[:13]  # Cap at ~13 dates for 26 API calls

    def print_strategy_comparison(self):
        """Print comparison of different monitoring strategies"""
        print("🎯 FLIGHT MARKET MONITORING STRATEGIES")
        print("=" * 60)
        
        frequencies = ['daily', 'weekly', 'bi_weekly', 'monthly']
        
        for freq in frequencies:
            rec = self.get_quota_recommendation(freq)
            print(f"\n📅 {freq.upper()} MONITORING")
            print("-" * 30)
            print(f"Strategy: {rec['strategy']}")
            print(f"Monthly API usage: {rec['monthly_usage']} calls ({rec['quota_percentage']}% of quota)")
            print(f"Remaining quota: {250 - rec['monthly_usage']} calls")
            print("✅ Pros:")
            for pro in rec['pros']:
                print(f"   • {pro}")
            print("⚠️  Considerations:")
            for con in rec['cons']:
                print(f"   • {con}")

    def estimate_annual_usage(self, frequency: str) -> Dict:
        """Estimate annual API usage for different strategies"""
        monthly_usage = self.get_quota_recommendation(frequency)['monthly_usage']
        
        return {
            'monthly_calls': monthly_usage,
            'annual_calls': monthly_usage * 12,
            'annual_cost_estimate': f"${(monthly_usage * 12 * 0.04):.2f}",  # Rough estimate
            'calls_per_trip_found': monthly_usage / 2,  # 2 destinations
            'market_coverage': self.get_quota_recommendation(frequency)
        }

if __name__ == "__main__":
    monitor = FlightMarketMonitor()
    
    print("🔍 SMART FLIGHT MARKET MONITORING GUIDE")
    print("=" * 60)
    print("Choose your monitoring frequency based on your needs:\n")
    
    monitor.print_strategy_comparison()
    
    print("\n💡 RECOMMENDATIONS BY USE CASE:")
    print("-" * 40)
    print("🚨 Price Alert Enthusiast: Daily monitoring")
    print("📊 Market Tracker: Weekly monitoring")  
    print("💰 Budget Optimizer: Bi-weekly monitoring")
    print("🎯 Trip Planner: Monthly deep dive")
    
    print("\n🤔 QUESTIONS TO ASK YOURSELF:")
    print("-" * 35)
    print("• How often do you actually book flights?")
    print("• Do you need real-time alerts or periodic updates?")
    print("• Are you tracking for specific dates or general trends?")
    print("• Do you want to monitor multiple routes simultaneously?")
    
    print(f"\n📞 CURRENT QUOTA: 244 calls remaining this month")
    print("Choose your strategy wisely! 🎯")
