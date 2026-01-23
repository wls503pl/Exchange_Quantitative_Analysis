import alpaca_trade_api as tradeapi
import random # Use it to simulate on-chain data

# --- Configuration ---
API_KEY = 'PKANIBNBXL65CBQWKYE5FNNTU2'
SECRET_KEY = 'Eaj8vevLiYgMKMACVQtVxrQLUe13KuViGnz9AtTcWqgZ'
BASE_URL = 'https://paper-api.alpaca.markets'
# 
MOCK_CHAIN_WALLET_ADDRESS = 'mock_paper_btc_address_from_error_67890' 

# --- Initialize API ---
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL, api_version='v2' )

def get_alpaca_data():
    """Retrieving ledger data from the Alpaca API"""
    print("\n--- 1. Retrieving data from the Alpaca API ---")
    try:
        # Get the latest transaction activity (let's assume it's the order we just placed).
        activities = api.get_activities(activity_types='FILL', direction='desc', page_size=1)
        if not activities:
            print("Error: No transaction activity was found in Alpaca.")
            return None, None
        
        last_trade = activities[0]
        print(f"Find the latest transaction record (ID: {last_trade.id})")
        print(f"Transaction assets: {last_trade.symbol}, Amount: {last_trade.qty}, Price: {last_trade.price}")

        # Get current BTC holdings
        account_info = api.get_account()
        btc_balance_from_activity = float(last_trade.qty)
        print(f"Based on the latest transaction history, the current BTC balance should be: {btc_balance_from_activity} BTC")

        class MockPosition:
            def __init__(self, qty):
                self.qty = qty

        btc_position = MockPosition(btc_balance_from_activity)
        
        return last_trade, btc_position

    except Exception as e:
        # Handling situations where there may be no BTC holdings.
        if "position not found" in str(e):
            print("The Alpaca account currently has no BTC holdings.")
            return last_trade, None
        print(f"Error retrieving data from Alpaca: {e}")
        return None, None

def get_mock_onchain_data(expected_qty):
    """Simulate retrieving data from blockchain explorers (such as Etherscan, Blockchain.com)."""
    print(f"\n--- 2. Simulating a query of an address on the blockchain: {MOCK_CHAIN_WALLET_ADDRESS} ---")
    
    # Simulate API call latency
    print("...")
    
    # Simulate potential on-chain discrepancies (such as network latency or errors).
    # It returns the correct data with a 90% probability, and a slightly different data with a 10% probability.
    if random.random() < 0.9:
        mock_balance = float(expected_qty)
        print("On-chain query successful!")
    else:
        mock_balance = float(expected_qty) * 0.99 # Simulate a 1% error
        print("Warning: Minor differences were found in the simulated on-chain query!")

    print(f"The on-chain address balance was found to be: {mock_balance} BTC.")
    return mock_balance

def run_reconciliation():
    """Perform reconciliation process"""
    # Part 1: Obtaining Data from Alpaca
    last_trade, btc_position = get_alpaca_data()

    if btc_position is None:
        print("\nReconciliation suspended: Unable to obtain Alpaca holdings information.")
        return

    # Part 2: Simulating On-Chain Queries
    # We expect the on-chain balance to equal the Alpaca holdings.
    expected_onchain_balance = btc_position.qty
    actual_onchain_balance = get_mock_onchain_data(expected_onchain_balance)

    # Part Three: Comparison and Report
    print("\n--- 3. Start reconciliation ---")
    alpaca_balance = float(btc_position.qty)

    print(f"Alpaca internal ledger balance: {alpaca_balance} BTC")
    print(f"Simulated on-chain balance: {actual_onchain_balance} BTC")

    # Comparison of differences
    discrepancy = abs(alpaca_balance - actual_onchain_balance)
    
    # Set a very small tolerance threshold to prevent floating-point calculation problems.
    if discrepancy < 0.00000001:
        print("\nReconciliation successful! Alpaca's internal ledger is consistent with its on-chain balance.")
    else:
        print(f"\nReconciliation failed! Discrepancy detected: {discrepancy:.8f} BTC")
        print("Recommended action: Immediately initiate the exception handling procedure (SOP) and conduct a manual investigation.")
        print(f"Investigative clues: Alpaca's latest transaction ID is '{last_trade.id}', and its wallet address is '{MOCK_CHAIN_WALLET_ADDRESS}'.")

# --- Run the main program ---
if __name__ == "__main__":
    run_reconciliation()
