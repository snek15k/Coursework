import json
import requests
import pandas as pd
from datetime import datetime
import logging
import os


# Загрузка пользовательских настроек
def load_user_settings() -> dict:
    pust_user_settings = (os.path.join(os.path.dirname(__file__), "..", "user_settings.json"))
    try:
        with open(pust_user_settings) as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading user settings: {e}")
        return {}


# Получение курсов валют из API
def get_currency_rates(currencies: list) -> list:
    rates = []
    api_key = "EXCHANGE_RATE_API_KEY"  # Используем API-ключ из .env
    url = f"https://api.exchangerate-api.com/v4/latest/RUB"

    try:
        response = requests.get(url)
        data = response.json()
        for currency in currencies:
            rate = data['rates'].get(currency)
            if rate:
                rates.append({"currency": currency, "rate": rate})
    except Exception as e:
        logging.error(f"Error fetching currency rates: {e}")
    return rates


# Получение цен на акции из API
def get_stock_prices(stocks: list) -> list:
    prices = []
    api_key = "ALPHA_VANTAGE_API_KEY"  # Используем API-ключ из .env
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="

    for stock in stocks:
        try:
            stock_url = f"{url}{stock}&interval=1min&apikey={api_key}"
            response = requests.get(stock_url)
            data = response.json()
            price = data['Time Series (1min)'][list(data['Time Series (1min)'].keys())[0]]['4. close']
            prices.append({"stock": stock, "price": float(price)})
        except Exception as e:
            logging.error(f"Error fetching stock prices for {stock}: {e}")
    return prices


# Загрузка данных о транзакциях из Excel
def load_transactions_from_excel(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        logging.error(f"Error loading transactions: {e}")
        return pd.DataFrame()


# Фильтрация транзакций по дате
def filter_transactions_by_date(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df['date'])
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]


# Получение топ-5 транзакций
def get_top_transactions(df: pd.DataFrame) -> list:
    top_transactions = df.nlargest(5, 'amount')[['date', 'amount', 'category', 'description']].to_dict(orient='records')
    return top_transactions
