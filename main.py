# main.py

from data_fetcher.data_fetcher import fetch_stock_list
from analyzer.analyzer import analyze_stocks
from backtester.backtester import backtest_strategy
import pandas as pd


# 示例调用
if __name__ == "__main__":
    # 获取股票列表
    stock_list = fetch_stock_list()
    
    # 加载示例数据或创建包含必要列的数据框
    try:
        # 尝试加载实际数据
        current_data = pd.read_csv('data/20250102.csv')  # 修改为实际数据路径
        previous_data = pd.read_csv('data/20250101.csv')  # 修改为实际数据路径
        
        # 确保列名映射正确
        if 'pct_chg' not in current_data.columns and '涨跌幅' in current_data.columns:
            current_data['pct_chg'] = current_data['涨跌幅']
        if 'pct_chg' not in previous_data.columns and '涨跌幅' in previous_data.columns:
            previous_data['pct_chg'] = previous_data['涨跌幅']
            
        if 'ts_code' not in current_data.columns and '代码' in current_data.columns:
            current_data['ts_code'] = current_data['代码']
        if 'ts_code' not in previous_data.columns and '代码' in previous_data.columns:
            previous_data['ts_code'] = previous_data['代码']
            
        if 'close' not in current_data.columns and '现价' in current_data.columns:
            current_data['close'] = current_data['现价']
        if 'close' not in previous_data.columns and '现价' in previous_data.columns:
            previous_data['close'] = previous_data['现价']
    except Exception as e:
        print(f"加载数据时出错: {e}")
        print("创建示例数据用于测试...")
        # 创建示例数据
        current_data = pd.DataFrame({
            'ts_code': ['000001.SZ', '000002.SZ', '000003.SZ'],
            'close': [10.5, 20.3, 15.7],
            'pct_chg': [12.5, 8.3, 15.2]  # 百分比形式
        })
        previous_data = pd.DataFrame({
            'ts_code': ['000001.SZ', '000002.SZ', '000003.SZ'],
            'close': [9.5, 18.3, 13.7],
            'pct_chg': [11.2, 7.5, 9.8]  # 百分比形式
        })

    # 分析股票
    gain_stocks, previous_gain_stocks, secret_codes = analyze_stocks(previous_data, current_data)

    # 打印分析结果
    print("\n涨幅超过10%的股票:")
    if not gain_stocks.empty:
        print(gain_stocks[['ts_code', 'close', 'pct_chg']])
    else:
        print("没有找到涨幅超过10%的股票")

    # 假设我们从分析程序中得到了涨幅超过10%的股票代码
    if not gain_stocks.empty:
        stock_codes = gain_stocks['ts_code'].tolist()  # 获取涨幅超过10%的股票代码
        start_date = "20250102"
        end_date = "20250103"

        # 回测策略
        backtest_results = backtest_strategy(stock_codes, start_date, end_date)

        print("\n回测结果：")
        print(backtest_results)
    else:
        print("\n没有股票可以进行回测")