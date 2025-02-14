import json
from datetime import datetime, timedelta
from utils import load_user_settings, get_currency_rates, get_stock_prices, load_transactions_from_excel, \
    filter_transactions_by_date, get_top_transactions


# Основная функция для страницы "Главная"
def get_event_data(date_str: str, period: str = 'M') -> str:
    # Преобразуем строку даты в datetime
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # Получаем начальную дату для анализа
    start_date = get_start_date(date, period)

    # Загружаем настройки пользователя
    user_settings = load_user_settings()

    # Загружаем данные о транзакциях
    transactions_df = load_transactions_from_excel(r'C:\Users\artem\PycharmProjects\Coursework\data\operations.xlsx')

    # Фильтруем транзакции по дате
    filtered_transactions = filter_transactions_by_date(transactions_df, start_date, date)

    # Получаем топ-5 транзакций
    top_transactions = get_top_transactions(filtered_transactions)

    # Получаем курсы валют и цены на акции
    currencies = user_settings.get("user_currencies", [])
    stocks = user_settings.get("user_stocks", [])
    currency_rates = get_currency_rates(currencies)
    stock_prices = get_stock_prices(stocks)

    # Приветствие
    greeting = get_greeting(date)

    # Формируем JSON-ответ
    response = {
        "greeting": greeting,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    response_json = json.dumps(response, ensure_ascii=False, indent=4)
    return response_json


# Функция для получения приветствия в зависимости от времени
def get_greeting(date: datetime) -> str:
    hour = date.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


# Получение начальной даты для анализа
def get_start_date(date: datetime, period: str) -> datetime:
    if period == 'M':
        return date.replace(day=1)
    elif period == 'W':
        start_of_week = date - timedelta(days=date.weekday())
        return start_of_week
    elif period == 'Y':
        return date.replace(month=1, day=1)
    else:
        return datetime.min


print(get_start_date(datetime.strptime('2021-11-13 10:00:00', "%Y-%m-%d %H:%M:%S"), "M"))
print(get_greeting(datetime.strptime('2021-11-13 10:00:00', "%Y-%m-%d %H:%M:%S")))
print(get_event_data("2023-11-11 00:00:00", "M"))
