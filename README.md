# Binance Futures Trading Bot 📈🤖

A real-time Python-based trading bot for Binance USDT-M Futures. This system
takes user input via an interactive menu or CLI, validates all parameters,
places MARKET / LIMIT / STOP_MARKET orders on Binance demo environment, and
logs every request and response — creating a clean, production-style trading
workflow.

## 🎯 Goal
Assist developers and traders in automating futures order placement by:

- Accepting and validating order parameters
- Placing real orders on Binance Futures demo environment
- Logging all activity with structured, readable logs

## 🧩 Key Technologies

| Component        | Tool Used                        |
|------------------|----------------------------------|
| Language         | Python 3.x                       |
| HTTP Client      | requests                         |
| Authentication   | HMAC-SHA256 signing              |
| CLI Interface    | argparse                         |
| Interactive Menu | Custom prompt loop (run.py)      |
| Logging          | Python logging (file + console)  |
| Exchange         | Binance USDT-M Futures Demo API  |

## 🔁 How It Works

### 📌 Architecture Overview
User Input (run.py / cli.py)
↓
bot/validators.py     ← validates symbol, side, qty, price
↓
bot/orders.py         ← builds correct API payload
↓
bot/client.py         ← signs request with HMAC-SHA256
↓
Binance Futures API   ← returns order confirmation
↓
Logs + Console Output

## 🛠️ Code Highlights

```python
# Validate and place a market order
r = place_market_order(client, 'BTCUSDT', 'BUY', '0.001')

# Validate and place a limit order
r = place_limit_order(client, 'BTCUSDT', 'BUY', '0.001', '60000')

# Validate and place a stop market order
r = place_stop_market_order(client, 'BTCUSDT', 'SELL', '0.001', '50000')
```

## 📊 Sample Output

```
==================================================
  ORDER REQUEST SUMMARY
==================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.001
==================================================

==================================================
  ORDER CONFIRMATION
==================================================
  Order ID     : 14487962026
  Symbol       : BTCUSDT
  Side         : BUY
  Type         : MARKET
  Status       : NEW
  Quantity     : 0.0010
  Executed Qty : 0.0000
==================================================
  Order placed successfully!
```

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API wrapper (auth, signing, HTTP)
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # File + console logging setup
├── cli.py                 # CLI entry point (argparse)
├── run.py                 # Interactive menu entry point
├── config.py              # API keys (excluded from git)
├── requirements.txt
└── README.md
```

## 🛠️ Setup

1. Clone the repository:git clone https://github.com/YOURUSERNAME/binance-futures-trading-bot.git
cd binance-futures-trading-bot
2. Create virtual environment:
   python -m venv venv
venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Add your API keys to `config.py`:
```python
   API_KEY = "your_key_here"
   API_SECRET = "your_secret_here"
```
   Get keys from: https://demo.binance.com/en/my/settings/api-management

## ▶️ How to Run

### Option 1 — Interactive Menu (Recommended)
python run.py
Select order type from menu and enter parameters when prompted.

### Option 2 — CLI Commands
python cli.py market --symbol BTCUSDT --side BUY --quantity 0.001
python cli.py limit  --symbol BTCUSDT --side BUY --quantity 0.001 --price 60000
python cli.py stop   --symbol BTCUSDT --side SELL --quantity 0.001 --stop-price 50000

## ✔️ Outputs saved as:
- Logs written to `logs/trading_bot_YYYYMMDD.log`
- Console shows real-time order status

## 🚧 Project Status & Notes

✅ Full order placement pipeline works end-to-end  
✅ MARKET, LIMIT, STOP_MARKET all tested and working  
✅ Interactive menu + CLI both functional  

> Note: Uses `demo-fapi.binance.com` (Binance official demo environment).
> STOP_MARKET orders use `/fapi/v1/algoOrder` endpoint as required
> by Binance since the December 2025 API migration.

## 🔮 Future Work
- Add order cancellation and status query commands
- Add position management (view open positions)
- Deploy as a web UI using Streamlit or Flask
- Add support for OCO and TWAP order types
- Add unit tests for all modules


## 📌 Tags
`#Python` `#Binance` `#TradingBot` `#Futures` `#AlgorithmicTrading`
`#CLI` `#Cryptocurrency` `#Fintech` `#HMAC` `#REST-API`
