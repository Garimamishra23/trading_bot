from decimal import Decimal, InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}

class ValidationError(ValueError):
    pass

def validate_symbol(symbol):
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValidationError("Symbol cannot be empty.")
    return symbol

def validate_side(side):
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Side must be BUY or SELL, got '{side}'.")
    return side

def validate_order_type(order_type):
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Order type must be MARKET, LIMIT or STOP_MARKET, got '{order_type}'.")
    return order_type

def validate_quantity(quantity):
    try:
        qty = Decimal(str(quantity))
    except InvalidOperation:
        raise ValidationError(f"Quantity must be a number, got '{quantity}'.")
    if qty <= 0:
        raise ValidationError(f"Quantity must be greater than zero, got {qty}.")
    return qty

def validate_price(price, order_type):
    if order_type == "MARKET":
        return None
    if price is None or str(price).strip() == "":
        raise ValidationError(f"Price is required for {order_type} orders.")
    try:
        p = Decimal(str(price))
    except InvalidOperation:
        raise ValidationError(f"Price must be a number, got '{price}'.")
    if p <= 0:
        raise ValidationError(f"Price must be greater than zero, got {p}.")
    return p