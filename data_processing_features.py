import finnhub
import pandas as pd
from textblob import TextBlob
import datetime
from datetime import datetime, timedelta
from time import sleep

# yahoo finance
import yfinance as yf

finnhub_client = finnhub.Client(api_key="co3vqm9r01qqeav0rtmgco3vqm9r01qqeav0rtn0")


def get_news_df(start_date, end_date, df= pd.DataFrame()):
    for _ in range(91):
        temp_date = start_date + timedelta(days=4) if start_date + timedelta(days=4) <= end_date else end_date
        print('Start Date :', start_date, 'End Date:', temp_date)
        res = finnhub_client.company_news('AAPL', _from=start_date.strftime('%Y-%m-%d'), to=temp_date.strftime('%Y-%m-%d'))
        df1 = pd.DataFrame(res)
        df = pd.concat([df, df1])
        sleep(0.7)
        start_date = temp_date + timedelta(days=1)
    # df.head()
    return df

def clean_news_df(news_df, start_date):
    news_df["date"] = pd.to_datetime(pd.to_datetime(news_df["datetime"], unit="s").dt.date)
    news_df.drop(news_df[news_df['date'] <= pd.to_datetime(start_date) ].index, axis=0, inplace=True)
    news_df.drop(['datetime','url','related', 'id', 'category', 'image'], axis=1, inplace=True)
    news_df = news_df.replace('Looking for stock market analysis and research with proves results? Zacks.com offers in-depth financial research with over 30years of proven results.', None)
    news_df = news_df.replace('', None)
    news_df = news_df.dropna()
    return news_df

def get_sentiment_df(news_df):
    news_df['HeadSenti'] = news_df['headline'].apply(lambda x:TextBlob(x).sentiment.polarity)
    news_df['SummSenti'] = news_df['summary'].apply(lambda x:TextBlob(x).sentiment.polarity)
    news_df = news_df.pivot_table(index=['date'], columns=['source'], values=['HeadSenti', 'SummSenti'], fill_value=0)
    news_df.columns = news_df.columns.map('_'.join)
    return news_df

def get_stock_df(start_date, end_date):
    stock = yf.Ticker('AAPL')
    hist = stock.history(start=start_date.strftime('%Y-%m-%d'),end=end_date.strftime('%Y-%m-%d'),interval="1d")
    hist['date'] = pd.to_datetime(hist.index)
    hist['date'] = hist['date'].dt.date
    hist.index = pd.to_datetime(hist['date'])
    hist.drop(columns=['date'], axis=1, inplace=True)
    return hist