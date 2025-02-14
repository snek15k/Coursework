import pandas as pd
import requests
import json


def get_category_totals(df: pd.DataFrame, category_type: str) -> dict:
    """Возвращает суммы расходов или поступлений по категориям."""
    category_column = 'expense_category' if category_type == 'expense' else 'income_category'

    # Сортировка и агрегация по категориям
    category_totals = df.groupby(category_column)['amount'].sum().sort_values(ascending=False)

    # Получаем топ-7 категорий
    main_categories = category_totals.head(7)

    # Все остальные категории в "Остальное"
    other_total = category_totals.iloc[7:].sum()
    main_categories = main_categories.append(pd.Series({"Остальное": other_total}))

    # Возвращаем данные по категориям
    return {
        "total": category_totals.sum(),
        "main": [{"category": category, "amount": round(amount)} for category, amount in main_categories.items()],
        "transfers_and_cash": get_transfers_and_cash(df)  # Получение перевода и наличных
    }


def get_transfers_and_cash(df: pd.DataFrame) -> list:
    """Возвращает суммы по переводам и наличным."""
    cash_and_transfers = df[df['expense_category'].isin(['Наличные', 'Переводы'])]
    return [
        {"category": category, "amount": round(amount)}
        for category, amount in cash_and_transfers.groupby('expense_category')['amount'].sum().items()
    ]


def get_currency_rates() -> list:
    """Получаем курсы валют через API."""
    # Пример API для получения курсов валют
    response = requests.get("EXCHANGE_RATE_API_KEY")
    data = json.loads(response.text)  # Применяем json для обработки ответа

    return [{"currency": currency, "rate": data['rates'][currency]} for currency in ['USD', 'EUR']]


def get_stock_prices() -> list:
    """Получаем стоимость акций через API."""
    # Пример API для получения стоимости акций
    stock_symbols = ["ALPHA_VANTAGE_API_KEY"]
    stock_prices = []

    for symbol in stock_symbols:
        response = requests.get(f"ALPHA_VANTAGE_API_KEY{symbol}")
        data = json.loads(response.text)  # Применяем json для обработки ответа
        stock_prices.append({"stock": symbol, "price": data['price']})

    return stock_prices
