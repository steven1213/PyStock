# main.py

from data_fetcher import fetch_data
import pandas as pd


# 示例调用
if __name__ == "__main__":
    start_date = "20240103"  # YYYYMMDD格式
    end_date = pd.to_datetime("today").strftime("%Y%m%d")  # 当前日期
    data = fetch_data(start_date, end_date)