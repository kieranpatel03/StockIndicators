import Technical_Analysis as TA
import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf
from matplotlib import dates as lib_dates
import pandas as pd


ticker = 'TSLA'
data = yf.download(ticker, period='360d', interval='1d')
data = data.loc[:, ['Open', 'High', 'Low', 'Close']]
data.index = pd.to_datetime(data.index)
ema_values  = TA.EMA(data['Close'].tolist(), 14)


extra_plots = [
    mpf.make_addplot(ema_values)
    ]


mpf.plot(data ,type='candle', figratio=(15, 7), style='yahoo',title=str(f"{ticker} Prices"), addplot=extra_plots)
