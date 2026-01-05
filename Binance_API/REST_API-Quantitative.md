# Binance API Quantitative Trading Project Report

**Project Name:** Binance REST API Quantitative Trading System  
**Report Date:** January 5, 2026  
**Project Status:** In Progress

---

## Project Overview

This project leverages the Binance official REST API for digital asset quantitative trading research. The current phase focuses on acquiring and processing historical trading data to prepare for subsequent strategy development and backtesting.

---

## Current Task Description

### Primary Objective

Retrieve complete trading data for the **BTC/USDT trading pair** over the **past 24 hours** from Binance API for quantitative analysis and strategy research.

### Technical Implementation

-   **API Endpoint:** `https://api.binance.com/api/v3/klines`
-   **Trading Pair:** BTCUSDT
-   **Time Interval:** 1-minute candles (1m)
-   **Data Range:** Past 24 hours
-   **Data Granularity:** Each candle contains up to 1000 trades (default limit)

---

## Data Acquisition Solution

### Technology Stack

| Component | Version/Description        |
| --------- | -------------------------- |
| Python    | 3.13                       |
| requests  | HTTP request library       |
| pandas    | Data processing & analysis |
| IDE       | PyCharm                    |

### Data Fetching Workflow

```
1. Initialize time range
   ├─ Current time (milliseconds): current_end
   └─ 24 hours ago (milliseconds): start_time

2. Fetch data in chunks (loop)
   ├─ Construct API request URL
   │  └─ startTime + endTime + limit=1000
   ├─ Send HTTP GET request
   ├─ Parse JSON response
   └─ Store in memory (all_data)

3. Data processing
   ├─ Convert to Pandas DataFrame
   ├─ Add column labels
   └─ Type conversion (string → numeric)

4. Data export
   └─ Save as CSV file
```

---

## Candlestick Data Structure

Each candle contains the following 11 fields:

| Index | Field Name         | Data Type | Description                          |
| ----- | ------------------ | --------- | ------------------------------------ |
| 0     | open_time          | Integer   | Opening time (millisecond timestamp) |
| 1     | open_price         | String    | Opening price (USDT)                 |
| 2     | high_price         | String    | Highest price (USDT)                 |
| 3     | low_price          | String    | Lowest price (USDT)                  |
| 4     | close_price        | String    | Closing price (USDT)                 |
| 5     | volume             | String    | Trading volume (BTC)                 |
| 6     | close_time         | Integer   | Closing time (millisecond timestamp) |
| 7     | quote_asset_volume | String    | Trading amount (USDT)                |
| 8     | trades             | Integer   | Number of trades                     |
| 9     | taker_base_volume  | String    | Taker buy base volume                |
| 10    | taker_quote_volume | String    | Taker buy quote volume               |
| 11    | ignore             | Integer   | Ignored field                        |

---

## Core Code Explanation

### Time Calculation

```python
current_end = int(time.time() * 1000)  # Current time (milliseconds)
start_time = int(current_end - 24 * 60 * 60 * 1000)  # 24 hours ago
```

### Chunked Data Retrieval

```python
current_start = start_time
while current_start < current_end:
    # Construct URL and request
    response = requests.get(url)
    data = response.json()

    if not data:
        print("No more data available")
        break

    all_data.extend(data)
    print(f"Fetched {len(data)} records")

    # Update start time: use previous batch's last close time + 1 millisecond
    current_start = data[-1][6] + 1
    time.sleep(0.5)
```

### Data Type Conversion & Storage

```python
if all_data:
    df = pd.DataFrame(all_data, columns=[...])

    # Convert string columns to numeric types
    df['open_price'] = pd.to_numeric(df['open_price'])
    df['close_price'] = pd.to_numeric(df['close_price'])
    df['volume'] = pd.to_numeric(df['volume'])
    df['trades'] = pd.to_numeric(df['trades'])

    # Calculate statistics
    print(f"Price range: {df['low_price'].min()} - {df['high_price'].max()}")

    df.to_csv('btc_1day_data.csv', index=False)
else:
    print("No data fetched")
```

---

## Output Data Example

### Data Statistics

-   **Total Records:** 1440 candles (theoretical: 24 hours × 60 minutes = 1440 1-minute candles)
-   **Total Trades:** Millions of trades
-   **Price Range:** Varies based on market volatility

### Output File

-   **Filename:** `btc_1day_data.csv`
-   **Format:** CSV format containing all candlestick data and indicators
-   **Usage:** For subsequent strategy analysis and backtesting

---

## Technical Details

### API Limits & Optimization

-   **Request Frequency:** 0.5-second interval between requests to avoid rate limiting
-   **Single Fetch Limit:** limit=1000 (maximum 1000 candles per request)
-   **Data Integrity:** Recursive retrieval ensures continuous and non-duplicative data

### Error Handling

-   SSL/Network connection timeout (timeout=15 seconds)
-   Retry mechanism (maximum 5 retries)
-   Exception logging

---

## Future Plans

### Short-term Goals

-   [ ] Achieve stable acquisition of 24-hour candlestick data
-   [ ] Data quality validation and cleaning
-   [ ] Basic statistical analysis (price volatility, trading volume, etc.)

### Medium-term Goals

-   [ ] Expand data acquisition scope (multiple trading pairs, longer time periods)
-   [ ] Develop quantitative strategy models
-   [ ] Implement historical backtesting functionality

### Long-term Goals

-   [ ] Real-time data acquisition and dynamic updates
-   [ ] Automated strategy execution
-   [ ] Risk management and position sizing

---

## Environment Configuration

### Python Dependencies

```
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
```

### Installation Command

```bash
pip install requests pandas numpy
```

---

## Important Notes

1. **API Key Security** - Safeguard API keys when using authenticated endpoints
2. **Rate Limiting** - Comply with Binance API request frequency limits
3. **Data Precision** - Price data is returned as strings and must be converted to numeric format for calculations
4. **Timezone** - All timestamps are in UTC (millisecond precision)

---

**Document Version:** v1.0  
**Last Updated:** January 5, 2026
