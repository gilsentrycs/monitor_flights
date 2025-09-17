# 🗼 Automated Flight Monitor

Smart automated flight price monitoring for Tel Aviv → Paris traditional weekend trips with email reports.

## 📊 Overview

This system automatically monitors flight prices for traditional weekend trips (Wednesday→Sunday and Thursday→Monday) from Tel Aviv to Paris for April-June 2026. It runs on a smart schedule using GitHub Actions and sends detailed email reports with pricing analysis and trends.

### 🎯 Key Features

- **Traditional Weekend Focus**: Only Wed→Sun and Thu→Mon 4-day trips
- **Complete Coverage**: Monitors all 26 possible traditional weekend dates  
- **Smart Scheduling**: 7 runs over 30 days (182 API calls, 84% quota usage)
- **Email Reports**: Beautiful HTML reports with price analysis and trends
- **Automated Backups**: JSON data stored as GitHub artifacts
- **Quota Efficient**: Uses only 10.4% of monthly SerpApi quota per complete scan

### 📅 Monitoring Schedule

The system runs on an optimized schedule to maximize market insights:

1. **Sept 17** - Baseline market scan
2. **Sept 23** - Early trend detection  
3. **Sept 26** - Early trend detection
4. **Oct 2** - Market trend monitoring
5. **Oct 8** - Peak season preparation
6. **Oct 13** - Peak season preparation
7. **Oct 17** - Final month analysis

## 🚀 Quick Setup

### 1. Create GitHub Repository

```bash
# Clone or fork this repository
git clone <your-repo-url>
cd flight_checker

# Or create new repository from these files
```

### 2. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these **Repository Secrets**:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `SERPAPI_KEY` | Your SerpApi API key | `6357aac8ff54c20e778...` |
| `EMAIL_USER` | Gmail address for sending reports | `your.email@gmail.com` |
| `EMAIL_PASS` | Gmail app password (not regular password) | `abcd efgh ijkl mnop` |
| `EMAIL_TO` | Email address to receive reports | `recipient@email.com` |

### 3. Set Up Gmail App Password

1. Enable 2-Factor Authentication on your Gmail account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate an app password for "Mail"
4. Use this 16-character password as `EMAIL_PASS` secret

### 4. Deploy and Test

```bash
# Push your code to GitHub
git add .
git commit -m "Set up automated flight monitoring"
git push origin main

# Test with manual run
# Go to Actions tab → Smart Flight Monitoring → Run workflow
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
