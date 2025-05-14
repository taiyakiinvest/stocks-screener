import pandas as pd, yfinance as yf, datetime as dt, time

# … 定数と passes() はそのまま …

def safe_get_info(ticker):
    """yfinance から info を取得。RateLimit 時は最大2回リトライ"""
    for _ in range(2):                      # 最大2回
        try:
            return yf.Ticker(ticker).info
        except Exception as e:
            # レート制限っぽい文言を検出
            if "rate limit" in str(e).lower() or "too many" in str(e).lower():
                time.sleep(3)               # 3秒待って再試行
            else:
                return None
    return None

def main():
    df = pd.read_csv("tickers.csv")
    hits = []
    for ticker in df["ticker"]:
        info = safe_get_info(ticker)
        if not info:
            continue
        if passes(info):
            hits.append(f"{ticker}\t{info.get('shortName','')}")
        time.sleep(1)                       # 1秒クールダウン

    today = dt.date.today()
    if hits:
        print(f"[{today}] Hits ({len(hits)})\n" + "\n".join(hits))
    else:
        print(f"[{today}] No hits")

if __name__ == "__main__":
    main()
