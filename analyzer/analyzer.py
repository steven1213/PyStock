import pandas as pd
import os

def load_daily_data(date_str):
    file_path = f"data/{date_str}.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"文件 {file_path} 不存在。")
        return pd.DataFrame()

def find_stocks_with_gain(data, threshold=0.1):
    # 计算涨幅
    data['涨幅'] = data['pct_chg'] / 100  # 将百分比转换为小数
    # 找出涨幅超过10%的股票
    return data[data['涨幅'] > threshold]

# analyzer.py

import pandas as pd
import numpy as np

def analyze_stocks(previous_data, current_data):
    """
    分析股票数据，找出涨幅超过10%的股票
    
    Args:
        previous_data: 前一天的股票数据
        current_data: 当前的股票数据
    
    Returns:
        gain_stocks: 涨幅超过10%的股票
        previous_gain_stocks: 前一天涨幅超过10%的股票
        secret_codes: 连续两天涨幅超过10%的股票
    """
    # 检查数据是否为空
    if current_data.empty or previous_data.empty:
        print("警告: 输入的数据为空，无法进行分析")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    # 检查必要的列是否存在
    required_columns = ['ts_code', 'close', 'pct_chg']
    for df, name in [(current_data, "current_data"), (previous_data, "previous_data")]:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"警告: {name} 缺少必要的列: {missing_columns}")
            print(f"可用的列: {df.columns.tolist()}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    # 复制数据以避免修改原始数据
    data = current_data.copy()
    prev_data = previous_data.copy()
    
    # 计算涨幅
    data['涨幅'] = data['pct_chg'] / 100  # 将百分比转换为小数
    prev_data['涨幅'] = prev_data['pct_chg'] / 100
    
    # 找出涨幅超过10%的股票
    gain_stocks = data[data['涨幅'] > 0.1]
    previous_gain_stocks = prev_data[prev_data['涨幅'] > 0.1]
    
    # 找出连续两天涨幅超过10%的股票
    gain_codes = set(gain_stocks['ts_code'])
    previous_gain_codes = set(previous_gain_stocks['ts_code'])
    secret_codes_set = gain_codes.intersection(previous_gain_codes)
    
    # 将连续两天涨幅超过10%的股票转换为DataFrame
    if secret_codes_set:
        secret_codes = data[data['ts_code'].isin(secret_codes_set)]
    else:
        secret_codes = pd.DataFrame()
    
    return gain_stocks, previous_gain_stocks, secret_codes

def analyze_secret_codes(gain_stocks, previous_gain_stocks):
    # 计算行业分布（假设数据中有industry字段）
    industry_distribution = gain_stocks['industry'].value_counts() if 'industry' in gain_stocks.columns else None
    
    # 计算平均成交量
    average_volume = gain_stocks['vol'].mean() if 'vol' in gain_stocks.columns else None
    
    # 计算涨幅的平均值
    average_gain = gain_stocks['涨幅'].mean() if '涨幅' in gain_stocks.columns else None
    
    # 计算前一天的平均涨幅
    previous_average_gain = previous_gain_stocks['pct_chg'].mean() / 100 if not previous_gain_stocks.empty else 0
    
    # 返回分析结果
    return {
        '行业分布': industry_distribution,
        '平均成交量': average_volume,
        '平均涨幅': average_gain,
        '前期平均涨幅': previous_average_gain
    }

if __name__ == "__main__":
    # 读取数据
    current_data = load_daily_data("20240103")
    previous_data = load_daily_data("20240102")

    # 分析股票
    gain_stocks, previous_gain_stocks, secret_codes = analyze_stocks(previous_data, current_data)

    print("当前涨幅超过10%的股票：")
    print(gain_stocks[['ts_code', '涨幅']])
    print("前一天对应的股票：")
    print(previous_gain_stocks[['ts_code', 'close']])
    
    print("上涨的秘密分析结果：")
    print("行业分布：")
    print(secret_codes['行业分布'])
    print("平均成交量：", secret_codes['平均成交量'])
    print("平均涨幅：", secret_codes['平均涨幅'])
    print("前期平均涨幅：", secret_codes['前期平均涨幅'])