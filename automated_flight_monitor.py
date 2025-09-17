#!/usr/bin/env python3
"""
Configurable Automated Flight Monitor with Email Reports
Easily customizable for any route via config.env file
"""

import os
import sys
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

# Load environment variables and configuration
load_dotenv()  # Load API keys and email settings
load_dotenv('config.env')  # Load flight configuration

class ConfigurableFlightMonitor:
    """Configurable automated flight monitoring with email reporting"""
    
    def __init__(self):
        # API and Email credentials
        self.api_key = os.getenv('SERPAPI_KEY')
        self.email_user = os.getenv('EMAIL_USER')
        self.email_pass = os.getenv('EMAIL_PASS')
        self.email_to = os.getenv('EMAIL_TO')
        
        if not all([self.api_key, self.email_user, self.email_pass, self.email_to]):
            raise ValueError("Missing required environment variables: SERPAPI_KEY, EMAIL_USER, EMAIL_PASS, EMAIL_TO")
        
        # Route configuration from config.env
        self.departure_city = os.getenv('DEPARTURE_CITY', 'Tel Aviv')
        self.departure_code = os.getenv('DEPARTURE_CODE', 'TLV')
        self.arrival_city = os.getenv('ARRIVAL_CITY', 'Paris')
        self.arrival_codes = os.getenv('ARRIVAL_CODES', 'CDG,ORY')
        
        # Trip configuration
        self.travel_year = int(os.getenv('TRAVEL_YEAR', 2026))
        self.start_month = int(os.getenv('START_MONTH', 4))
        self.end_month = int(os.getenv('END_MONTH', 6))
        self.departure_days = [int(d) for d in os.getenv('DEPARTURE_DAYS', '2,3').split(',')]  # Wed, Thu
        self.trip_duration = int(os.getenv('TRIP_DURATION_DAYS', 4))
        
        # Email and other settings
        self.email_subject_prefix = os.getenv('EMAIL_SUBJECT_PREFIX', 'Flight Monitor Report')
        self.currency = os.getenv('CURRENCY', 'USD')
        self.adults = int(os.getenv('ADULTS', 1))
        self.api_timeout = int(os.getenv('API_TIMEOUT_SECONDS', 30))
        
        # API setup
        self.base_url = "https://serpapi.com/search"
        self.api_calls_used = 0
        self.results = []
        
        print(f"🛫 Configured for {self.departure_city} ({self.departure_code}) → {self.arrival_city} ({self.arrival_codes})")
        print(f"📅 Monitoring {self.get_month_name(self.start_month)}-{self.get_month_name(self.end_month)} {self.travel_year}")
        print(f"🗓️  Departure days: {', '.join([self.get_day_name(d) for d in self.departure_days])}")
        print(f"⏱️  Trip duration: {self.trip_duration} days")
    
    def get_month_name(self, month_num):
        """Convert month number to name"""
        months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return months[month_num]
    
    def get_day_name(self, day_num):
        """Convert day number to name"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days[day_num]
        
    def get_weekend_dates(self) -> List[tuple]:
        """Get weekend dates based on configuration"""
        weekend_trips = []
        current_date = datetime(self.travel_year, self.start_month, 1)
        end_date = datetime(self.travel_year, self.end_month + 1, 1) - timedelta(days=1)
        
        while current_date <= end_date:
            if current_date.weekday() in self.departure_days:
                departure = current_date.strftime('%Y-%m-%d')
                return_date = (current_date + timedelta(days=self.trip_duration)).strftime('%Y-%m-%d')
                
                return_datetime = datetime.strptime(return_date, '%Y-%m-%d')
                if return_datetime.month <= self.end_month:
                    weekend_trips.append((departure, return_date))
            
            current_date += timedelta(days=1)
        
        return weekend_trips
    
    def search_flight(self, departure_date: str, return_date: str) -> Optional[Dict]:
        """Search for a single flight"""
        params = {
            'engine': 'google_flights',
            'departure_id': self.departure_code,
            'arrival_id': self.arrival_codes,
            'outbound_date': departure_date,
            'return_date': return_date,
            'currency': self.currency,
            'hl': 'en',
            'type': '1',
            'adults': str(self.adults),
            'api_key': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=self.api_timeout)
            self.api_calls_used += 1
            
            if response.status_code == 200:
                data = response.json()
                if 'error' not in data:
                    return data
            return None
        except Exception:
            return None
    
    def extract_flight_info(self, search_data: Dict, departure_date: str, return_date: str) -> Optional[Dict]:
        """Extract best flight from search results"""
        flights = search_data.get('best_flights', [])
        if not flights:
            flights = search_data.get('other_flights', [])
        
        if not flights:
            return None
        
        best_flight = min(flights, key=lambda x: x.get('price', float('inf')))
        
        flight_segments = best_flight.get('flights', [])
        layovers = best_flight.get('layovers', [])
        carbon_info = best_flight.get('carbon_emissions', {})
        
        return {
            'departure_date': departure_date,
            'return_date': return_date,
            'price': best_flight.get('price', 0),
            'duration_minutes': best_flight.get('total_duration', 0),
            'airline': flight_segments[0].get('airline', 'Unknown') if flight_segments else 'Unknown',
            'direct_flight': len(flight_segments) == 1,
            'layovers': [l.get('id', 'Unknown') for l in layovers],
            'carbon_kg': carbon_info.get('this_flight', 0) / 1000 if carbon_info.get('this_flight') else 0,
            'departure_day': datetime.strptime(departure_date, '%Y-%m-%d').strftime('%A'),
            'return_day': datetime.strptime(return_date, '%Y-%m-%d').strftime('%A'),
            'month': datetime.strptime(departure_date, '%Y-%m-%d').strftime('%B')
        }
    
    def run_complete_scan(self) -> List[Dict]:
        """Run complete weekend scan"""
        print(f"� Starting Automated Flight Scan: {self.departure_city} → {self.arrival_city}")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Get weekend dates based on configuration
        weekend_dates = self.get_weekend_dates()
        departure_day_names = ', '.join([self.get_day_name(d) for d in self.departure_days])
        print(f"📅 Scanning {len(weekend_dates)} weekend dates")
        print(f"🎯 Departure days: {departure_day_names}")
        print(f"⏱️  Trip duration: {self.trip_duration} days")
        
        results = []
        
        for i, (dep_date, ret_date) in enumerate(weekend_dates, 1):
            dep_day = datetime.strptime(dep_date, '%Y-%m-%d').strftime('%a')
            ret_day = datetime.strptime(ret_date, '%Y-%m-%d').strftime('%a')
            
            print(f"  {i:2d}/{len(weekend_dates)}: {dep_day} {dep_date} → {ret_day} {ret_date}")
            
            search_result = self.search_flight(dep_date, ret_date)
            
            if search_result:
                flight_info = self.extract_flight_info(search_result, dep_date, ret_date)
                if flight_info:
                    results.append(flight_info)
                    print(f"        ✅ ${flight_info['price']} {self.currency} ({flight_info['airline']})")
                else:
                    print(f"        ❌ No flights found")
            else:
                print(f"        ❌ Search failed")
        
        # Sort by price
        results.sort(key=lambda x: x['price'])
        
        print(f"\n📊 Scan Complete:")
        print(f"   API calls used: {self.api_calls_used}")
        print(f"   Flight options found: {len(results)}")
        
        self.results = results
        return results
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analyze flight results for insights"""
        if not results:
            return {}
        
        prices = [r['price'] for r in results]
        
        # Basic statistics
        analysis = {
            'total_options': len(results),
            'price_min': min(prices),
            'price_max': max(prices),
            'price_avg': sum(prices) // len(prices),
            'price_median': sorted(prices)[len(prices)//2],
            'api_calls_used': self.api_calls_used
        }
        
        # By month analysis
        by_month = {}
        for result in results:
            month = result['month']
            if month not in by_month:
                by_month[month] = []
            by_month[month].append(result['price'])
        
        analysis['by_month'] = {}
        for month, month_prices in by_month.items():
            analysis['by_month'][month] = {
                'count': len(month_prices),
                'min_price': min(month_prices),
                'avg_price': sum(month_prices) // len(month_prices),
                'best_deal': min(results, key=lambda x: x['price'] if x['month'] == month else float('inf'))
            }
        
        # Day of week analysis
        by_day = {}
        for result in results:
            day = result['departure_day']
            if day not in by_day:
                by_day[day] = []
            by_day[day].append(result['price'])
        
        analysis['by_day'] = {}
        for day, day_prices in by_day.items():
            analysis['by_day'][day] = {
                'count': len(day_prices),
                'avg_price': sum(day_prices) // len(day_prices)
            }
        
        # Find best deals
        analysis['best_deals'] = results[:5]  # Top 5 cheapest
        analysis['direct_flights'] = [r for r in results if r['direct_flight']]
        
        return analysis
    
    def generate_email_report(self, results: List[Dict], analysis: Dict) -> str:
        """Generate HTML email report"""
        now = datetime.now()
        route_title = f"{self.departure_city} → {self.arrival_city}"
        period_text = f"{self.get_month_name(self.start_month)}-{self.get_month_name(self.end_month)} {self.travel_year}"
        departure_days_text = ', '.join([self.get_day_name(d) for d in self.departure_days])
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; }}
                .summary {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .best-deals {{ margin: 20px 0; }}
                .deal {{ background: #e8f5e8; padding: 10px; margin: 5px 0; border-left: 4px solid #27ae60; border-radius: 3px; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat {{ text-align: center; }}
                .month-analysis {{ margin: 20px 0; }}
                .month {{ background: #ffeaa7; padding: 10px; margin: 5px 0; border-radius: 3px; }}
                .footer {{ text-align: center; color: #7f8c8d; margin-top: 30px; border-top: 1px solid #bdc3c7; padding-top: 15px; }}
                h1, h2 {{ color: #2c3e50; }}
                .price {{ font-weight: bold; color: #27ae60; }}
                .airline {{ color: #3498db; }}
                .direct {{ color: #e74c3c; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✈️ Flight Monitor Report</h1>
                    <h2>{route_title}</h2>
                    <p>{now.strftime('%B %d, %Y at %H:%M UTC')}</p>
                </div>
                
                <div class="summary">
                    <h2>📊 Executive Summary</h2>
                    <div class="stats">
                        <div class="stat">
                            <h3>${analysis.get('price_min', 0)}</h3>
                            <p>Best Deal</p>
                        </div>
                        <div class="stat">
                            <h3>${analysis.get('price_avg', 0)}</h3>
                            <p>Average Price</p>
                        </div>
                        <div class="stat">
                            <h3>{analysis.get('total_options', 0)}</h3>
                            <p>Options Found</p>
                        </div>
                        <div class="stat">
                            <h3>{analysis.get('api_calls_used', 0)}</h3>
                            <p>API Calls Used</p>
                        </div>
                    </div>
                </div>
                
                <div class="best-deals">
                    <h2>🏆 Top 5 Best Deals</h2>
        """
        
        for i, deal in enumerate(analysis.get('best_deals', [])[:5], 1):
            duration_hours = deal['duration_minutes'] // 60
            duration_mins = deal['duration_minutes'] % 60
            direct_text = "Direct" if deal['direct_flight'] else f"Via {', '.join(deal['layovers'])}"
            
            html += f"""
                    <div class="deal">
                        <strong>#{i}. <span class="price">${deal['price']} {self.currency}</span></strong> - 
                        <span class="airline">{deal['airline']}</span><br>
                        📅 {deal['departure_day']} {deal['departure_date']} → {deal['return_day']} {deal['return_date']}<br>
                        ✈️ {duration_hours}h {duration_mins}m | <span class="direct">{direct_text}</span> | 
                        🌱 {deal['carbon_kg']:.1f}kg CO₂
                    </div>
            """
        
        html += """
                </div>
                
                <div class="month-analysis">
                    <h2>📅 Monthly Breakdown</h2>
        """
        
        for month, data in analysis.get('by_month', {}).items():
            best_deal = data['best_deal']
            html += f"""
                    <div class="month">
                        <strong>{month}</strong>: {data['count']} options | 
                        From <span class="price">${data['min_price']} {self.currency}</span> | 
                        Avg: ${data['avg_price']} {self.currency}<br>
                        🏆 Best: {best_deal['departure_day']} {best_deal['departure_date']} - 
                        <span class="price">${best_deal['price']} {self.currency}</span> ({best_deal['airline']})
                    </div>
            """
        
        html += f"""
                </div>
                
                <div class="summary">
                    <h2>📈 Market Insights</h2>
                    <ul>
                        <li><strong>Route:</strong> {route_title}</li>
                        <li><strong>Period:</strong> {period_text}</li>
                        <li><strong>Departure Days:</strong> {departure_days_text}</li>
                        <li><strong>Trip Duration:</strong> {self.trip_duration} days</li>
                        <li><strong>Price Range:</strong> ${analysis.get('price_min', 0)} - ${analysis.get('price_max', 0)} {self.currency} (${analysis.get('price_max', 0) - analysis.get('price_min', 0)} spread)</li>
                        <li><strong>Direct Flights:</strong> {len(analysis.get('direct_flights', []))} out of {analysis.get('total_options', 0)} options</li>
                        <li><strong>Best Month:</strong> {min(analysis.get('by_month', {}).items(), key=lambda x: x[1]['min_price'])[0] if analysis.get('by_month') else 'N/A'}</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p>🤖 Automated Flight Monitor | Configurable for any route</p>
                    <p>Monitoring {period_text} weekend trips ({departure_days_text} departures)</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_email_report(self, results: List[Dict], analysis: Dict):
        """Send email report with results"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            route_text = f"{self.departure_city} → {self.arrival_city}"
            msg['Subject'] = f"{self.email_subject_prefix} - {route_text} - Best: ${analysis.get('price_min', 0)} {self.currency} - {datetime.now().strftime('%b %d')}"
            msg['From'] = self.email_user
            msg['To'] = self.email_to
            
            # Generate HTML report
            html_content = self.generate_email_report(results, analysis)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Add JSON attachment with raw data
            json_data = {
                'scan_date': datetime.now().isoformat(),
                'route': {
                    'departure_city': self.departure_city,
                    'departure_code': self.departure_code,
                    'arrival_city': self.arrival_city,
                    'arrival_codes': self.arrival_codes
                },
                'configuration': {
                    'travel_year': self.travel_year,
                    'start_month': self.start_month,
                    'end_month': self.end_month,
                    'departure_days': self.departure_days,
                    'trip_duration': self.trip_duration,
                    'currency': self.currency
                },
                'analysis': analysis,
                'all_results': results
            }
            
            json_attachment = MIMEBase('application', 'octet-stream')
            json_attachment.set_payload(json.dumps(json_data, indent=2).encode())
            encoders.encode_base64(json_attachment)
            json_attachment.add_header(
                'Content-Disposition',
                f'attachment; filename="flight_data_{datetime.now().strftime("%Y%m%d_%H%M")}.json"'
            )
            msg.attach(json_attachment)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.email_user, self.email_pass)
                server.sendmail(self.email_user, self.email_to, msg.as_string())
            
            print("✅ Email report sent successfully")
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
    
    def save_local_backup(self, results: List[Dict], analysis: Dict):
        """Save results locally as backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        route_slug = f"{self.departure_code}_{self.arrival_codes.replace(',', '_')}"
        filename = f"flight_monitor_{route_slug}_{timestamp}.json"
        
        backup_data = {
            'scan_date': datetime.now().isoformat(),
            'route': {
                'departure_city': self.departure_city,
                'departure_code': self.departure_code,
                'arrival_city': self.arrival_city,
                'arrival_codes': self.arrival_codes,
                'route_display': f"{self.departure_city} → {self.arrival_city}"
            },
            'configuration': {
                'travel_year': self.travel_year,
                'start_month': self.start_month,
                'end_month': self.end_month,
                'departure_days': self.departure_days,
                'trip_duration': self.trip_duration,
                'currency': self.currency,
                'adults': self.adults
            },
            'analysis': analysis,
            'results': results,
            'metadata': {
                'api_calls_used': self.api_calls_used,
                'scan_type': 'configurable_weekend_monitor',
                'total_possible_dates': len(self.get_weekend_dates())
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        print(f"💾 Backup saved: {filename}")
        return filename

def main():
    """Main execution function"""
    print("🤖 Configurable Flight Monitor Starting...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    try:
        # Initialize monitor
        monitor = ConfigurableFlightMonitor()
        
        # Run complete scan
        results = monitor.run_complete_scan()
        
        if not results:
            print("❌ No results found - sending alert email")
            # Could send alert email here
            return
        
        # Analyze results
        analysis = monitor.analyze_results(results)
        
        # Save local backup
        backup_file = monitor.save_local_backup(results, analysis)
        
        # Send email report
        monitor.send_email_report(results, analysis)
        
        print("\n" + "="*60)
        print("✅ CONFIGURABLE FLIGHT MONITOR COMPLETE")
        route_display = f"{monitor.departure_city} → {monitor.arrival_city}"
        print(f"📊 Route: {route_display}")
        print(f"✈️  Found {len(results)} options, best: ${analysis['price_min']} {monitor.currency}")
        print(f"📧 Email report sent to {monitor.email_to}")
        print(f"💾 Backup saved: {backup_file}")
        print(f"📞 API calls used: {monitor.api_calls_used}/250 monthly")
        
    except Exception as e:
        print(f"❌ Error in automated monitor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
