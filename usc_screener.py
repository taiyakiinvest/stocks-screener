import pandas as pd, yfinance as yf, os, datetime as dt

PER_MAX = 10
MCAP_MAX = 50_000_000_000       # 500 億
NETCASH_RATIO_MIN = 1

def passes(info):
    cap = info.get("marketCap")
    cash, debt = info.get("totalCash"), info.get("totalDebt", 0)
    per = info.get("trailingPE")
    if not (cap and cash is not None and per):
        return False
    netcash = (cash - debt) / cap if cap else 0
    return per <= PER_MAX and cap < MCAP_MAX and netcash >= NETCASH_RATIO_MIN

def main():
    df = pd.read_csv("tickers.csv")
    hits = []
    for ticker in df['ticker']:
        info = yf.Ticker(ticker).info
        if passes(info):
            hits.append(f"{ticker}\t{info.get('shortName','')}")
    today = dt.date.today()
    if hits:
        print(f"[{today}] Hits ({len(hits)})\n" + "\n".join(hits))
    else:
        print(f"[{today}] No hits")

if __name__ == "__main__":
    main()
