import time
from yfinance.utils import YFRateLimitError

for ticker in df['ticker']:
    for _ in range(2):                 # 最大2回試す
        try:
            info = yf.Ticker(ticker).info
            break                      # 成功したら抜ける
        except YFRateLimitError:
            time.sleep(3)              # 3秒待ってリトライ
    else:
        continue                       # 2回とも失敗ならスキップ

    if passes(info):
        hits.append(f"{ticker}\t{info.get('shortName','')}")
    time.sleep(1)                      # 1秒クールダウン
