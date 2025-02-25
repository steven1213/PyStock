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

def analyze_stocks(previous_data, current_data):
    # 找出当前涨幅超过10%的股票
    gain_stocks = find_stocks_with_gain(current_data)
    gain_stocks_codes = gain_stocks['ts_code'].tolist()

    # 找出前一天的对应股票
    previous_gain_stocks = previous_data[previous_data['ts_code'].isin(gain_stocks_codes)]
    
    # 分析上涨的秘密
    secret_codes = analyze_secret_codes(gain_stocks, previous_gain_stocks)
    
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