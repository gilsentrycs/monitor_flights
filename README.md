# ✈️ Automated Flight Monitor

**Get email alerts for the best flight deals on any route. Fork, configure, and deploy in 5 minutes.**

## 🎯 What You Get

- **📧 Automated email reports** every 4 days with the best flight deals
- **📊 Price analysis** - trends, monthly breakdown, market insights
- **🤖 GitHub Actions** - runs automatically, no maintenance needed
- **🌍 Any route** - just change 4 lines in the config file
- **💾 Data backup** - complete flight data stored as artifacts

## 🚀 Quick Setup (4 Steps)

### 1. Fork This Repository
Click the "Fork" button at the top of this page to get your own copy.

### 2. Edit Your Route
Edit the `config.env` file with your desired route:

```env
# Change these 4 lines for your route:
DEPARTURE_CITY="Tel Aviv"
DEPARTURE_CODE="TLV"
ARRIVAL_CITY="Paris"
ARRIVAL_CODES="CDG,ORY"

# Customize your travel preferences:
START_MONTH=4    # April
END_MONTH=6      # June
DEPARTURE_DAYS="2,3"  # Wednesday, Thursday (0=Mon, 1=Tue, etc.)
TRIP_DURATION_DAYS=4  # 4-day trips
```

### 3. Add Your API Credentials
Go to **Settings → Secrets and Variables → Actions** in your forked repository.

Add these 4 secrets:

| Secret Name | Value | Get It From |
|-------------|-------|-------------|
| `SERPAPI_KEY` | Your SerpApi API key | [serpapi.com](https://serpapi.com/users/sign_up) (free 100 searches/month) |
| `EMAIL_USER` | Your Gmail address | Your Gmail account |
| `EMAIL_PASS` | Gmail app password | [Google App Passwords](https://myaccount.google.com/apppasswords) |
| `EMAIL_TO` | Where to send reports | Any email address |

**Gmail Setup:** Enable 2-factor auth, then generate an app password (not your regular password).

### 4. Deploy
```bash
git add config.env
git commit -m "Configure for my route"
git push
```

**Done!** Your flight monitor starts automatically.

## 📧 What You'll Receive

Beautiful HTML email reports every 4 days with:

- **🏆 Top 5 Best Deals** - prices, airlines, flight times
- **📊 Executive Summary** - average prices, total options found
- **📅 Monthly Breakdown** - price trends by month  
- **📈 Market Insights** - price ranges, direct flights availability
- **📎 JSON Data** - complete flight information for analysis

## 🔧 Route Examples

**European Weekend:**
```env
DEPARTURE_CITY="London"
DEPARTURE_CODE="LHR"
ARRIVAL_CITY="Barcelona"
ARRIVAL_CODES="BCN"
DEPARTURE_DAYS="4,5"  # Friday, Saturday
TRIP_DURATION_DAYS=3
```

**US Cross-Country:**
```env
DEPARTURE_CITY="New York"
DEPARTURE_CODE="JFK"
ARRIVAL_CITY="Los Angeles"
ARRIVAL_CODES="LAX"
DEPARTURE_DAYS="0,1,2,3,4"  # Weekdays
TRIP_DURATION_DAYS=5
```

**Asian Adventure:**
```env
DEPARTURE_CITY="Tokyo"
DEPARTURE_CODE="NRT"
ARRIVAL_CITY="Bangkok"
ARRIVAL_CODES="BKK,DMK"
DEPARTURE_DAYS="5,6"  # Weekend departures
TRIP_DURATION_DAYS=7
```

## 📊 API Usage & Costs

- **Free SerpApi**: 100 searches/month (3-4 complete scans)
- **Paid Plans**: 250+ searches/month (7+ complete scans)
- **Typical Usage**: ~26 searches per scan
- **Auto Schedule**: 7 scans per month (efficient quota usage)

## ✅ Test Your Setup

Before deploying, validate your configuration:
```bash
python validate_config.py
```

This checks your route settings and estimates API usage.

## 🔍 Monitor Your System

- **Actions Tab**: See automated runs and logs
- **Email Reports**: Arrive every 4 days automatically  
- **Manual Runs**: Trigger anytime via "Run workflow"
- **Data Backups**: Download JSON files from Actions artifacts

## 🚨 Troubleshooting

**No email received?**
- Check spam/junk folder
- Verify Gmail app password (not regular password)
- Ensure 2-factor auth is enabled

**GitHub Actions failing?**
- Check all 4 secrets are set correctly
- Verify SerpApi key has remaining quota
- Test with manual workflow trigger

**No flights found?**
- Verify airport codes are correct
- Check if dates are too far in future
- Ensure route actually exists

## 🎯 Project Files

- `automated_flight_monitor.py` - Main monitoring script
- `config.env` - **Edit this** for your route
- `.github/workflows/flight-monitor.yml` - Automated scheduling
- `validate_config.py` - Test your configuration
- `requirements.txt` - Python dependencies

**You only need to edit `config.env` - everything else works automatically.**

## 📈 Next Steps

1. **🍴 Fork** this repository
2. **⚙️ Edit** `config.env` with your route
3. **🔐 Add** your 4 GitHub secrets
4. **🚀 Push** to start monitoring
5. **📧 Enjoy** automated flight deal alerts!

---

**Happy flight hunting!** ✈️🗺️

*This project is open source and community-friendly. Your API credentials stay private even in public repositories.*
