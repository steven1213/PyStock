import tushare as ts
import pandas as pd
import os
from config import TUSHARE_TOKEN, MAX_TS_CODES
from datetime import datetime

# 设置Tushare的token
ts.set_token(TUSHARE_TOKEN)
pro = ts.pro_api()

def fetch_stock_list():
    # 检查本地文件是否存在
    if os.path.exists('stock_list.csv'):
        # 检查文件的最后修改日期
        last_modified_date = datetime.fromtimestamp(os.path.getmtime('stock_list.csv')).date()
        today = datetime.today().date()
        
        # 如果今天的日期与最后修改日期相同，则返回缓存的数据
        if last_modified_date == today:
            print("使用缓存的股票列表。")
            return pd.read_csv('stock_list.csv')
        else:
            print("股票列表已过期，删除旧文件并重新获取数据。")
            os.remove('stock_list.csv')  # 删除旧文件
    
    # 获取股票列表
    stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name')
    stock_list.to_csv('stock_list.csv', index=False)  # 保存到本地文件
    return stock_list

def fetch_data(start_date, end_date):
    stock_list = fetch_stock_list()  # 获取股票列表

    # 从stock_list中获取创业板股票列表
    cyb_list = stock_list[stock_list['ts_code'].str.startswith('30')]

    # 存储所有股票的日线数据
    cyb_data = pd.DataFrame()

    # 遍历分组后的数据，请求日行情，并追加到cyb_data中
    for i in range(0, len(cyb_list), MAX_TS_CODES):
        # 获取当前批次的ts_code
        ts_codes_batch = cyb_list['ts_code'].iloc[i:i + MAX_TS_CODES].tolist()
        ts_codes_str = ','.join(ts_codes_batch)  # 拼接成字符串

        # 请求日线数据
        daily_data = pro.daily(ts_code=ts_codes_str, start_date=start_date, end_date=end_date)
        cyb_data = pd.concat([cyb_data, daily_data], ignore_index=True)  # 追加到总数据中

    return cyb_data 