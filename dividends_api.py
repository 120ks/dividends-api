from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/dividends/{ticker}")
def get_dividends(ticker: str):
    t = yf.Ticker(ticker)
    divs = t.dividends

    results = [
        {"date": str(date.date()), "dividend": float(div)}
        for date, div in divs.items()
    ]

    return {"ticker": ticker.upper(), "dividends": results}