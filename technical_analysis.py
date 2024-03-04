import json
import requests
from datetime import datetime

LOGGING_FREQUENCY = "5T"  #every 5 minutes
ANALYSIS_FREQUENCY = "1H"  #every hour

#HISTORICAL DUMMY DATA
def fetch_historical_data(crypto_id, days): #real historical data just for dummy data testing purposes
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days={days}&interval=daily"
    response = requests.get(url)
    if response.status_code == 200:
        prices = response.json()['prices']
        return [(datetime.fromtimestamp(price[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'), price[1]) for price in prices]
    else:
        return None

def log_historical_data(): #real historical data
    btc_data = fetch_historical_data('bitcoin', 200)
    eth_data = fetch_historical_data('ethereum', 200)

    # Combine into one list of dictionaries
    combined_data = []
    for i in range(len(btc_data)):
        entry = {
            "timestamp": btc_data[i][0],
            "data": {
                "bitcoin": {"usd": btc_data[i][1]},
                "ethereum": {"usd": eth_data[i][1]}
            }
        }
        combined_data.append(entry)

    file_path = 'logs/real_historical_prices_log.json'
    with open(file_path, 'w') as f:
        for entry in combined_data:
            f.write(json.dumps(entry) + '\n')

#MOVING AVERAGES
def calculate_moving_average(prices, window_size):
    """Calculate the moving average for the given list of prices and window size."""
    if len(prices) < window_size:
        return []  # Not enough data
    return [sum(prices[i:i+window_size]) / window_size for i in range(len(prices) - window_size + 1)]

def moving_average_crossover_signals(prices, short_window, long_window):
    """Determine buy/sell signals based on moving average crossovers."""
    short_ma = calculate_moving_average(prices, short_window)
    long_ma = calculate_moving_average(prices, long_window)
    
    # Ensure both MAs are of the same length for comparison
    length_difference = len(short_ma) - len(long_ma)
    if length_difference > 0:
        short_ma = short_ma[length_difference:]
    elif length_difference < 0:
        long_ma = long_ma[-length_difference:]
    
    signals = []
    for i in range(1, len(short_ma)):
        if short_ma[i] > long_ma[i] and short_ma[i-1] <= long_ma[i-1]:
            signals.append(('buy', i + long_window - 1))  # Buy signal
        elif short_ma[i] < long_ma[i] and short_ma[i-1] >= long_ma[i-1]:
            signals.append(('sell', i + long_window - 1))  # Sell signal
    return signals


#HISTORICAL PRICES LOADING FROM PRICES_LOG.JSON
def load_historical_prices(file_path, crypto):
    prices = []
    with open(file_path, 'r') as file:
        for line in file:
            entry = json.loads(line)
            # Extract the price for the specified cryptocurrency
            price = entry['data'][crypto]['usd'] if crypto in entry['data'] else None
            if price is not None:
                prices.append(price)
    return prices

def logCryptoPrices(crypto_ids):
    ids = ','.join(crypto_ids)
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {"timestamp": timestamp, "data": data}
        with open("logs/prices_log.json", "a") as log_file:
            json.dump(log_entry, log_file)
            log_file.write('\n')  # Ensure each log entry is on a new line
    except requests.exceptions.HTTPError as http_e:
        error_message = f"HTTP error occurred: {http_e}"
        print(error_message)
        # logError(error_message)
    except Exception as e:
        error_message = f"Other error occurred: {e}"
        print(error_message)
        # logError(error_message)

