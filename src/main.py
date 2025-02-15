import os
import logging
import json
from datetime import datetime

import pandas as pd

from src.services import analyze_cashback_categories_from_excel
from src.reports import spending_by_category
from src.views import get_main_page

# Настройка логирования
logging.basicConfig(level=logging.INFO)

def main():
    # Путь к файлу с транзакциями
    transactions_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")

    # Параметры для анализа (год и месяц)
    current_year = datetime.now().year
    current_month = datetime.now().month

    logging.info(f"Запуск программы для {current_month}/{current_year}.")

    # 1. Получение главной страницы с данными (приветствие, карты, топ-5 транзакций, курсы валют, цены акций)
    logging.info("Получаем данные для главной страницы...")
    main_page = get_main_page(date=datetime.now().strftime("%Y-%m-%d"), transactions_path=transactions_file_path)
    print(main_page)

    # 2. Анализ кешбэка по категориям
    logging.info(f"Анализируем кешбэк по категориям для {current_month}/{current_year}...")
    cashback_analysis = analyze_cashback_categories_from_excel(
        file_path=transactions_file_path, year=current_year, month=current_month
    )
    print(cashback_analysis)

    # 3. Получение отчета по тратам по категориям за последние 3 месяца
    logging.info("Получаем отчет по тратам по категориям за последние 3 месяца...")
    transactions_df = pd.read_excel(transactions_file_path)
    spending_report = spending_by_category(transactions=transactions_df, category="Переводы")
    print(spending_report)

if __name__ == "__main__":
    main()
