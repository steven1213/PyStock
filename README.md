# 创业板股票分析项目

## 项目目标
从2025年1月3号到今天，按天统计创业板每天涨幅10%+的股票，并分析这些股票的共性，最终编写通达信的选股指标。

## 步骤

1. **获取数据**
   - 使用Tushare获取创业板股票数据。
   - 每天获取涨幅超过10%的股票，并按天记录。

2. **分析**
   - 分析T-1日的股票数据，找出是否存在共性指标。
   - 根据共性指标编写通达信的选股指标。

3. **回测**
   - 对分析结果进行回测，验证选股策略的有效性。

## 数据源
- Tushare API接口：
  - 股票列表：[Tushare 股票列表文档](https://tushare.pro/document/2?doc_id=25)
  - 日线行情：[Tushare 日线行情文档](https://tushare.pro/document/2?doc_id=27)
  - 交易日历：[Tushare 交易日历文档](https://tushare.pro/document/2?doc_id=26)
- 网络爬虫


## 使用说明

### 环境准备
1. 安装所需库：
   ```bash
   pip install tushare pandas
   ```

2. 设置Tushare的token：
   - 在代码中设置您的Tushare token。