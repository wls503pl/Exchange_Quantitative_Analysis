# Import the requests library to make HTTP requests
import requests
# Import the time module for time-related operations
import time
# Import pandas library and alias it as pd for data manipulation
import pandas as pd

# Configure pandas to display DataFrames without line wrapping
pd.set_option('expand_frame_repr', False)

# Define the base URL for Binance API
BASE_URL = 'https://api.binance.com'

# Get Binance's transaction data for the past day
limit = 1000  # Max records per request
current_end = int(time.time() * 1000)  # Current time in milliseconds
start_time = int(current_end - 24 * 60 * 60 * 1000)  # Start time: 1 day ago

# Store all data
all_data = []

# Fetch data in chunks - from past to present
current_start = start_time
while current_start < current_end:
    # Build URL with correct parameters: startTime and endTime
    url = (BASE_URL + '/api/v3/klines?' +
           'symbol=BTCUSDT&interval=1m&limit=' + str(limit) +
           '&startTime=' + str(current_start) +
           '&endTime=' + str(current_end))

    print(f"Fetching data from {current_start} to {current_end}...")
    response = requests.get(url)
    data = response.json()

    # Break if no more data
    if not data:
        print("No more data available")
        break

    # Add data to list
    all_data.extend(data)
    print(f"Fetched {len(data)} records")

    # Update start_time for next iteration (move forward)
    # The last candle's close time becomes the next start time
    current_start = data[-1][6] + 1  # close_time is at index 6

    # Add small delay to avoid rate limiting
    time.sleep(0.5)

# Create DataFrame with proper column names
if all_data:
    df = pd.DataFrame(all_data, columns=['open_time', 'open_price', 'high_price', 'low_price',
                                         'close_price', 'volume', 'close_time', 'quote_asset_volume',
                                         'trades', 'taker_base_volume', 'taker_quote_volume', 'ignore'])

    # Convert columns to numeric types
    df['open_price'] = pd.to_numeric(df['open_price'])
    df['close_price'] = pd.to_numeric(df['close_price'])
    df['volume'] = pd.to_numeric(df['volume'])
    df['trades'] = pd.to_numeric(df['trades'])

    print("\n" + "="*60)
    print(df)
    print("="*60)
    print(f"Total records: {len(df)}")
    print(f"Total trades: {int(df['trades'].sum())}")
    print(f"Price range: {df['low_price'].min()} - {df['high_price'].max()}")

    # Save to CSV
    df.to_csv('btc_1day_data.csv', index=False)
    print("Data saved to btc_1day_data.csv")
else:
    print("No data fetched")