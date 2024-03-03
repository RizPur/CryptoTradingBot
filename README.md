# Crypto Trading Bot Simulation :robot:

This project is a simple simulation of a crypto trading bot written in Python. It utilizes the Covalent API to fetch balances from different chains (Ethereum, Polygon, BSC) and the CoinGecko API to get current crypto prices for Ethereum (ETH) and Bitcoin (BTC). Based on the fetched balances and prices, it simulates trading decisions (buy/sell) and logs the outcomes.

## Features :star:

- Fetches current balances of USDT across Ethereum, Polygon, and BSC.
- Retrieves current prices for ETH and BTC.
- Simulates trading decisions based on predefined conditions.
- Logs buy/sell actions and updates the virtual USDT balance accordingly.

## Setup :gear:

1. **Clone the repository**

    ```bash
    git clone <repository-url>
    cd crypto-trade
    ```

2. **Install dependencies**

    First, ensure you have Python and `pip` installed. Then, set up a virtual environment and install the required packages:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Configuration**

    Create a `params.json` file in the root directory with your Covalent API key and MetaMask wallet address:

    ```json
    {
      "covalentAPIKey": "your_covalent_api_key_here",
      "metaMaskWallet": "your_metamask_wallet_address_here"
    }
    ```

## Usage :rocket:

To run the simulation, execute the `main.py` script:

```bash
python main.py
