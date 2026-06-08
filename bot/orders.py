from decimal import Decimal
from bot.client import BinanceFuturesClient
from bot.logging_config import get_logger
from bot.validators import validate_symbol, validate_side, validate_quantity, validate_price, validate_order_type

logger = get_logger("orders")

def place_market_order(client, symbol, side, quantity):
    symbol   = validate_symbol(symbol)
    side     = validate_side(side)
    quantity = validate_quantity(quantity)

    logger.info("Placing MARKET order | symbol=%s side=%s qty=%s", symbol, side, quantity)

    payload = {
        "symbol":   symbol,
        "side":     side,
        "type":     "MARKET",
        "quantity": str(quantity),
    }

    response = client.place_order(**payload)
    logger.info("MARKET order placed | orderId=%s status=%s", response.get("orderId"), response.get("status"))
    return response

def place_limit_order(client, symbol, side, quantity, price):
    symbol   = validate_symbol(symbol)
    side     = validate_side(side)
    quantity = validate_quantity(quantity)
    price    = validate_price(price, "LIMIT")

    logger.info("Placing LIMIT order | symbol=%s side=%s qty=%s price=%s", symbol, side, quantity, price)

    payload = {
        "symbol":      symbol,
        "side":        side,
        "type":        "LIMIT",
        "quantity":    str(quantity),
        "price":       str(price),
        "timeInForce": "GTC",
    }

    response = client.place_order(**payload)
    logger.info("LIMIT order placed | orderId=%s status=%s", response.get("orderId"), response.get("status"))
    return response

def place_stop_market_order(client, symbol, side, quantity, stop_price):
    symbol     = validate_symbol(symbol)
    side       = validate_side(side)
    quantity   = validate_quantity(quantity)
    stop_price = validate_price(stop_price, "LIMIT")

    logger.info("Placing STOP_MARKET order | symbol=%s side=%s qty=%s stopPrice=%s", symbol, side, quantity, stop_price)

    payload = {
    "symbol":       symbol,
    "side":         side,
    "algoType":     "CONDITIONAL",
    "type":         "STOP_MARKET",
    "quantity":     str(quantity),
    "triggerPrice": str(stop_price),
    "timeInForce":  "GTC",
    }

    response = client.place_algo_order(**payload)
    logger.info("STOP_MARKET order placed | algoId=%s status=%s", response.get("algoId"), response.get("algoStatus"))
    return response