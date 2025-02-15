import json
from datetime import datetime

from src.utils import (
    get_cards,
    get_currency_rates,
    get_data_frame_from_excel_file,
    get_stock_prices,
    get_top_transactions,
    greet,
)


def generate_json_response(date_time_str: str, path_to_excel_file: str, path_to_user_settings_json: str) -> str:
    """
    Главная функция, принимающая на вход строку с датой и временем и возвращающая JSON-ответ с данными.

    :param date_time_str: Строка с датой и временем в формате "YYYY-MM-DD HH:MM:SS"
    :param path_to_excel_file: Путь к файлу Excel с данными транзакций
    :param path_to_user_settings_json: Путь к JSON файлу с настройками пользователя
    :return: JSON строка с нужными данными
    """

    # Преобразуем строку с датой и временем в объект datetime
    try:
        date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Неверный формат даты и времени. Ожидается формат YYYY-MM-DD HH:MM:SS")

    # Получаем приветствие
    greeting = greet()

    # Загружаем данные из Excel файла
    transactions = get_data_frame_from_excel_file(path_to_excel_file)

    # Получаем информацию по картам
    cards = get_cards(transactions)

    # Получаем топ-5 транзакций
    top_transactions = get_top_transactions(transactions)

    # Получаем курсы валют
    currency_rates = get_currency_rates(path_to_user_settings_json)

    # Получаем стоимость акций
    stock_prices = get_stock_prices(path_to_user_settings_json)

    # Формируем результат в формате JSON
    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    # Преобразуем ответ в строку JSON и возвращаем
    return json.dumps(response, ensure_ascii=False, indent=2)
