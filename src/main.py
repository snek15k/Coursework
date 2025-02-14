import json
import logging
from datetime import datetime
import pandas as pd
from src.utils import get_category_totals, get_currency_rates, get_stock_prices
from src.services import analyze_cashback_categories
from src.views import get_event_data
from src.reports import spending_by_category

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main() -> None:
    """Главная функция для выполнения всех операций проекта."""
    logging.info("Запуск программы")

    # Получение текущей даты и формирование строки
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Генерация данных о событиях
    event_data = get_event_data(current_date, period='M')
    logging.info("Данные о событиях:")
    print(json.dumps(json.loads(event_data), indent=4, ensure_ascii=False))

    # Загрузка транзакций
    df = pd.read_excel('data/operations.xlsx')

    # Анализ расходов по категориям
    expenses = get_category_totals(df, category_type='expense')
    logging.info("Анализ расходов:")
    print(json.dumps(expenses, indent=4, ensure_ascii=False))

    # Анализ доходов по категориям
    income = get_category_totals(df, category_type='income')
    logging.info("Анализ доходов:")
    print(json.dumps(income, indent=4, ensure_ascii=False))

    # Получаем курсы валют и стоимость акций
    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices()
    logging.info("Курсы валют и стоимость акций:")
    print("Currency Rates:", json.dumps(currency_rates, indent=4, ensure_ascii=False))
    print("Stock Prices:", json.dumps(stock_prices, indent=4, ensure_ascii=False))

    # Анализ кешбэка за текущий месяц
    year = datetime.now().year
    month = datetime.now().month
    cashback_analysis = analyze_cashback_categories(df.to_dict(orient='records'), year, month)
    logging.info("Анализ кешбэка:")
    print(cashback_analysis)

    # Анализ расходов по заданной категории
    category = "Продукты"
    category_spending = spending_by_category(df, category)
    logging.info(f"Анализ расходов по категории '{category}':")
    print(json.dumps(category_spending, indent=4, ensure_ascii=False))

    logging.info("Программа завершила выполнение")


if __name__ == "__main__":
    main()
