from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/dividends/{ticker}")
def get_dividend_info(ticker: str):
    try:
        t = yf.Ticker(ticker)
        divs = t.dividends

        if divs.empty:
            return {
                "ticker": ticker.upper(),
                "latest_dividend": None,
                "annual_dividend": None,
                "price": None,
                "yield_percent": None
            }

        # Latest dividend (most recent payout)
        latest_dividend = float(divs.iloc[-1])

        # Estimate annual dividend (assuming quarterly payments)
        annual_dividend = latest_dividend * 4

        # Get current share price (latest close)
        hist = t.history(period="1d")
        if hist.empty:
            price = None
        else:
            price = float(hist["Close"].iloc[-1])

        # Calculate yield if price available
        yield_percent = None
        if price and annual_dividend:
            yield_percent = (annual_dividend / price) * 100

        return {
            "ticker": ticker.upper(),
            "latest_dividend": latest_dividend,
            "annual_dividend": annual_dividend,
            "price": price,
            "yield_percent": yield_percent
        }

    except Exception as e:
        return {"ticker": ticker.upper(), "error": str(e)}
