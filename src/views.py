import os
import pandas as pd
import json
import requests
from datetime import datetime


def get_main_page(date: str, transactions_path: str) -> str:
    """
    Главная функция, которая принимает на вход дату и путь к файлу с транзакциями,
    возвращает JSON-ответ с приветствием, данными по картам, топ-5 транзакций,
    курсами валют и ценами акций.
    """

    # 1. Получаем приветствие
    def greet() -> str:
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            return "Доброе утро"
        elif 12 <= current_hour < 18:
            return "Добрый день"
        elif 18 <= current_hour < 23:
            return "Добрый вечер"
        else:
            return "Доброй ночи"

    greeting = greet()

    # 2. Получаем данные по картам
    def get_cards(transactions: pd.DataFrame) -> list:
        card_data = {}

        # Выводим уникальные значения в столбце 'Статус' и количество каждого статуса
        status_counts = transactions['Статус'].value_counts()
        print("Количество транзакций по статусам:", status_counts)

        for _, row in transactions.iterrows():
            card_number = row['Номер карты']
            # Фильтруем только успешные транзакции
            if row['Статус'] == 'OK' and row['Сумма операции'] > 0:
                # Очистка номера карты (удаление лишних пробелов или символов)
                card_number = str(card_number).replace(" ", "")  # удаляем пробелы
                last_4_digits = card_number[-4:]  # Получаем последние 4 цифры

                if card_number not in card_data:
                    card_data[card_number] = {
                        'last_4_digits': last_4_digits,
                        'total_spent': 0,
                        'cashback': 0
                    }
                card_data[card_number]['total_spent'] += row['Сумма операции']
                card_data[card_number]['cashback'] += row['Сумма операции'] // 100

        result = []
        for card_number, data in card_data.items():
            result.append({
                'last_digits': data['last_4_digits'],
                'total_spent': data['total_spent'],
                'cashback': data['cashback']
            })
        return result

    # Чтение данных из файла Excel
    df_transactions = pd.read_excel(transactions_path)

    cards = get_cards(df_transactions)

    # 3. Получаем топ-5 транзакций
    def get_top_transactions(transactions: pd.DataFrame) -> list:
        successful_transactions = transactions[transactions['Статус'] == 'OK']
        top_transactions = successful_transactions.sort_values(by='Сумма платежа', ascending=False).head(5)

        return [
            {
                'date': row['Дата операции'],
                'amount': row['Сумма платежа'],
                'category': row['Категория'],
                'description': row['Описание']
            }
            for _, row in top_transactions.iterrows()
        ]

    top_transactions = get_top_transactions(df_transactions)

    # 4. Получаем курс валют
    def get_currency_rates() -> list:
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url)
        data = response.json()
        currencies = ['USD', 'EUR']
        currency_rates = []
        for currency in currencies:
            if currency in data['rates']:
                currency_rates.append({
                    'currency': currency,
                    'rate': data['rates'][currency]
                })
        return currency_rates

    currency_rates = get_currency_rates()

    # 5. Получаем стоимость акций из S&P500
    def get_stock_prices() -> list:
        stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        stock_prices = []
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey=YOUR_API_KEY"
            response = requests.get(url)
            data = response.json()
            if "Time Series (1min)" in data:
                latest_timestamp = list(data["Time Series (1min)"].keys())[0]
                latest_price = data["Time Series (1min)"][latest_timestamp]["4. close"]
                stock_prices.append({
                    'stock': stock,
                    'price': latest_price
                })
        return stock_prices

    stock_prices = get_stock_prices()

    # Формируем итоговый JSON
    response_data = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(response_data, ensure_ascii=False, indent=4)


# # Пример вызова функции
# transactions_path = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
# date = "2025-02-15 10:00:00"
# result = get_main_page(date, transactions_path)
# print(result)
