import json
import requests
import random
import datetime
# from covalent import CovalentClient

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

def readNJsonLog(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield json.loads(line)

def logError(error_message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/errors_log.json", "a") as log_file:
        log_file.write(f"{timestamp} - {error_message}\n")

def getCryptoPrices(crypto_ids):
    # Join the crypto_ids into a comma-separated string for the API request
    ids = ','.join(crypto_ids)
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        data = response.json()
    except requests.exceptions.HTTPError as http_e:
        #HTTP errors
        error_message = f"HTTP error occurred: {http_e}"
        print(error_message)
        logError(error_message)
    except Exception as e:
        error_message = f"Other error occurred: {e}"
        # print(error_message)
        logError(error_message)
    else:
        # log data if no errs
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {"timestamp": timestamp, "data": data}

        with open("logs/prices_log.json", "a") as log_file:
            json.dump(log_entry, log_file)
            log_file.write('\n')

def getCryptoPrice(crypto):
    if crypto.lower() in cryptos:
        crypto_id = cryptos[crypto.lower()]
        url =f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd'
        response = requests.get(url)
        data = response.json()
        # print(data)
        # print(data[crypto_id]['usd'])
        return data[crypto_id]['usd']
    else:
        return None

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

def simultateTrade():
    usdt_polygon = getBalances(chains["polygon"])
    # print(usdt_polygon)
    usdt_bsc = getBalances(chains["bsc"])
    usdt_balance = 0
    for obj in usdt_polygon:
        if obj['ticker_symbol'] == "USDT":
            usdt_balance += obj['balance']
    for obj in usdt_bsc:
        if obj['ticker_symbol'] == "USDT":
            usdt_balance += obj['balance']
    # print(usdt_balance)
    
    eth_price = getCryptoPrice("eth")
    btc_price = getCryptoPrice("btc")

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


if __name__ == "__main__":
    try:
        # getBalances(chains["eth"])
        # getBalances(chains["Polygon"])
        # getBalances(chains["BSC"])
        # getCryptoPrice("btc")
        # getCryptoPrice("eth")
        # simultateTrade()
        getCryptoPrices(["ethereum", "bitcoin"])
        # for log_entry in readNJsonLog("prices_log.json"):
        #     print(log_entry["timestamp"], log_entry["data"])
    except Exception as e:
        print(f"Error:{e}")