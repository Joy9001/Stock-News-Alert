import os
import requests
from twilio.rest import Client

# STOCK API INFO
STOCK = "AMZN"
COMPANY_NAME = "Amazon.com, Inc."
# Get your STOCK_API_KEY
stock_api_key = os.environ.get("STOCK_API_KEY")
STOCK_API_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key
}

# NEWS API INFO
# Get your API_KEY
news_api_key = os.environ.get("NEWS_API_KEY")
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_PARAMS = {
    "apikey": news_api_key,
    "q": COMPANY_NAME,
    "sortBy": "popularity",
}

# TWILIO API
# Get your SID and TOKEN
sid = os.environ.get("SID")
token = os.environ.get("TOKEN")

stock_data = requests.get(url=STOCK_API_ENDPOINT, params=STOCK_PARAMS)
stock_data.raise_for_status()
# print(stock_data.json())
stock_info = stock_data.json()['Time Series (Daily)']
price1 = float(stock_info["2023-09-26"]["4. close"])
price2 = float(stock_info["2023-09-25"]["4. close"])

symbol = ""
news = ""
if price1 > price2:
    symbol = "🔼"
else:
    symbol = "🔽"
if price2 * 1.05 <= price1 or price1 * 1.05 >= price2:
    percent = round((abs(price1 - price2) / max(price1, price2)) * 100, 2)

    news_info = requests.get(url=NEWS_API_ENDPOINT, params=NEWS_PARAMS)
    news_info.raise_for_status()
    news_data = news_info.json()["articles"][0]
    news = f"{STOCK}: {symbol} {percent}%\nHeadline: {news_data['title']}\nBrief: {news_data['description']}"

    client = Client(sid, token)
    message = client.messages.create(body=news, from_="ENTER YOUR TWILIO NUMBER", to="ENTER YOUR NUMBER")
    print(message.status)
