import schedule
import time
from technical_analysis import logCryptoPrices

def logPricesJob():
    crypto_ids = ['bitcoin', 'ethereum']
    logCryptoPrices(crypto_ids)
    print(f"Logged prices at {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Schedule the job every 5 minutes
schedule.every(5).minutes.do(logPricesJob)

if __name__ == "__main__":
    print("Starting price logging scheduler...")
    while True:
        schedule.run_pending()
        time.sleep(1)