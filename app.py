import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from config import API_KEY, API_SECRET
from bot.logging_config import setup_logging
from bot.client import BinanceFuturesClient, BinanceAPIError, NetworkError
from bot.orders import place_market_order, place_limit_order, place_stop_market_order
from bot.validators import ValidationError

setup_logging()

# ── Page Config ───────────────────────────────────────
st.set_page_config(
    page_title="Futures Trading Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Hide streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; }

/* App background */
.stApp { background-color: #070b14; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
    border-right: 1px solid #1e2433;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* Top navbar */
.navbar {
    background: #0d1117;
    border-bottom: 1px solid #1e2433;
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0;
}
.navbar-brand {
    font-size: 20px;
    font-weight: 700;
    color: #f0b90b !important;
    letter-spacing: 0.5px;
}
.navbar-sub {
    font-size: 12px;
    color: #4a5568;
    margin-left: 10px;
}
.live-dot {
    width: 8px; height: 8px;
    background: #00d395;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.3; }
}

/* Ticker bar */
.ticker-bar {
    background: #0d1117;
    border-bottom: 1px solid #1e2433;
    padding: 10px 32px;
    display: flex;
    gap: 48px;
    align-items: center;
}
.ticker-label { font-size: 11px; color: #4a5568; text-transform: uppercase; letter-spacing: 1px; }
.ticker-value { font-size: 15px; font-weight: 600; font-family: 'JetBrains Mono', monospace; color: #e2e8f0; }
.ticker-pos   { color: #00d395 !important; }
.ticker-neg   { color: #ff4d4d !important; }

/* Main content area */
.main-content { padding: 20px 24px; }

/* Cards */
.card {
    background: #0d1117;
    border: 1px solid #1e2433;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.card-title {
    font-size: 11px;
    font-weight: 600;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 16px;
    border-bottom: 1px solid #1e2433;
    padding-bottom: 10px;
}
.balance-amount {
    font-size: 28px;
    font-weight: 700;
    color: #f0b90b;
    font-family: 'JetBrains Mono', monospace;
}
.balance-sub {
    font-size: 13px;
    color: #4a5568;
    margin-top: 4px;
}
.balance-avail {
    font-size: 18px;
    font-weight: 600;
    color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
}

/* Position card */
.position-item {
    background: #131921;
    border: 1px solid #1e2433;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.position-symbol { font-size: 14px; font-weight: 700; color: #e2e8f0; }
.position-side-long  { background:#00d39520; color:#00d395; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600; }
.position-side-short { background:#ff4d4d20; color:#ff4d4d; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600; }
.position-detail { font-size:12px; color:#4a5568; margin-top:6px; }
.pnl-pos { color:#00d395; font-weight:700; font-family:'JetBrains Mono',monospace; }
.pnl-neg { color:#ff4d4d; font-weight:700; font-family:'JetBrains Mono',monospace; }

/* Order form */
.order-card {
    background: #0d1117;
    border: 1px solid #1e2433;
    border-radius: 12px;
    padding: 24px;
}
.order-title {
    font-size: 11px;
    font-weight: 600;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 20px;
    border-bottom: 1px solid #1e2433;
    padding-bottom: 12px;
}

/* Summary row */
.summary-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #1e2433;
    font-size: 13px;
}
.summary-label { color: #4a5568; }
.summary-value { color: #e2e8f0; font-weight: 600; font-family: 'JetBrains Mono', monospace; }
.summary-buy   { color: #00d395 !important; }
.summary-sell  { color: #ff4d4d !important; }

/* Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: #131921 !important;
    border: 1px solid #1e2433 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #f0b90b !important;
    box-shadow: 0 0 0 2px #f0b90b20 !important;
}

/* Radio buttons */
.stRadio label { color: #e2e8f0 !important; }

/* Place order button */
.stButton button {
    width: 100% !important;
    padding: 14px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border: none !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s !important;
}

/* Confirmation box */
.confirm-box {
    background: #00d39510;
    border: 1px solid #00d39540;
    border-radius: 12px;
    padding: 20px;
    margin-top: 16px;
}
.confirm-title { color: #00d395; font-size: 13px; font-weight: 700; margin-bottom: 12px; }
.confirm-row   { display:flex; justify-content:space-between; padding:6px 0; font-size:13px; border-bottom:1px solid #1e2433; }
.confirm-label { color: #4a5568; }
.confirm-value { color: #e2e8f0; font-weight:600; font-family:'JetBrains Mono',monospace; }

/* Metric overrides */
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.2rem !important;
}
[data-testid="stMetricDelta"] { font-size: 0.85rem !important; }

/* Divider */
hr { border-color: #1e2433 !important; }

/* Expander */
.streamlit-expanderHeader {
    background: #131921 !important;
    border: 1px solid #1e2433 !important;
    border-radius: 8px !important;
    color: #4a5568 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Client ────────────────────────────────────────────
@st.cache_resource
def get_client():
    return BinanceFuturesClient(api_key=API_KEY, api_secret=API_SECRET)

client = get_client()

# ── Navbar ────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div style="display:flex; align-items:center;">
        <span class="navbar-brand">⚡ FUTURES TERMINAL</span>
        <span class="navbar-sub">USDT-M Demo Environment</span>
    </div>
    <div style="display:flex; align-items:center; gap:6px;">
        <span class="live-dot"></span>
        <span style="font-size:12px; color:#00d395;">LIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Ticker Bar ────────────────────────────────────────
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

try:
    tickers = {s: client.get_ticker(s) for s in SYMBOLS}
    ticker_html = '<div class="ticker-bar">'
    for sym, t in tickers.items():
        price  = float(t.get("lastPrice", 0))
        chg    = float(t.get("priceChangePercent", 0))
        cls    = "ticker-pos" if chg >= 0 else "ticker-neg"
        arrow  = "▲" if chg >= 0 else "▼"
        ticker_html += f"""
        <div>
            <div class="ticker-label">{sym}</div>
            <div class="ticker-value">${price:,.2f}
                <span class="{cls}" style="font-size:12px;">
                    {arrow} {abs(chg):.2f}%
                </span>
            </div>
        </div>"""
    ticker_html += "</div>"
    st.markdown(ticker_html, unsafe_allow_html=True)
except:
    pass

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💼 Account Overview")
    st.divider()

    try:
        balances = client.get_balance()
        usdt = next((b for b in balances if b.get("asset") == "USDT"), None)

        if usdt:
            total  = float(usdt.get("balance", 0))
            avail  = float(usdt.get("availableBalance", 0))
            pnl    = float(usdt.get("crossUnPnl", 0))
            used   = total - avail

            st.markdown(f"""
            <div class="card">
                <div class="card-title">Wallet Balance</div>
                <div class="balance-amount">${total:,.2f}</div>
                <div class="balance-sub">USDT Total</div>
                <br/>
                <div style="display:flex; justify-content:space-between; margin-top:8px;">
                    <div>
                        <div class="balance-sub">Available</div>
                        <div class="balance-avail">${avail:,.2f}</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="balance-sub">In Use</div>
                        <div class="balance-avail">${used:,.2f}</div>
                    </div>
                </div>
                <br/>
                <div class="balance-sub">Unrealized PnL</div>
                <div class="{'pnl-pos' if pnl >= 0 else 'pnl-neg'}">
                    {'▲' if pnl >= 0 else '▼'} ${abs(pnl):,.4f}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Balance bar
            if total > 0:
                pct = (avail / total) * 100
                st.progress(int(pct), text=f"Available: {pct:.1f}%")

    except Exception as e:
        st.error(f"Balance error: {e}")

    st.markdown("### 📊 Open Positions")
    st.divider()

    try:
        positions = client.get_positions()
        open_pos  = [p for p in positions if float(p.get("positionAmt", 0)) != 0]

        if open_pos:
            for p in open_pos:
                amt   = float(p.get("positionAmt", 0))
                pnl   = float(p.get("unRealizedProfit", 0))
                entry = float(p.get("entryPrice", 0))
                mark  = float(p.get("markPrice", 0))
                side  = "LONG" if amt > 0 else "SHORT"
                sc    = "position-side-long" if side == "LONG" else "position-side-short"
                pc    = "pnl-pos" if pnl >= 0 else "pnl-neg"

                st.markdown(f"""
                <div class="position-item">
                    <div style="display:flex; justify-content:space-between;">
                        <span class="position-symbol">{p.get('symbol')}</span>
                        <span class="{sc}">{side}</span>
                    </div>
                    <div class="position-detail">
                        Size: {abs(amt)} &nbsp;|&nbsp;
                        Entry: ${entry:,.2f} &nbsp;|&nbsp;
                        Mark: ${mark:,.2f}
                    </div>
                    <div class="{pc}" style="margin-top:6px;">
                        PnL: ${pnl:,.4f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; color:#4a5568; padding:20px;">
                No open positions
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Positions error: {e}")

    st.divider()
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()

# ── Main Content ──────────────────────────────────────
st.markdown('<div class="main-content">', unsafe_allow_html=True)
col_chart, col_order = st.columns([1.6, 1])

# ── LEFT: Chart ───────────────────────────────────────
with col_chart:
    

    chart_sym = st.selectbox("", SYMBOLS, key="chart_sym", label_visibility="collapsed")

    try:
        import requests as req
        url = f"https://demo-fapi.binance.com/fapi/v1/klines"
        params = {"symbol": chart_sym, "interval": "15m", "limit": 60}
        resp = req.get(url, params=params, timeout=5)
        klines = resp.json()

        opens   = [float(k[1]) for k in klines]
        highs   = [float(k[2]) for k in klines]
        lows    = [float(k[3]) for k in klines]
        closes  = [float(k[4]) for k in klines]
        times   = [datetime.fromtimestamp(k[0]/1000) for k in klines]

        fig = go.Figure(data=[go.Candlestick(
            x=times, open=opens, high=highs, low=lows, close=closes,
            increasing_line_color="#00d395",
            decreasing_line_color="#ff4d4d",
            increasing_fillcolor="rgba(0, 211, 149, 0.5)",
            decreasing_fillcolor="rgba(255, 77, 77, 0.5)",

        )])

        fig.update_layout(
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            font=dict(color="#4a5568", family="JetBrains Mono"),
            xaxis=dict(gridcolor="#1e2433", showgrid=True, zeroline=False),
            yaxis=dict(gridcolor="#1e2433", showgrid=True, zeroline=False, side="right"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=380,
            showlegend=False,
            xaxis_rangeslider_visible=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Chart error: {e}")

    

# ── RIGHT: Order Form ─────────────────────────────────
with col_order:
   

    symbol     = st.text_input("Symbol", value="BTCUSDT", key="order_sym").upper()
    side       = st.radio("Side", ["BUY", "SELL"], horizontal=True, key="order_side")
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "STOP_MARKET"], key="order_type")
    quantity   = st.number_input("Quantity", min_value=0.001,
                                  value=0.001, step=0.001, format="%.3f")

    price      = None
    stop_price = None

    if order_type == "LIMIT":
        price = st.number_input("Limit Price (USDT)", min_value=1.0,
                                 value=60000.0, step=100.0)
    elif order_type == "STOP_MARKET":
        stop_price = st.number_input("Stop Price (USDT)", min_value=1.0,
                                      value=50000.0, step=100.0)

    # Summary
    side_cls = "summary-buy" if side == "BUY" else "summary-sell"
    price_row = f"<div class='summary-row'><span class='summary-label'>Price</span><span class='summary-value'>${price:,.2f}</span></div>" if price else ""
    stop_row  = f"<div class='summary-row'><span class='summary-label'>Stop Price</span><span class='summary-value'>${stop_price:,.2f}</span></div>" if stop_price else ""

    st.markdown(f"""
    <div style="background:#070b14; border:1px solid #1e2433;
                border-radius:8px; padding:14px; margin:16px 0;">
        <div class="summary-row">
            <span class="summary-label">Symbol</span>
            <span class="summary-value">{symbol}</span>
        </div>
        <div class="summary-row">
            <span class="summary-label">Side</span>
            <span class="summary-value {side_cls}">{side}</span>
        </div>
        <div class="summary-row">
            <span class="summary-label">Type</span>
            <span class="summary-value">{order_type}</span>
        </div>
        <div class="summary-row">
            <span class="summary-label">Quantity</span>
            <span class="summary-value">{quantity:.3f}</span>
        </div>
        {price_row}
        {stop_row}
    </div>
    """, unsafe_allow_html=True)

    # Button color based on side
    btn_color = "#00d395" if side == "BUY" else "#ff4d4d"
    btn_hover = "#00b87a" if side == "BUY" else "#cc3333"
    st.markdown(f"""
    <style>
    div[data-testid="stButton"] > button {{
        background: {btn_color} !important;
        color: #fff !important;
    }}
    div[data-testid="stButton"] > button:hover {{
        background: {btn_hover} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    if st.button(f"⚡ {side} {order_type}", use_container_width=True):
        with st.spinner("Executing order..."):
            try:
                if order_type == "MARKET":
                    r = place_market_order(client, symbol, side, quantity)
                elif order_type == "LIMIT":
                    r = place_limit_order(client, symbol, side, quantity, price)
                elif order_type == "STOP_MARKET":
                    r = place_stop_market_order(client, symbol, side, quantity, stop_price)

                oid = r.get("algoId") or r.get("orderId")
                sta = r.get("algoStatus") or r.get("status")
                qty = r.get("quantity") or r.get("origQty")
                tp  = r.get("triggerPrice")
                lp  = r.get("price")

                tp_row = f"<div class='confirm-row'><span class='confirm-label'>Trigger Price</span><span class='confirm-value'>${float(tp):,.2f}</span></div>" if tp and float(tp) > 0 else ""
                lp_row = f"<div class='confirm-row'><span class='confirm-label'>Limit Price</span><span class='confirm-value'>${float(lp):,.2f}</span></div>" if lp and float(lp) > 0 else ""

                st.markdown(f"""
                <div class="confirm-box">
                    <div class="confirm-title">✅ Order Placed Successfully</div>
                    <div class="confirm-row">
                        <span class="confirm-label">Order ID</span>
                        <span class="confirm-value">{oid}</span>
                    </div>
                    <div class="confirm-row">
                        <span class="confirm-label">Status</span>
                        <span class="confirm-value">{sta}</span>
                    </div>
                    <div class="confirm-row">
                        <span class="confirm-label">Quantity</span>
                        <span class="confirm-value">{qty}</span>
                    </div>
                    {tp_row}
                    {lp_row}
                </div>
                """, unsafe_allow_html=True)

                with st.expander("🔍 Raw Response"):
                    st.json(r)

            except ValidationError as e:
                st.error(f"❌ {e}")
            except BinanceAPIError as e:
                st.error(f"❌ [{e.code}] {e.message}")
            except NetworkError as e:
                st.error(f"❌ {e}")

   

st.markdown("</div>", unsafe_allow_html=True)
