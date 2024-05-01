from datetime import datetime, timedelta
from data_processing_features import get_news_df, clean_news_df, get_sentiment_df, get_stock_df


start_date = datetime.strptime('2023-04-18', '%Y-%m-%d')
end_date = datetime.strptime('2024-04-17', '%Y-%m-%d')


news_df = get_news_df(start_date=start_date, end_date=end_date)
news_df = clean_news_df(news_df, start_date)
news_df = get_sentiment_df(news_df)

stock_df = get_stock_df(start_date=start_date, end_date=end_date)
print(stock_df.head())
