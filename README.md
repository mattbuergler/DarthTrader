# Darth Trader

A lightweight Python script that interacts with the [Crypto.com Exchange API](https://exchange-docs.crypto.com/) to automate basic cryptocurrency trading operations. This script demonstrates how to:

- Fetch market data (tickers, candlesticks).  
- Retrieve and print account balances.  
- Place simple limit buy and sell orders.  
- Manage open orders.

> **Disclaimer**: This code is for educational purposes only. Use at your own risk. Trading cryptocurrencies involves significant risk of loss.

---

## Features

1. **Market Data Retrieval**  
   - Public GET requests to fetch instruments, tickers, and candlestick data (`getInstruments`, `getTicker`, `getCandleSticks`, etc.).

2. **Authenticated Trading**  
   - Private POST requests (using HMAC signatures) to place orders, get account summaries, and retrieve open or historical orders (`createOrder`, `getOpenOders`, `getOderHistory`, etc.).

3. **Automated Workflow** (Commented Out)  
   - The example code includes a `run()` function (currently commented out) that can loop through buy/sell operations over a specified duration.

4. **Simple Wallet Class**  
   - Manages available balances and places limit orders (`Wallet.placeLimitBuyOrder` / `Wallet.placeLimitSellOrder`).

---

## Requirements

- **Python 3.x**
- [requests](https://pypi.org/project/requests/)  
- [numpy](https://pypi.org/project/numpy/)

Install dependencies (for example, using `pip`):

```bash
pip install requests numpy
```

## Repository Structure

```graphql
.
├── misc
│   └── run
│       ├── Dockerfile       # Docker configuration for containerizing the app
│       ├── recreate.sh      # Script to rebuild or recreate Docker containers
│       └── start.sh         # Script to start the Docker container/application
├── src
│   └── darthTrader.py      # Main Python trading script
├── userData
│   └── api_template.txt    # Template file for API credentials (rename to api.txt for actual use)
├── .gitignore               # Specifies intentionally untracked files (e.g., secrets)
└── README.md                # Main project documentation
```

> **Note**: The code references an `api.txt` file in `../userData/api.txt`.  
> Make sure you do **not** commit your private API keys to version control.

---

## Setup and Usage

1. **Obtain API Keys**  
   - Generate your API Key and Secret Key from your [Crypto.com Exchange](https://crypto.com/exchange) account settings.

2. **Store Keys in `api.txt`**  
   Create a file named `api.txt` in a separate (and **private**) `userData` folder.  
   It should look something like:


```php
API_KEY  <YOUR_PUBLIC_KEY>
SECRET_KEY  <YOUR_SECRET_KEY>
```
The script will read this file to authenticate private endpoints.

3. **Configure Script Parameters**  
- At the bottom of `darth_trader.py`, in the `if __name__ == "__main__":` section, you’ll find settings such as:
  - `instrument = "DAI_CRO"`  
  - `min_trading_cost = 0.0`  
  - `maxInitPrice = 5.6`  
  - `mainInitTradingQuantity = 100`  
  - …and more.

Adjust these values to suit your needs, including your desired trading pairs and thresholds.

4. **Run the Script**  
- By default, the main trading loop (`run(...)`) is commented out.  
- Uncomment the `run(...)` line (in the `if __name__ == "__main__":` section) if you want the bot to **actually place orders**.
- Execute from the command line:
  ```bash
  python3 darth_trader.py
  ```
- **Important**: This will attempt real trades against the Crypto.com Exchange if you have uncommented the `run()` function.

5. **Dry Run / Testing**  
- To avoid placing real orders, keep the `run(...)` call commented out. You can still call or modify individual functions (e.g., `getTicker`, `getCandleSticks`) for testing.

---

## Security & Disclaimer

- **API Key Safety**: Never commit `api.txt` (or any file containing private credentials) to a public repository. Always place it in `.gitignore`.  
- **Use at Your Own Risk**: Cryptocurrency trading is inherently risky. This script is provided for educational purposes only.  
- **No Guarantees**: There’s no guarantee of profit or protection from losses.

---

## Contributing

1. **Fork** the repository.  
2. **Create** a new feature branch (`git checkout -b feature-name`).  
3. **Commit** your changes (`git commit -m 'Add some feature'`).  
4. **Push** to the branch (`git push origin feature-name`).  
5. **Create** a new Pull Request on GitHub.

---

## License

This project is published under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE` file for details. You are free to use and modify this code as long as you include the original license information.


Happy Trading! If you have any questions or run into issues, feel free to open an issue or pull request.
