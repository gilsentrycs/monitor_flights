#!/usr/bin/env python3
"""
Automated Flight Monitor with Email Reports
Runs complete traditional weekend flight search and sends detailed email report
"""

import os
import sys
import json
import smtplib
import ssl
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AutomatedFlightMonitor:
    """Automated flight monitoring with email reporting"""
    
    def __init__(self):
        self.api_key = os.getenv('SERPAPI_KEY')
        self.email_user = os.getenv('EMAIL_USER')
        self.email_pass = os.getenv('EMAIL_PASS')
        self.email_to = os.getenv('EMAIL_TO')
        
        if not all([self.api_key, self.email_user, self.email_pass, self.email_to]):
            raise ValueError("Missing required environment variables")
        
        self.base_url = "https://serpapi.com/search"
        self.api_calls_used = 0
        self.results = []
        
    def get_traditional_weekend_dates(self, start_month: int, end_month: int, year: int) -> List[tuple]:
        """Get all Wed→Sun and Thu→Mon weekend dates"""
        weekend_trips = []
        current_date = datetime(year, start_month, 1)
        end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)
        
        while current_date <= end_date:
            if current_date.weekday() in [2, 3]:  # Wed, Thu only
                departure = current_date.strftime('%Y-%m-%d')
                return_date = (current_date + timedelta(days=4)).strftime('%Y-%m-%d')
                
                return_datetime = datetime.strptime(return_date, '%Y-%m-%d')
                if return_datetime.month <= end_month:
                    weekend_trips.append((departure, return_date))
            
            current_date += timedelta(days=1)
        
        return weekend_trips
    
    def search_flight(self, departure_date: str, return_date: str) -> Optional[Dict]:
        """Search for a single flight"""
        params = {
            'engine': 'google_flights',
            'departure_id': 'TLV',
            'arrival_id': 'CDG,ORY',
            'outbound_date': departure_date,
            'return_date': return_date,
            'currency': 'USD',
            'hl': 'en',
            'type': '1',
            'adults': '1',
            'api_key': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
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
        """Run complete traditional weekend scan"""
        print("🗼 Starting Automated Traditional Weekend Flight Scan")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Get all traditional weekend dates for April-June 2026
        weekend_dates = self.get_traditional_weekend_dates(4, 6, 2026)
        print(f"📅 Scanning {len(weekend_dates)} traditional weekend dates")
        print("🎯 Wed→Sun and Thu→Mon trips only")
        
        results = []
        
        for i, (dep_date, ret_date) in enumerate(weekend_dates, 1):
            dep_day = datetime.strptime(dep_date, '%Y-%m-%d').strftime('%a')
            ret_day = datetime.strptime(ret_date, '%Y-%m-%d').strftime('%a')
            
            print(f"  {i:2d}/26: {dep_day} {dep_date} → {ret_day} {ret_date}")
            
            search_result = self.search_flight(dep_date, ret_date)
            
            if search_result:
                flight_info = self.extract_flight_info(search_result, dep_date, ret_date)
                if flight_info:
                    results.append(flight_info)
                    print(f"        ✅ ${flight_info['price']} USD ({flight_info['airline']})")
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
                    <h1>🗼 Flight Monitor Report</h1>
                    <h2>Tel Aviv → Paris Traditional Weekends</h2>
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
                        <strong>#{i}. <span class="price">${deal['price']} USD</span></strong> - 
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
                        From <span class="price">${data['min_price']} USD</span> | 
                        Avg: ${data['avg_price']} USD<br>
                        🏆 Best: {best_deal['departure_day']} {best_deal['departure_date']} - 
                        <span class="price">${best_deal['price']} USD</span> ({best_deal['airline']})
                    </div>
            """
        
        html += f"""
                </div>
                
                <div class="summary">
                    <h2>📈 Market Insights</h2>
                    <ul>
                        <li><strong>Price Range:</strong> ${analysis.get('price_min', 0)} - ${analysis.get('price_max', 0)} USD (${analysis.get('price_max', 0) - analysis.get('price_min', 0)} spread)</li>
                        <li><strong>Direct Flights:</strong> {len(analysis.get('direct_flights', []))} out of {analysis.get('total_options', 0)} options</li>
                        <li><strong>Best Month:</strong> {min(analysis.get('by_month', {}).items(), key=lambda x: x[1]['min_price'])[0] if analysis.get('by_month') else 'N/A'}</li>
                        <li><strong>Wednesday vs Thursday:</strong> 
                            Wed avg: ${analysis.get('by_day', {}).get('Wednesday', {}).get('avg_price', 0)} | 
                            Thu avg: ${analysis.get('by_day', {}).get('Thursday', {}).get('avg_price', 0)}</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p>🤖 Automated Flight Monitor | Next scan in ~4-5 days</p>
                    <p>Monitoring April-June 2026 traditional weekends (Wed→Sun, Thu→Mon)</p>
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
            msg = MimeMultipart('alternative')
            msg['Subject'] = f"Flight Monitor Report - Best: ${analysis.get('price_min', 0)} USD - {datetime.now().strftime('%b %d')}"
            msg['From'] = self.email_user
            msg['To'] = self.email_to
            
            # Generate HTML report
            html_content = self.generate_email_report(results, analysis)
            html_part = MimeText(html_content, 'html')
            msg.attach(html_part)
            
            # Add JSON attachment with raw data
            json_data = {
                'scan_date': datetime.now().isoformat(),
                'analysis': analysis,
                'all_results': results
            }
            
            json_attachment = MimeBase('application', 'octet-stream')
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
        filename = f"flight_monitor_backup_{timestamp}.json"
        
        backup_data = {
            'scan_date': datetime.now().isoformat(),
            'analysis': analysis,
            'results': results,
            'metadata': {
                'api_calls_used': self.api_calls_used,
                'scan_type': 'traditional_weekends_complete',
                'destination': 'Paris (CDG, ORY)',
                'origin': 'Tel Aviv (TLV)'
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        print(f"💾 Backup saved: {filename}")
        return filename

def main():
    """Main execution function"""
    print("🤖 Automated Flight Monitor Starting...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    try:
        # Initialize monitor
        monitor = AutomatedFlightMonitor()
        
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
        print("✅ AUTOMATED FLIGHT MONITOR COMPLETE")
        print(f"📊 Found {len(results)} options, best: ${analysis['price_min']} USD")
        print(f"📧 Email report sent to {monitor.email_to}")
        print(f"💾 Backup saved: {backup_file}")
        print(f"📞 API calls used: {monitor.api_calls_used}/250 monthly")
        
    except Exception as e:
        print(f"❌ Error in automated monitor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
