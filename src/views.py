import json
import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Optional
from src.utils import get_category_totals, get_currency_rates, get_stock_prices

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def get_event_data(date_str: str, period: Optional[str] = 'M') -> str:
    """Основная функция для генерации данных о событиях."""

    # Преобразуем строку в datetime
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # Загружаем данные из Excel
    df = pd.read_excel('data/operations.xlsx')

    # Фильтрация данных по заданному периоду
    if period is None:
        period = 'M'  # Если period не передан, ставим месяц по умолчанию.

    start_date = get_start_date(date, period)
    df_filtered = df[df['date'] >= start_date]

    # Получаем данные о расходах и поступлениях
    expenses = get_category_totals(df_filtered, category_type='expense')
    income = get_category_totals(df_filtered, category_type='income')

    # Получаем курсы валют и стоимость акций
    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices()

    # Формируем данные для ответа в виде словаря
    response = {
        "expenses": {
            "total_amount": round(expenses['total']),
            "main": expenses['main'],
            "transfers_and_cash": expenses['transfers_and_cash'],
        },
        "income": {
            "total_amount": round(income['total']),
            "main": income['main'],
        },
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    # Возвращаем строку JSON
    return json.dumps(response, ensure_ascii=False)


def get_start_date(date: datetime, period: str) -> datetime:
    """Возвращает начальную дату для фильтрации в зависимости от периода."""
    if period == 'W':
        # Начало недели (понедельник)
        start_date = date - timedelta(days=date.weekday())
    elif period == 'M':
        # Начало месяца
        start_date = date.replace(day=1)
    elif period == 'Y':
        # Начало года
        start_date = date.replace(month=1, day=1)
    elif period == 'ALL':
        # Все данные до указанной даты
        start_date = datetime.min
    else:
        # По умолчанию месяц
        start_date = date.replace(day=1)

    return start_date
