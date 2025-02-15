import json
from datetime import datetime
from unittest.mock import mock_open, patch

import pandas as pd

from src.utils import (
    get_cards,
    get_currency_rates,
    get_data_frame_from_excel_file,
    get_stock_prices,
    get_top_transactions,
    greet,
)


# Тест для функции greet
def test_greet():
    current_time = datetime.now().hour
    if 5 <= current_time < 12:
        assert greet() == "Доброе утро"
    elif 12 <= current_time < 18:
        assert greet() == "Добрый день"
    elif 18 <= current_time < 23:
        assert greet() == "Добрый вечер"
    else:
        assert greet() == "Доброй ночи"


# Тест для функции get_data_frame_from_excel_file
@patch("pandas.read_excel")
def test_get_data_frame_from_excel_file(mock_read_excel):
    mock_read_excel.return_value = {'Sheet1': 'data'}  # Подставляем mock данные

    result = get_data_frame_from_excel_file('dummy_path.xlsx')

    assert isinstance(result, dict)
    assert 'Sheet1' in result


# Тест для функции get_cards
def test_get_cards():
    transactions = {
        'Sheet1': pd.DataFrame([
            {"Номер карты": 1234567890123456, "Статус": "ОК", "Сумма операции": 1000},
            {"Номер карты": 1234567890123456, "Статус": "ОК", "Сумма операции": 500},
            {"Номер карты": 9876543210987654, "Статус": "ОК", "Сумма операции": 1500},
        ])
    }

    result = get_cards(transactions)

    assert len(result) == 2
    assert result[0]['Номер карты (последние 4 цифры)'] == '3456'
    assert result[0]['Общая сумма расходов'] == 1500
    assert result[0]['Кэшбэк'] == 15
    assert result[1]['Номер карты (последние 4 цифры)'] == '7654'
    assert result[1]['Общая сумма расходов'] == 1500
    assert result[1]['Кэшбэк'] == 15


# Тест для функции get_top_transactions
def test_get_top_transactions():
    transactions = {
        'Sheet1': pd.DataFrame([
            {"Сумма платежа": 1000, "Статус": "OK", "Описание": "Transaction 1",
             "Дата операции": "2025-02-15", "Дата платежа": "2025-02-15",
             "Номер карты": "1234", "Сумма операции": 1000},

            {"Сумма платежа": 500, "Статус": "OK", "Описание": "Transaction 2",
             "Дата операции": "2025-02-16", "Дата платежа": "2025-02-16",
             "Номер карты": "5678", "Сумма операции": 500},

            {"Сумма платежа": 1500, "Статус": "OK", "Описание": "Transaction 3",
             "Дата операции": "2025-02-17", "Дата платежа": "2025-02-17",
             "Номер карты": "9012", "Сумма операции": 1500},

            {"Сумма платежа": 1200, "Статус": "OK", "Описание": "Transaction 4",
             "Дата операции": "2025-02-18", "Дата платежа": "2025-02-18",
             "Номер карты": "3456", "Сумма операции": 1200},

            {"Сумма платежа": 700, "Статус": "OK", "Описание": "Transaction 5",
             "Дата операции": "2025-02-19", "Дата платежа": "2025-02-19",
             "Номер карты": "7890", "Сумма операции": 700},
        ])
    }

    result = get_top_transactions(transactions)

    assert len(result) == 5
    assert result[0]['Сумма платежа'] == 1500
    assert result[4]['Сумма платежа'] == 500


# Тест для функции get_currency_rates
@patch("requests.get")
def test_get_currency_rates(mock_requests_get, monkeypatch):
    # Имитация переменной окружения с ключом API
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "dummy_api_key")

    mock_response = {
        'rates': {'USD': 1, 'EUR': 0.85, 'GBP': 0.75}
    }
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    user_settings = {"user_currencies": ["EUR", "GBP"]}
    mock_open_file = mock_open(read_data=json.dumps(user_settings))

    with patch('builtins.open', mock_open_file):
        result = get_currency_rates("dummy_path.json")

    assert len(result) == 2
    assert result[0]['currency'] == 'EUR'
    assert result[0]['rate'] == 0.85
    assert result[1]['currency'] == 'GBP'
    assert result[1]['rate'] == 0.75


# Тест для функции get_stock_prices
@patch("requests.get")
def test_get_stock_prices(mock_requests_get, monkeypatch):
    # Имитация переменной окружения с ключом API
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "dummy_api_key")

    mock_response = {
        "Time Series (1min)": {
            "2025-02-15 12:30:00": {"4. close": "150.12"}
        }
    }
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    user_settings = {"user_stocks": ["AAPL", "GOOGL"]}
    mock_open_file = mock_open(read_data=json.dumps(user_settings))

    with patch('builtins.open', mock_open_file):
        result = get_stock_prices("dummy_path.json")

    assert len(result) == 2  # Ожидаем два элемента, так как указаны две акции
    assert result[0]['symbol'] == 'AAPL'
    assert result[0]['price'] == "150.12"
    assert result[1]['symbol'] == 'GOOGL'
    assert result[1]['price'] == "150.12"
