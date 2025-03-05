import pandas as pd
import os
from datetime import datetime, timedelta

def analyze_stock_rise():
    data_dir = r'e:\Project\python\PyStock\data'  # 使用原始字符串处理Windows路径
    
    # 修正日期范围（包含2月25日）
    current_date = datetime(2025, 1, 2)
    end_date = datetime(2025, 2, 25)
    
    while current_date <= end_date:
        filename = current_date.strftime('%Y%m%d') + '.csv'
        file_path = os.path.join(data_dir, filename)
        
        try:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                # 添加多个编码格式尝试
                try:
                    df = pd.read_csv(file_path, encoding='gbk')
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding='utf-8')
                
                # 列名兼容处理
                required_columns = {'代码', '名称', '现价', '涨跌幅'}
                if not required_columns.issubset(df.columns):
                    missing = required_columns - set(df.columns)
                    print(f"文件 {filename} 缺少必要列：{missing}")
                    continue
                
                # 转换数值类型
                df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
                df['现价'] = pd.to_numeric(df['现价'], errors='coerce')
                
                # 筛选有效数据
                rise_stocks = df[(df['涨跌幅'] > 10.0) & (df['涨跌幅'].notna())]
                
                if not rise_stocks.empty:
                    # 修正日期格式显示
                    print(f"\n{current_date.strftime('%Y年%m月%d日')}：")
                    for _, stock in rise_stocks.iterrows():
                        print(f"\t{stock['代码']}，{stock['名称']}，"
                              f"现价{stock['现价']:.2f}，涨幅{stock['涨跌幅']:.2f}%")
        
        except Exception as e:
            print(f"处理文件 {filename} 时出错：{str(e)}")
            continue
        finally:
            # 正确递增日期
            current_date += timedelta(days=1)

if __name__ == '__main__':
    analyze_stock_rise()