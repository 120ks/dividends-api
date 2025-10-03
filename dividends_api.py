from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

# -----------------------
# 1. Dividend API
# -----------------------
@app.get("/dividend/{ticker}")
def get_dividend_yield(ticker: str):
    try:
        t = yf.Ticker(ticker)
        dividend_yield = t.info.get("dividendYield", None)

        # If no dividend, set to 0.000
        if dividend_yield is None:
            dividend_yield_fmt = "0.000"
        else:
            dividend_yield_fmt = f"{float(dividend_yield):.3f}"

        return {
            "ticker": ticker.upper(),
            "yield": dividend_yield_fmt
        }

    except Exception as e:
        return {"ticker": ticker.upper(), "error": str(e)}


# -----------------------
# 2. AssetData API
# -----------------------
@app.get("/assetdata/{ticker}")
def get_asset_data(ticker: str):
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="20y", interval="1y")  # yearly open prices

        if hist.empty:
            return {"ticker": ticker.upper(), "data": []}

        shares = t.info.get("sharesOutstanding", None)
        if not shares:
            return {"ticker": ticker.upper(), "data": []}

        yearly_data = []
        for date, row in hist.iterrows():
            year = date.year
            price = row["Open"]

            if not price:
                continue

            # Round to nearest integer, then format as x.00
            price_fmt = f"{round(float(price)):.2f}"
            market_cap_fmt = f"{round((float(price) * shares) / 1e9):.2f}"

            yearly_data.append({
                "year": year,
                "price": price_fmt,
                "marketCap": market_cap_fmt
            })

        return {"ticker": ticker.upper(), "data": yearly_data}

    except Exception as e:
        return {"ticker": ticker.upper(), "error": str(e)}
