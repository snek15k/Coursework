from datetime import datetime
import os
import pandas as pd
import requests
from dotenv import load_dotenv
from typing import List, Dict
import json


def greet() -> str:
    """
    Функция возвращает приветствие в зависимости от текущего времени суток.
    """
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_data_frame_from_excel_file(path_to_excel_file: str) -> dict:
    """
        Загружает данные из Excel файла и возвращает их в виде словаря.
        """
    try:
        # Загружаем Excel файл
        excel_data = pd.read_excel(path_to_excel_file, sheet_name=None)

        # Преобразуем в словарь, где ключи — имена листов, а значения — DataFrame
        return excel_data

    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return {}


def get_cards(transactions: dict) -> list[dict]:
    """
    Функция анализирует список транзакций и возвращает информацию по каждой карте:
    - последние 4 цифры номера карты;
    - общая сумма расходов;
    - кешбэк (1 рубль на каждые 100 рублей).
    """
    card_data = {}

    for sheet_name, df in transactions.items():
        print(f"Обрабатываем лист: {sheet_name}")

        # Проверим первые несколько строк для диагностики
        print(df.head())  # Выводим первые несколько строк данных

        for _, row in df.iterrows():
            card_number = row['Номер карты']
            # Проверка: выводим все данные транзакции
            print(f"Транзакция: {row.to_dict()}")

            if row['Статус'] == 'ОК' and row['Сумма операции'] > 0:
                # Извлекаем последние 4 цифры карты
                last_4_digits = str(card_number)[-4:]

                # Суммируем расходы по каждой карте
                if card_number not in card_data:
                    card_data[card_number] = {
                        'last_4_digits': last_4_digits,
                        'total_spent': 0,
                        'cashback': 0
                    }

                card_data[card_number]['total_spent'] += row['Сумма операции']
                # Кэшбэк: 1 рубль на каждые 100 рублей
                card_data[card_number]['cashback'] += row['Сумма операции'] // 100

    # Преобразуем данные в список словарей
    result = []
    for card_number, data in card_data.items():
        result.append({
            'Номер карты (последние 4 цифры)': data['last_4_digits'],
            'Общая сумма расходов': data['total_spent'],
            'Кэшбэк': data['cashback']
        })

    return result


def get_top_transactions(transactions: dict) -> list[dict]:
    """
        Функция выводит Топ-5 транзакций по сумме платежа.
        """
    all_transactions = []

    for sheet_name, df in transactions.items():
        print(f"Обрабатываем лист: {sheet_name}")

        # Проверим, что в данных есть нужные столбцы
        if 'Сумма платежа' not in df.columns or 'Статус' not in df.columns:
            print(f"Лист {sheet_name} не содержит нужных столбцов!")
            continue

        # Проверим уникальные значения в столбце 'Статус'
        print(f"Уникальные значения в столбце 'Статус': {df['Статус'].unique()}")

        # Фильтруем только успешные транзакции с статусом 'OK'
        successful_transactions = df[df['Статус'] == 'OK']
        print(f"Найдено успешных транзакций: {len(successful_transactions)}")

        # Собираем данные для каждой транзакции
        for _, row in successful_transactions.iterrows():
            all_transactions.append({
                'Дата операции': row['Дата операции'],
                'Дата платежа': row['Дата платежа'],
                'Номер карты': row['Номер карты'],
                'Сумма операции': row['Сумма операции'],
                'Сумма платежа': row['Сумма платежа'],
                'Описание': row['Описание']
            })

    # Если список пуст, то ничего не выводим
    if not all_transactions:
        print("Нет успешных транзакций для обработки.")
        return []

    # Сортируем транзакции по 'Сумма платежа' в порядке убывания и выбираем топ-5
    top_transactions = sorted(all_transactions, key=lambda x: x['Сумма платежа'], reverse=True)[:5]

    return top_transactions


def get_currency_rates(path_to_user_settings_json: str) -> list[dict]:
    """
        Функция получает стоимость валют для валют, указанных в файле настроек пользователя.
        """
    # Загружаем переменные окружения из файла .env
    load_dotenv()

    # Получаем ключ API из переменной окружения
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")

    if not api_key:
        raise ValueError("API ключ не найден в файле .env")

    # Загрузим настройки пользователя
    try:
        with open(path_to_user_settings_json, 'r') as f:
            user_settings = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл настроек {path_to_user_settings_json} не найден.")
    except json.JSONDecodeError:
        raise ValueError("Ошибка при чтении JSON файла настроек.")

    # Получаем список валют, которые интересуют пользователя
    user_currencies = user_settings.get("user_currencies", [])

    if not user_currencies:
        raise ValueError("Список валют в файле настроек не найден или пуст.")

    # Формируем URL для запроса (например, API Open Exchange Rates)
    url = "https://open.er-api.com/v6/latest/USD"  # Используем USD как базовую валюту

    # Отправляем запрос
    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})

    if response.status_code != 200:
        raise Exception(f"Ошибка при запросе данных: {response.status_code}")

    # Получаем данные из ответа
    data = response.json()

    # Проверяем, что курсы валют получены
    if 'rates' not in data:
        raise ValueError("Не удалось получить курсы валют из ответа API.")

    # Формируем список курсов валют для нужных валют из настроек
    currency_rates = []
    for currency in user_currencies:
        if currency in data['rates']:
            currency_rates.append({
                'currency': currency,
                'rate': data['rates'][currency]
            })
        else:
            print(f"Курс для валюты {currency} не найден в ответе API.")

    return currency_rates


def get_stock_prices(path_to_user_settings_json: str) -> list[dict]:
    """
        Функция получает стоимость акций для акций, указанных в файле настроек пользователя.
        """
    # Загружаем переменные окружения из файла .env
    load_dotenv()

    # Получаем ключ API из переменной окружения
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    if not api_key:
        raise ValueError("API ключ не найден в файле .env")

    # Загрузим настройки пользователя
    try:
        with open(path_to_user_settings_json, 'r') as f:
            user_settings = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл настроек {path_to_user_settings_json} не найден.")
    except json.JSONDecodeError:
        raise ValueError("Ошибка при чтении JSON файла настроек.")

    # Получаем список акций, которые интересуют пользователя
    user_stocks = user_settings.get("user_stocks", [])

    if not user_stocks:
        raise ValueError("Список акций в файле настроек не найден или пуст.")

    # Формируем URL для запроса к API Alpha Vantage (для получения данных о текущих ценах акций)
    base_url = "https://www.alphavantage.co/query"
    stock_prices = []

    # Запрашиваем цену каждой акции по очереди
    for stock in user_stocks:
        url = f"{base_url}?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey={api_key}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Ошибка при запросе данных для акции {stock}: {response.status_code}")
            continue

        # Получаем данные из ответа
        data = response.json()

        # Проверим, что данные для акций есть в ответе
        if "Time Series (1min)" not in data:
            print(f"Не удалось получить данные для акции {stock}.")
            continue

        # Получаем самую последнюю цену (первый элемент из данных)
        latest_timestamp = list(data["Time Series (1min)"].keys())[0]
        latest_data = data["Time Series (1min)"][latest_timestamp]
        latest_price = latest_data["4. close"]

        stock_prices.append({
            "symbol": stock,
            "price": latest_price
        })

    return stock_prices
