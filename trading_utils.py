import pandas as pd
import pandas_market_calendars as mcal

def is_trading_day(date_str):
    china_calendar = mcal.get_calendar('SSE')
    date = pd.to_datetime(date_str)

    if date in china_calendar.schedule(start_date=date, end_date=date).index:
        return True
    else:
        return False 