import pandas as pd
import yfinance as yf
import time

# ---------------------------
# LOAD S&P 500 LIST
# ---------------------------

sp500 = pd.read_csv(
    "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
)

# ---------------------------
# SIMPLE SCORING MODEL
# ---------------------------

def calculate_score(info):

    score = 50

    pe = info.get("trailingPE")
    roe = info.get("returnOnEquity")
    debt = info.get("debtToEquity")
    market_cap = info.get("marketCap")

    # PE
    if pe:
        if pe < 15:
            score += 10
        elif pe < 25:
            score += 5

    # ROE
    if roe:
        roe_pct = roe * 100

        if roe_pct > 20:
            score += 15
        elif roe_pct > 10:
            score += 8

    # Debt
    if debt:
        if debt < 50:
            score += 10
        elif debt > 200:
            score -= 10

    return max(1, min(100, score))

# ---------------------------
# BUILD DATASET
# ---------------------------

results = []

for ticker in sp500["Symbol"]:

    try:

        stock = yf.Ticker(ticker)

        info = stock.info

        score = calculate_score(info)

        results.append({

            "Ticker": ticker,

            "Company": info.get(
                "shortName",
                ticker
            ),

            "Price": info.get(
                "currentPrice",
                info.get("regularMarketPrice")
            ),

            "Market Cap": info.get(
                "marketCap"
            ),

            "Score": score

        })

        print(f"Processed {ticker}")

        time.sleep(0.25)

    except Exception as e:

        print(f"Failed {ticker}: {e}")

# ---------------------------
# SAVE RESULTS
# ---------------------------

df = pd.DataFrame(results)

df.to_csv(
    "rankings.csv",
    index=False
)

print("Saved rankings.csv")