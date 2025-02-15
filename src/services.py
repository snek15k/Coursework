import json
import logging
import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any


def analyze_cashback_categories_from_excel(file_path: str, year: int, month: int) -> str:
    """
    Функция анализирует транзакции из Excel файла и рассчитывает кешбэк по категориям для указанного года и месяца.
    """
    logging.info(f"Начат анализ транзакций за {month}/{year} из файла {file_path}.")

    # Загрузка данных из Excel файла
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных из Excel файла: {e}")
        return json.dumps({"error": "Не удалось загрузить данные из Excel файла."})

    # Проверим, что в данных есть необходимые столбцы
    required_columns = ['Дата операции', 'Категория', 'Сумма операции']
    for col in required_columns:
        if col not in df.columns:
            logging.error(f"Отсутствует обязательный столбец: {col}")
            return json.dumps({"error": f"Отсутствует обязательный столбец: {col}"})

    # Преобразуем дату транзакции в datetime
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], errors='coerce', dayfirst=True)

    # Логируем проверку преобразования
    logging.info(f"Преобразованные данные: {df['Дата операции']}")

    # Проверка на наличие некорректных дат (NaT)
    if df['Дата операции'].isna().any():
        logging.error("Некорректные даты в данных.")
        return json.dumps({"error": "Не удалось загрузить данные из Excel файла."})

    # Фильтруем данные по году и месяцу
    filtered_df = df[(df['Дата операции'].dt.year == year) & (df['Дата операции'].dt.month == month)]

    # Логируем результат фильтрации
    logging.info(f"Отфильтрованные данные: {filtered_df}")

    if filtered_df.empty:
        logging.warning(f"Нет транзакций за {month}/{year}.")
        return json.dumps({})  # Возвращаем пустой словарь, если нет транзакций

    # Функция для подсчета кешбэка по категориям
    def calculate_cashback_by_category(filtered_data: pd.DataFrame) -> Dict[str, float]:
        cashback_by_category = {}
        cashback_rate = 0.01  # Кешбэк составляет 1% от суммы транзакции

        for _, transaction in filtered_data.iterrows():
            category = transaction['Категория']
            amount = abs(transaction['Сумма операции'])  # Преобразуем сумму операции в положительное значение

            cashback = amount * cashback_rate  # Расчет кешбэка

            # Добавляем кешбэк для категории
            if category in cashback_by_category:
                cashback_by_category[category] += cashback
            else:
                cashback_by_category[category] = cashback

        return cashback_by_category

    # Анализ кешбэка по категориям
    cashback_by_category = calculate_cashback_by_category(filtered_df)

    # Логируем результаты кешбэка
    logging.info(f"Результаты кешбэка по категориям: {cashback_by_category}")

    # Преобразуем результаты в JSON
    result_json = json.dumps(cashback_by_category, ensure_ascii=False, indent=4)

    logging.info("Анализ завершен. Результат: %s", result_json)

    return result_json

# # Пример использования функции
# if __name__ == "__main__":
#     # Путь к Excel файлу
#     file_path = (os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx"))
#
#     # Анализ кешбэка за май 2020
#     result = analyze_cashback_categories_from_excel(file_path, 2020, 5)
#     print(result)
