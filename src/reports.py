import pandas as pd
import json
import logging
from functools import wraps
from datetime import datetime, timedelta
from typing import Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Декоратор для записи отчета в файл
def log_report_to_file(filename: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(filename=None, *args, **kwargs):
            result = func(*args, **kwargs)
            print(result)

            # Если имя файла не передано, используем текущее время для имени файла
            if filename is None:
                filename = f"../data/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            # Записываем результат в файл
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            logging.info(f"Отчет записан в файл: {filename}")
            return result

        return wrapper

    return decorator


# Функция для получения трат по категории за последние 3 месяца
@log_report_to_file("spending_by_category_report.json")  # Можно передать имя файла
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> dict:
    # Если дата не передана, используем текущую дату
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # Преобразуем строку в объект datetime
    date = datetime.strptime(date, "%Y-%m-%d")

    # Убедимся, что столбец 'Дата операции' преобразован в тип datetime
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], errors='coerce')

    # Вычисляем дату 3 месяца назад
    start_date = date - timedelta(days=90)

    # Фильтруем транзакции по категории и дате
    filtered_transactions = transactions[
        (transactions['Категория'] == category) &
        (transactions['Дата операции'] >= start_date)
        ]

    # Возвращаем сумму трат по категории
    total_spending = filtered_transactions['Сумма операции'].sum()

    transactions = transactions.melt(id_vars=['Дата операции'])

    return {
        'category': category,
        'total_spending': total_spending,
        'transactions': filtered_transactions[['Дата операции', 'Сумма операции', 'Описание']].to_dict(orient='records')
    }


# Пример использования
if __name__ == "__main__":
    # Загружаем данные из Excel файла
    df = pd.read_excel(r'C:\Users\artem\PycharmProjects\Coursework\data\operations.xlsx')

    # Пример вызова функции с категорией и датой
    result = spending_by_category(transactions=df, category="Супермаркеты", date="2020-05-20")
    print(result)
