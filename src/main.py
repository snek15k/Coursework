import os

import pandas as pd

from src.reports import spending_by_category
from src.services import get_personal_transfers
from src.views import generate_json_response

all_operations = pd.read_excel(os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx"))
all_operations_list_dict = all_operations.to_dict(orient='records')


excel_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
user_settings_path = os.path.join(os.path.dirname(__file__), "..", "user_settings.json")

# Вызов функции с более читаемыми аргументами
print(generate_json_response(
    "2025-02-15 12:30:00",
    excel_file_path,
    user_settings_path
))
print(get_personal_transfers(all_operations_list_dict))
# Путь к файлу
excel_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")

# Загружаем данные из Excel
transactions = pd.read_excel(excel_file_path)

# Вызов функции с разделёнными аргументами
print(spending_by_category(
    transactions=transactions,
    category="Супермаркеты",
    date="2020-05-20"
))
