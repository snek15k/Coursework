import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Any, Optional, Callable

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def analyze_cashback_categories(transactions: List[Dict[str, Any]], year: int, month: int) -> str:
    """
    Анализирует категории с повышенным кешбэком за указанный месяц и год.
    """
    cashback_by_category = defaultdict(float)

    for transaction in transactions:
        try:
            transaction_date = datetime.strptime(transaction["Дата операции"], "%Y-%m-%d")
            if transaction_date.year == year and transaction_date.month == month:
                category = transaction["Категория"]
                cashback = float(transaction["Кэшбэк"].replace(',', '.'))
                cashback_by_category[category] += cashback
        except (KeyError, ValueError) as e:
            logging.warning(f"Ошибка обработки транзакции {transaction}: {e}")

    result = json.dumps(cashback_by_category, ensure_ascii=False, indent=4)
    logging.info(f"Анализ кешбэка за {year}-{month} завершен")
    return result


def report_decorator(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для сохранения отчета в файл.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            file_name = filename or f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
            logging.info(f"Отчет сохранен в файл {file_name}")
            return result

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Dict[str, float]:
    """
    Возвращает траты по заданной категории за последние три месяца от переданной даты.
    """
    if date is None:
        date = datetime.today().strftime('%Y-%m-%d')

    end_date = datetime.strptime(date, '%Y-%m-%d')
    start_date = end_date - timedelta(days=90)

    filtered_data = transactions[(transactions['Дата операции'] >= start_date.strftime('%Y-%m-%d')) &
                                 (transactions['Дата операции'] <= end_date.strftime('%Y-%m-%d')) &
                                 (transactions['Категория'] == category)]

    total_spent = filtered_data['Сумма операции'].sum()

    result = {category: total_spent}
    logging.info(
        f"Расходы по категории '{category}' за период {start_date.date()} - {end_date.date()} составили {total_spent}")
    return result
