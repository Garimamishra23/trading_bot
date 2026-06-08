import argparse
import sys
from config import API_KEY, API_SECRET
from bot.logging_config import setup_logging, get_logger
from bot.client import BinanceFuturesClient, BinanceAPIError, NetworkError
from bot.orders import place_market_order, place_limit_order, place_stop_market_order
from bot.validators import ValidationError

setup_logging()
logger = get_logger("cli")

def print_request_summary(symbol, side, order_type, quantity, price=None, stop_price=None):
    print("\n" + "="*50)
    print("  ORDER REQUEST SUMMARY")
    print("="*50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    if stop_price:
        print(f"  Stop Price : {stop_price}")
    print("="*50 + "\n")

def print_order_result(r):
    # algo orders use different field names
    is_algo = "algoId" in r

    print("\n" + "="*50)
    print("  ORDER CONFIRMATION")
    print("="*50)
    print(f"  Order ID     : {r.get('algoId') or r.get('orderId')}")
    print(f"  Symbol       : {r.get('symbol')}")
    print(f"  Side         : {r.get('side')}")
    print(f"  Type         : {r.get('orderType') or r.get('type')}")
    print(f"  Status       : {r.get('algoStatus') or r.get('status')}")
    print(f"  Quantity     : {r.get('quantity') or r.get('origQty')}")
    print(f"  Executed Qty : {r.get('executedQty', 'N/A')}")
    if r.get('triggerPrice') and float(r.get('triggerPrice', 0)) > 0:
        print(f"  Trigger Price: {r.get('triggerPrice')}")
    if r.get('price') and float(r.get('price', 0)) > 0:
        print(f"  Limit Price  : {r.get('price')}")
    print("="*50)

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # shared arguments
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--symbol",   required=True, help="e.g. BTCUSDT")
    shared.add_argument("--side",     required=True, choices=["BUY", "SELL"])
    shared.add_argument("--quantity", required=True, type=float)

    # market
    subparsers.add_parser("market", parents=[shared],
                          help="Place a MARKET order")

    # limit
    lp = subparsers.add_parser("limit", parents=[shared],
                               help="Place a LIMIT order")
    lp.add_argument("--price", required=True, type=float)

    # stop (bonus)
    sp = subparsers.add_parser("stop", parents=[shared],
                               help="Place a STOP_MARKET order")
    sp.add_argument("--stop-price", required=True, type=float, dest="stop_price")

    args = parser.parse_args()
    client = BinanceFuturesClient(api_key=API_KEY, api_secret=API_SECRET)

    try:
        if args.command == "market":
            print_request_summary(args.symbol, args.side, "MARKET", args.quantity)
            r = place_market_order(client, args.symbol, args.side, args.quantity)

        elif args.command == "limit":
            print_request_summary(args.symbol, args.side, "LIMIT", args.quantity, price=args.price)
            r = place_limit_order(client, args.symbol, args.side, args.quantity, args.price)

        elif args.command == "stop":
            print_request_summary(args.symbol, args.side, "STOP_MARKET", args.quantity, stop_price=args.stop_price)
            r = place_stop_market_order(client, args.symbol, args.side, args.quantity, args.stop_price)

        print_order_result(r)
        print("\n  Order placed successfully!\n")
        logger.info("Order completed | orderId=%s status=%s", r.get('orderId'), r.get('status'))

    except ValidationError as e:
        print(f"\n  Validation error: {e}\n")
        logger.warning("Validation error: %s", e)
        sys.exit(1)

    except BinanceAPIError as e:
        print(f"\n  Binance API error [{e.code}]: {e.message}\n")
        logger.error("API error: %s", e)
        sys.exit(2)

    except NetworkError as e:
        print(f"\n  Network error: {e}\n")
        logger.error("Network error: %s", e)
        sys.exit(3)

if __name__ == "__main__":
    main()