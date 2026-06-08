from config import API_KEY, API_SECRET
from bot.logging_config import setup_logging
from bot.client import BinanceFuturesClient, BinanceAPIError, NetworkError
from bot.orders import place_market_order, place_limit_order, place_stop_market_order
from bot.validators import ValidationError

setup_logging()

def print_result(r):
    print("\n" + "="*50)
    print("  ORDER CONFIRMATION")
    print("="*50)
    print(f"  Order ID     : {r.get('algoId') or r.get('orderId')}")
    print(f"  Symbol       : {r.get('symbol')}")
    print(f"  Side         : {r.get('side')}")
    print(f"  Type         : {r.get('orderType') or r.get('type')}")
    print(f"  Status       : {r.get('algoStatus') or r.get('status')}")
    print(f"  Quantity     : {r.get('quantity') or r.get('origQty')}")
    if r.get('triggerPrice') and float(r.get('triggerPrice', 0)) > 0:
        print(f"  Trigger Price: {r.get('triggerPrice')}")
    if r.get('price') and float(r.get('price', 0)) > 0:
        print(f"  Limit Price  : {r.get('price')}")
    print("="*50)
    print("\n  Order placed successfully!\n")

def main():
    client = BinanceFuturesClient(api_key=API_KEY, api_secret=API_SECRET)

    while True:
        print("\n" + "="*50)
        print("   BINANCE FUTURES TRADING BOT")
        print("="*50)
        print("  1. Place MARKET order")
        print("  2. Place LIMIT order")
        print("  3. Place STOP_MARKET order")
        print("  4. Exit")
        print("="*50)

        choice = input("  Select option (1-4): ").strip()

        if choice == "4":
            print("\n  Goodbye!\n")
            break

        if choice not in ("1", "2", "3"):
            print("\n  Invalid choice. Please select 1-4.")
            continue

        symbol   = input("  Symbol   (e.g. BTCUSDT): ").strip().upper()
        side     = input("  Side     (BUY/SELL)    : ").strip().upper()
        quantity = input("  Quantity (e.g. 0.001)  : ").strip()

        try:
            if choice == "1":
                r = place_market_order(client, symbol, side, quantity)
                print_result(r)

            elif choice == "2":
                price = input("  Price    (e.g. 60000)  : ").strip()
                r = place_limit_order(client, symbol, side, quantity, price)
                print_result(r)

            elif choice == "3":
                stop_price = input("  Stop Price (e.g. 50000): ").strip()
                r = place_stop_market_order(client, symbol, side, quantity, stop_price)
                print_result(r)

        except ValidationError as e:
            print(f"\n  Validation error: {e}\n")
        except BinanceAPIError as e:
            print(f"\n  Binance error [{e.code}]: {e.message}\n")
        except NetworkError as e:
            print(f"\n  Network error: {e}\n")

if __name__ == "__main__":
    main()