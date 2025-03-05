import pandas as pd
import os

def load_daily_data(date_str):
    file_path = f"data/{date_str}.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"文件 {file_path} 不存在。")
        return pd.DataFrame()

def backtest_strategy(stock_codes, start_date, end_date):
    # 这里可以实现回测逻辑
    # 假设我们有一个简单的策略：如果前一天涨幅超过10%，则买入
    results = []
    
    for date in pd.date_range(start=start_date, end=end_date):
        date_str = date.strftime("%Y%m%d")
        daily_data = load_daily_data(date_str)
        
        if daily_data.empty:
            continue
        
        # 找出符合条件的股票
        gain_stocks = daily_data[daily_data['ts_code'].isin(stock_codes)]
        
        for _, stock in gain_stocks.iterrows():
            # 记录回测结果
            results.append({
                'date': date_str,
                'ts_code': stock['ts_code'],
                'close': stock['close'],
                'gain': stock['pct_chg']  # 使用pct_chg字段
            })
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    # 假设我们从分析程序中得到了涨幅超过10%的股票代码
    stock_codes = ['300001', '300002']  # 示例股票代码
    start_date = "20240102"
    end_date = "20240130"

    # 回测策略
    backtest_results = backtest_strategy(stock_codes, start_date, end_date)

    print("回测结果：")
    print(backtest_results) 