import alpaca_trade_api as tradeapi

# Replace with your API key
API_KEY = 'PKANIBNBXL65CBQWKYE5FNNTU2'
SECRET_KEY = 'Eaj8vevLiYgMKMACVQtVxrQLUe13KuViGnz9AtTcWqgZ'
BASE_URL = 'https://paper-api.alpaca.markets' # This is the address of Paper Trading.

# Initialize API Client
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL, api_version='v2' )

try:
    # call get_account()
    account = api.get_account()

    # Print account's information
    print("--- Account Info ---")
    print(f"Account ID: {account.id}")
    print(f"Account Number: {account.account_number}")
    print(f"Account Status: {account.status}")
    print(f"Purchasing Power: ${account.buying_power}")
    print(f"Net Asset Value: ${account.equity}")
    print("--------------------")

    # Verification returned account number
    if account.account_number == 'PA372OJ134YU':
        print("\nVerification successful! You have connected to your Paper account via API.")
    else:
        print("\nVerification failed. Please check your API key or account number.")

except Exception as e:
    print(f"Connection failed, an error occurred: {e}")
