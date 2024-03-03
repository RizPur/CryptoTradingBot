import json
import requests
import random
# from covalent import CovalentClient

config = json.load(open("params.json"))
apiKey = config["covalentAPIKey"]
wallet = config["metaMaskWallet"]
chains = {
    "eth": "1",
    "polygon": "137",
    "bsc": "56",
}

def getCryptoPrice(crypto):
    cryptos = {
        "btc" : "bitcoin",
        "eth" : "ethereum"
    }
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
    # getBalances(chains["eth"])
    # getBalances(chains["Polygon"])
    # getBalances(chains["BSC"])
    # getCryptoPrice("btc")
    try:
        # getCryptoPrice("eth")
        simultateTrade()
    except Exception as e:
        print(f"Error:{e}")