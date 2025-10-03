from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

# --- Dividends Endpoint ---
@app.get("/dividends/{ticker}")
def get_dividend_info(ticker: str):
    t = yf.Ticker(ticker)
    divs = t.dividends

    if divs.empty:
        return {"ticker": ticker.upper(), "latest_dividend": 0, "yield_percent": 0}

    latest_dividend = float(divs.iloc[-1])
    annual_dividend = latest_dividend * 4
    hist = t.history(period="1d")

    price = float(hist["Close"].iloc[-1]) if not hist.empty else None
    yield_percent = (annual_dividend / price) * 100 if price else 0

    return {
        "ticker": ticker.upper(),
        "latest_dividend": round(latest_dividend, 3),
        "yield_percent": round(yield_percent, 3),
        "price": round(price, 2) if price else 0
    }


# --- Asset Data Endpoint ---
@app.get("/assetdata/{ticker}")
def get_asset_data(ticker: str):
    t = yf.Ticker(ticker)
    hist = t.history(period="20y", interval="1mo")

    if hist.empty:
        return {"ticker": ticker.upper(), "data": []}

    yearly_data = {}
    shares = t.info.get("sharesOutstanding", None)

    for date, row in hist.iterrows():
        year = date.year
        if year not in yearly_data:
            price = float(row["Open"])
            if not price or price == 0:
                continue  # skip if no price data

            # Calculate market cap (or 0 if shares not available)
            market_cap = (price * shares) / 1e9 if shares else 0

            yearly_data[year] = {
                "year": year,
                "price": round(price, 2),
                "marketCap": round(market_cap, 2)
            }

    return {"ticker": ticker.upper(), "data": list(yearly_data.values())}
