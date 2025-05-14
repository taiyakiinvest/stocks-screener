import pandas as pd, yfinance as yf, datetime as dt, time

# ────────── ルール定数 ──────────
PER_MAX = 10
MCAP_MAX = 50_000_000_000       # 500 億
NETCASH_RATIO_MIN = 1
# ────────────────────────────────

def passes(info):
    """3 つの清原ルールを判定"""
    cap  = info.get("marketCap")
    cash = info.get("totalCash")
    debt = info.get("totalDebt", 0)
    per  = info.get("trailingPE")

    # PER が None または文字列の時に備え数値化
    try:
        per = float(per)
    except (TypeError, ValueError):
        return False

    if not (cap and cash is not None):
        return False

    netcash_ratio = (cash - debt) / cap if cap else 0
    return per <= PER_MAX and cap < MCAP_MAX and netcash_ratio >= NETCASH_RATIO_MIN

def safe_get_info(ticker):
    """yfinance 取得＋レート制限リトライ"""
    for _ in range(2):   # 最大2回
        try:
            return yf.Ticker(ticker).info
        except Exception as e:
            if "rate limit" in str(e).lower() or "too many" in str(e).lower():
                time.sleep(3)      # 3秒待って再試行
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
        time.sleep(1)            # 1秒クールダウン

    today = dt.date.today()
    if hits:
        print(f"[{today}] Hits ({len(hits)})\n" + "\n".join(hits))
    else:
        print(f"[{today}] No hits")

if __name__ == "__main__":
    main()
