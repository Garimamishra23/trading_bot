import hashlib
import hmac
import time
from urllib.parse import urlencode
import requests
from bot.logging_config import get_logger

logger = get_logger("client")
BASE_URL = "https://demo-fapi.binance.com"

class BinanceAPIError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"Binance error {code}: {message}")

class NetworkError(Exception):
    pass

class BinanceFuturesClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = BASE_URL

        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        logger.info("Client ready (testnet)")

    def _timestamp(self):
        return int(time.time() * 1000)

    def _sign(self, params):
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()

    def _request(self, method, endpoint, params=None):
        params = params or {}
        params["timestamp"] = self._timestamp()
        params["signature"] = self._sign(params)

        url = self.base_url + endpoint
        logger.debug(">> %s %s | %s", method, url, {k: v for k, v in params.items() if k != "signature"})

        try:
            if method == "GET":
                response = self.session.get(url, params=params, timeout=(5, 10))
            elif method == "POST":
                response = self.session.post(url, data=params, timeout=(5, 10))
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection failed: {e}")
        except requests.exceptions.Timeout:
            raise NetworkError("Request timed out.")

        logger.debug("<< HTTP %s | %s", response.status_code, response.text[:300])

        data = response.json()

        if not response.ok or (isinstance(data, dict) and data.get("code", 0) not in (0, 200)):
            code = data.get("code", response.status_code)
            msg = data.get("msg", response.text)
            raise BinanceAPIError(code=code, message=msg)

        return data

    def get_account(self):
        return self._request("GET", "/fapi/v2/account")

    def place_algo_order(self, **params):
        return self._request("POST", "/fapi/v1/algoOrder", params=params)
    def place_order(self, **params):
        return self._request("POST", "/fapi/v1/order", params=params)
    def get_ticker(self, symbol):
        url = self.base_url + "/fapi/v1/ticker/24hr"
        response = self.session.get(url, params={"symbol": symbol}, timeout=(5, 10))
        return response.json()

    def get_balance(self):
        return self._request("GET", "/fapi/v2/balance")

    def get_positions(self):
        return self._request("GET", "/fapi/v2/positionRisk")


