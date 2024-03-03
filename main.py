import json
import requests
# from covalent import CovalentClient

config = json.load(open("params.json"))
apiKey = config["covalentAPIKey"]
wallet = config["metaMaskWallet"]
chains = {
    "Eth": "1",
    "Polygon": "137",
    "BSC": "56",
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
        print(data[crypto_id]['usd'])
        return data[crypto_id]['usd']
    else:
        return None

def getBalances(chain):
    url = f"https://api.covalenthq.com/v1/{chain}/address/{wallet}/balances_v2/?key={apiKey}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data']
        items = data['items']
        # print(items)
        for item in items:
            balance_raw = item['balance']
            if int(balance_raw) < 0.1:
                break
            contract_name = item.get('contract_name', 'N/A')
            ticker_symbol = item.get('contract_ticker_symbol', 'N/A')
            contract_decimals = item['contract_decimals']
            balance = int(balance_raw) / 10 ** contract_decimals
            quote = item.get('quote',0.0)

            formatted_quote = f"${quote:.2f}" if quote is not None else "N/A"
            print(f"Asset ({chain}): {contract_name} ({ticker_symbol}), Balance: {balance}, Value: {formatted_quote}")
    else:
        print("Failed to fetch data")

if __name__ == "__main__":
    # getBalances(chains["Eth"])
    # getBalances(chains["Polygon"])
    # getBalances(chains["BSC"])
    getCryptoPrice("btc")