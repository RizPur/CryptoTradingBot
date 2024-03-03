import json

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

#HISTORICAL PRICES
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

