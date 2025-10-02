from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/dividends/{ticker}")
def get_latest_dividend(ticker: str):
    try:
        t = yf.Ticker(ticker)
        divs = t.dividends

        if divs.empty:
            return {"ticker": ticker.upper(), "latest_dividend": None}

        latest_dividend = float(divs.iloc[-1])

        return {
            "ticker": ticker.upper(),
            "latest_dividend": latest_dividend
        }

    except Exception as e:
        return {"ticker": ticker.upper(), "error": str(e)}
