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
end_time = int(time.time() * 1000)  # Current time in milliseconds
# Start time: 1 day ago
start_time = int(end_time - 24 * 60 * 60 * 1000)

# Store all data
all_data = []

# Fetch data in chunks
current_start = start_time
while current_start < end_time:
    # Build URL with correct parameters: startTime and endTime
    url = (BASE_URL + '/api/v3/klines?' +
           'symbol=BTCUSDT&interval=1m&limit=' + str(limit) +
           '&startTime=' + str(current_start) +
           '&endTime=' + str(end_time))

    # print(f"Fetching data from {current_start} to {end_time}...")
    response = requests.get(url)
    data = response.json()

    # Break if no more data
    if not data:
        break

    # Add data to list
    all_data.extend(data)

    # Update start_time for next iteration (move forward)
    # The last candle's close time becomes the next start time
    current_start = data[-1][6] + 1  # close_time is at index 6

    # Add small delay to avoid rate limiting
    time.sleep(0.1)

# Create DataFrame with proper column names
df = pd.DataFrame(all_data, columns=['open_time', 'open_price', 'high_price', 'low_price',
                                     'close_price', 'volume', 'close_time', 'quote_asset_volume',
                                     'trades', 'taker_base_volume', 'taker_quote_volume', 'ignore'])

print(df)
print(f"Total records: {len(df)}")
print(f"Total trades: {df['trades'].sum()}")

# Save to CSV
df.to_csv('btc_1day_data.csv', index=False)
print("Data saved to btc_1day_data.csv")