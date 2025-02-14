import json
import logging
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def analyze_cashback_categories(transactions: List[Dict[str, Any]], year: int, month: int) -> str:
    """
    Анализирует категории с повышенным кешбэком за указанный месяц и год.

    :param transactions: Список транзакций в формате словарей.
    :param year: Год для анализа.
    :param month: Месяц для анализа.
    :return: JSON-строка с анализом кэшбэка по категориям.
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
