# main.py

from data_fetcher import fetch_data
import pandas as pd
import pandas_market_calendars as mcal

def is_trading_day(date_str):
    china_calendar = mcal.get_calendar('SSE')
    date = pd.to_datetime(date_str)

    if date in china_calendar.schedule(start_date=date, end_date=date).index:
        return True
    else:
        return False

# 示例调用
if __name__ == "__main__":
    start_date = "20250103"  # YYYYMMDD格式
    end_date = pd.to_datetime("today").strftime("%Y%m%d")  # 当前日期
    data = fetch_data(start_date, end_date)