# Binance Futures Trading Bot

A Python CLI trading bot for Binance USDT-M Futures demo environment.
Supports MARKET, LIMIT, and STOP_MARKET orders with full validation,
structured logging, and clean error handling.

## Project Structure
## Setup

1. Clone the repo
2. Create virtual environment:
   python -m venv venv
   venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Add your API keys to config.py:
   API_KEY = "your_key"
   API_SECRET = "your_secret"

Get API keys from: https://demo.binance.com/en/my/settings/api-management

## How to Run

### MARKET order
python cli.py market --symbol BTCUSDT --side BUY --quantity 0.001
### LIMIT order
python cli.py limit --symbol BTCUSDT --side BUY --quantity 0.001 --price 60000
### STOP_MARKET order (bonus)
python cli.py stop --symbol BTCUSDT --side SELL --quantity 0.001 --stop-price 50000
### Get help
python cli.py --help
python cli.py market --help

