# ✈️ Configurable Flight Monitor

**Easily configurable automated flight price monitoring for any route with email reports and GitHub Actions automation.**

## 🎯 Key Features

- **🌍 Any Route**: Easily configure source and destination cities
- **📅 Flexible Dates**: Customize travel period, departure days, and trip duration  
- **📧 Email Reports**: Beautiful HTML reports with price analysis and trends
- **🤖 GitHub Actions**: Automated monitoring with smart scheduling
- **📊 Smart Analysis**: Price trends, monthly breakdown, and market insights
- **💾 Data Backup**: JSON backups stored as GitHub artifacts
- **🔧 Easy Setup**: Just configure a few settings and deploy

## 🚀 Quick Setup (3 Steps)

### 1. Fork & Configure
```bash
# Fork this repository to your GitHub account
# Edit config.env for your desired route
```

### 2. Set GitHub Secrets
Go to your repository → Settings → Secrets → Actions

Add these 4 secrets:
- `SERPAPI_KEY` - Your SerpApi API key  
- `EMAIL_USER` - Gmail address for sending reports
- `EMAIL_PASS` - Gmail app password (not regular password)
- `EMAIL_TO` - Email address to receive reports

### 3. Deploy & Monitor
```bash
# Push changes to trigger first run
git commit -am "Configure monitoring for my route"
git push

# Or manually trigger: Actions → Configurable Flight Monitor → Run workflow
```

## 🔧 Route Configuration

Edit `config.env` to customize your monitoring:

```env
# Route Configuration - EDIT THESE VALUES
DEPARTURE_CITY="Tel Aviv"
DEPARTURE_CODE="TLV"
ARRIVAL_CITY="Paris"  
ARRIVAL_CODES="CDG,ORY"

# Trip Configuration
TRAVEL_YEAR=2026
START_MONTH=4    # April
END_MONTH=6      # June  
DEPARTURE_DAYS="2,3"  # Wednesday, Thursday
TRIP_DURATION_DAYS=4  # 4-day trips

# Email Configuration
EMAIL_SUBJECT_PREFIX="Flight Monitor Report"
```

### Example Configurations

**London Monitoring:**
```env
DEPARTURE_CITY="New York"
DEPARTURE_CODE="JFK"
ARRIVAL_CITY="London"
ARRIVAL_CODES="LHR,LGW,STN"
```

**Weekend Getaways:**
```env
DEPARTURE_DAYS="4,5"  # Friday, Saturday departures
TRIP_DURATION_DAYS=3  # 3-day weekend trips
```

**Holiday Planning:**
```env
START_MONTH=11  # November
END_MONTH=1     # January
DEPARTURE_DAYS="0,1,2,3,4"  # Any weekday
```
python tel_aviv_paris_flights.py
```

The script will:
- Search for round-trip flights from Tel Aviv (TLV) to Paris (CDG, ORY)
- Show outbound date: May 15, 2025
- Show return date: May 20, 2025 (5-day trip)
- Display results with prices, duration, and detailed flight information
- Save results to a timestamped JSON file

## Sample Output

```
Tel Aviv to Paris Flight Search
==================================================

Searching for flights...
Route: TLV → CDG,ORY
Outbound: 2025-05-15
Return: 2025-05-20
Duration: 5 days

Please wait, this may take 10-30 seconds...

================================================================================
GOOGLE FLIGHTS SEARCH RESULTS
================================================================================
Search ID: 651a585815afff2d53eb9a5e
Status: Success
Route: TLV → CDG,ORY
Dates: 2025-05-15 to 2025-05-20
Currency: USD

PRICE INSIGHTS:
  Lowest Price: $450
  Price Level: Typical
  Typical Range: $400 - $600

BEST FLIGHTS (3 found):
--------------------------------------------------------------------------------
1.
  Price: $485 USD | Duration: 7h 25m | Type: Round trip
    Carbon: 1.1kg (+5% vs typical 1.0kg)
    Segments:
      1. TLV → CDG | Air France AF2042 | 2025-05-15 14:30 → 2025-05-15 19:55
      2. CDG → TLV | Air France AF2041 | 2025-05-20 08:15 → 2025-05-20 14:40

...
```

## API Parameters Explanation

The script uses these key Google Flights API parameters:

- **`departure_id`**: `TLV` (Tel Aviv Ben Gurion Airport)
- **`arrival_id`**: `CDG,ORY` (Paris Charles de Gaulle and Orly airports)
- **`outbound_date`**: `2025-05-15` (May 15, 2025)
- **`return_date`**: `2025-05-20` (May 20, 2025)
- **`type`**: `1` (Round trip)
- **`adults`**: `1` (1 adult passenger)
- **`currency`**: `USD` (US Dollars)

## Customization

You can modify the script to change:

### Dates
```python
outbound_date = "2025-05-10"  # Change to your preferred date
return_date = "2025-05-17"    # Change return date
```

### Airports
```python
departure_id = "TLV"        # Tel Aviv
arrival_id = "CDG"          # Only Charles de Gaulle (remove ORY)
# or
arrival_id = "ORY"          # Only Orly airport
```

### Search Options
```python
deep_search=True            # More accurate results (slower)
currency="EUR"              # European Euros
language="fr"               # French language
```

### Passenger Count
```python
adults="2"                  # 2 adult passengers
children="1"                # 1 child
```

## File Structure

```
flight_checker/
├── tel_aviv_paris_flights.py    # Main flight search script
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .env                          # Your API configuration (create this)
├── README.md                     # This documentation
└── flight_results_*.json         # Generated search results
```

## API Rate Limits

- **Free Account**: 100 searches/month
- **Paid Plans**: Higher limits available
- Each script run = 1 search

## Troubleshooting

### Common Issues

1. **"API key not found" error**
   - Make sure `.env` file exists
   - Check that `SERPAPI_KEY` is correctly set
   - Verify your API key is valid

2. **"No flights found" or empty results**
   - Check if dates are in the future
   - Verify airport codes are correct
   - Try different date ranges

3. **Request timeout**
   - Check internet connection
   - Try setting `deep_search=False` for faster results
   - SerpApi servers might be busy

4. **API quota exceeded**
   - Check your usage at [SerpApi Dashboard](https://serpapi.com/dashboard)
   - Wait for quota reset or upgrade plan

### Debug Mode

Add debug prints to see raw API response:

```python
# In main() function, after results = searcher.search_flights(...):
if results:
    print("\\nDEBUG - Raw API Response:")
    print(json.dumps(results, indent=2)[:1000] + "...")
```

## Google Flights API Documentation

For more details about the API parameters and response format:
- [SerpApi Google Flights API Documentation](https://serpapi.com/google-flights-api)
- [API Playground](https://serpapi.com/playground?engine=google_flights)

## Airport Codes Reference

### Tel Aviv Airports
- **TLV**: Ben Gurion Airport (main international airport)

### Paris Airports  
- **CDG**: Charles de Gaulle Airport (main international airport)
- **ORY**: Orly Airport (secondary airport)
- **BVA**: Beauvais Airport (budget airlines, farther from city)

### Other Major Cities
- **LHR**: London Heathrow
- **JFK**: New York JFK
- **LAX**: Los Angeles
- **DXB**: Dubai
- **FRA**: Frankfurt

## License

This project is for educational purposes. Please respect SerpApi's terms of service and rate limits.
