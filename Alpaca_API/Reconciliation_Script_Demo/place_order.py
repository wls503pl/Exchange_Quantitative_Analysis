import alpaca_trade_api as tradeapi
import time

# --- Configuration ---
API_KEY = 'PKANIBNBXL65CBQWKYE5FNNTU2'
SECRET_KEY = 'Eaj8vevLiYgMKMACVQtVxrQLUe13KuViGnz9AtTcWqgZ'
BASE_URL = 'https://paper-api.alpaca.markets'

# --- Initialize API ---
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL, api_version='v2' )

# --- Order Parameters ---
symbol = 'BTC/USD'   # Trading Pairs: Bitcoin vs. US Dollar
qty = 0.01           # Quantity: 0.01 Bitcoin purchased
side = 'buy'         # Direction: 'buy' or 'sell'
order_type = 'market'# Type: 'market' (market order)
time_in_force = 'gtc'# Valid until: 'gtc' (Good 'til Canceled - Valid until cancellation)

try:
    # --- Submit an order ---
    print(f"Submitting a transaction for account {api.get_account().account_number}...")
    print(f"Order details: {side} {qty} {symbol} ({order_type})")
    
    order = api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=order_type,
        time_in_force=time_in_force
    )

    print("\n--- Order submitted, awaiting completion. ---")
    print(f"Order ID: {order.id}")
    print(f"Initial state: {order.status}")
    
    # --- Wait and confirm order status ---
    # In a simulated environment, market orders are usually executed very quickly.
    time.sleep(5) # Wait 5 seconds to allow the system time to process.

    filled_order = api.get_order(order.id)
    
    print("\n--- Get the final order status in 5 seconds. ---")
    print(f"Order ID: {filled_order.id}")
    print(f"Final state: {filled_order.status}")

    if filled_order.status == 'filled':
        print(f"The order has been successfully completed!")
        print(f"Transaction volume:{filled_order.filled_qty} {symbol.split('/')[0]}")
        print(f"Average transaction price:${filled_order.filled_avg_price}")
        print("\nYour account should now show a new transaction record and BTC holding.")
    else:
        print(f"The order was not fulfilled; its current status is {filled_order.status}. Subsequent reconciliation scripts may not be able to find the data.")

except Exception as e:
    print(f"\nOrder submission failed, error: {e}")
    print("Please check:")
    print("1. Is the API key correct?")
    print("2. Does the account have sufficient purchasing power?")
    print(f"3. Whether the trading pair {symbol} is supported.")