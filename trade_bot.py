import json
import requests
import random
import datetime
from technical_analysis import load_historical_prices, moving_average_crossover_signals
#run every hour to simulate trade

config = json.load(open("params.json"))
apiKey = config["covalentAPIKey"]
wallet = config["metaMaskWallet"]
chains = {
    "eth": "1",
    "polygon": "137",
    "bsc": "56", 
}
cryptos = {
    "btc" : "bitcoin",
    "eth" : "ethereum"
}

def logError(error_message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/errors_log.json", "a") as log_file:
        log_file.write(f"{timestamp} - {error_message}\n")

def getBalances(chain):
    url = f"https://api.covalenthq.com/v1/{chain}/address/{wallet}/balances_v2/?key={apiKey}"
    response = requests.get(url)
    if response.status_code == 200:
        balances = []
        data = response.json()['data']
        items = data['items']
        # print(items)
        for item in items:
            balance_raw = item['balance']
            if int(balance_raw) < 0.1:
                continue
            contract_name = item.get('contract_name', 'N/A')
            ticker_symbol = item.get('contract_ticker_symbol', 'N/A')
            contract_decimals = item['contract_decimals']
            balance = int(balance_raw) / 10 ** contract_decimals
            quote = item.get('quote',0.0)

            assets = {
                "chain" : chain,
                "contract_name": contract_name,
                "ticker_symbol": ticker_symbol,
                "balance": balance,
                "value": f"${quote:.2f}" if quote is not None else "N/A"
            }
            balances.append(assets)
            # formatted_quote = f"${quote:.2f}" if quote is not None else "N/A"
            # print(f"Asset ({chain}): {contract_name} ({ticker_symbol}), Balance: {balance}, Value: {formatted_quote}")
        return balances
    else:
        print("Failed to fetch data")
        return json.dumps({"error": "Failed to fetch data"})
    
def getPriceFromLog(crypto_id):
    try:
        with open("logs/prices_log.json", "r") as log_file:
            last_line = log_file.readlines()[-1]
            data = json.loads(last_line)
            print(data['data'][crypto_id]['usd'])
            return data['data'][crypto_id]['usd']
    except FileNotFoundError:
        print("Log file not found.")
        logError("Log file not found")
        return None
    except Exception as e:
        print(f"Error occurred while getting the current price: {e}")
        logError(f"Error occurred while getting the current price: {e}")
        return None

def getSMASignals():
    btc_prices = load_historical_prices("logs/prices_log.json", "bitcoin")
    eth_prices = load_historical_prices("logs/prices_log.json", "ethereum")

    # Define your short-term and long-term windows for SMAs
    short_window = 10  # This could represent a 10-period SMA, for example
    long_window = 50   # This could represent a 50-period SMA, for example

    # Calculate SMA crossover signals for BTC
    btc_signals = moving_average_crossover_signals(btc_prices, short_window, long_window)
    print("BTC Signals:", btc_signals)

    # Calculate SMA crossover signals for ETH
    eth_signals = moving_average_crossover_signals(eth_prices, short_window, long_window)
    print("ETH Signals:", eth_signals)

def simultateTrade():
    #get USDT balance
    usdt_polygon = getBalances(chains["polygon"])
    usdt_bsc = getBalances(chains["bsc"])
    usdt_balance = 0
    for obj in usdt_polygon:
        if obj['ticker_symbol'] == "USDT":
            usdt_balance += obj['balance']
    for obj in usdt_bsc:
        if obj['ticker_symbol'] == "USDT":
            usdt_balance += obj['balance']
    # print(usdt_balance)
    
    #get current prices
    eth_price = getPriceFromLog("ethereum")
    btc_price = getPriceFromLog("bitcoin")

    should_buy = random.choice([True, False])

    if should_buy and usdt_balance > 0:
        # Split USDT balance according to 0.6/0.4 for ETH/BTC
        eth_amount = (usdt_balance * 0.6) / eth_price
        btc_amount = (usdt_balance * 0.4) / btc_price
        usdt_balance = 0  # All USDT is converted
        
        print(f"Bought {eth_amount} ETH and {btc_amount} BTC.")
    elif not should_buy and usdt_balance == 0:
        # Simulate selling all holdings back to USDT at current prices
        usdt_balance += eth_amount * eth_price + btc_amount * btc_price
        
        print(f"Sold all holdings, new USDT balance: {usdt_balance}")
    else:
        print("No action taken.")

getPriceFromLog("ethereum")
getSMASignals()