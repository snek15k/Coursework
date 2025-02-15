from src.services import get_personal_transfers  # Подключите вашу функцию из модуля

# Тестовые данные
test_data = [
    {"Категория": "Переводы", "Описание": "Иван С.", "Сумма операции": 100, "Валюта операции": "RUB"},
    {"Категория": "Переводы", "Описание": "Артем П.", "Сумма операции": 150, "Валюта операции": "USD"},
    {"Категория": "Покупка", "Описание": "Сергей З.", "Сумма операции": 200, "Валюта операции": "RUB"},
    {"Категория": "Переводы", "Описание": "Марина Т.", "Сумма операции": 50, "Валюта операции": "EUR"},
    {"Категория": "Переводы", "Описание": "Иванов И.", "Сумма операции": 500, "Валюта операции": "USD"},
    {"Категория": "Переводы", "Описание": "Петр К.", "Сумма операции": 300, "Валюта операции": "RUB"},
    {"Категория": "Переводы", "Описание": "Алексей М.", "Сумма операции": 700, "Валюта операции": "EUR"},
    {"Категория": "Дивиденды", "Описание": "Татьяна О.", "Сумма операции": 1000, "Валюта операции": "USD"},
    {"Категория": "Переводы", "Описание": "Иван", "Сумма операции": 400, "Валюта операции": "RUB"},  # Некорректное имя
    {"Категория": "Переводы", "Описание": "Михаил", "Сумма операции": 200, "Валюта операции": "USD"}   # Некор имя
]

# Ожидаемый результат
expected_result = [
    {"Категория": "Переводы", "Описание": "Иван С.", "Сумма операции": 100, "Валюта операции": "RUB"},
    {"Категория": "Переводы", "Описание": "Артем П.", "Сумма операции": 150, "Валюта операции": "USD"},
    {"Категория": "Переводы", "Описание": "Марина Т.", "Сумма операции": 50, "Валюта операции": "EUR"},
    {"Категория": "Переводы", "Описание": "Иванов И.", "Сумма операции": 500, "Валюта операции": "USD"},
    {"Категория": "Переводы", "Описание": "Петр К.", "Сумма операции": 300, "Валюта операции": "RUB"},
    {"Категория": "Переводы", "Описание": "Алексей М.", "Сумма операции": 700, "Валюта операции": "EUR"}
]


# Тест фильтрации перевода на физлиц
def test_get_personal_transfers():
    result = get_personal_transfers(test_data)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


# Тест, когда нет подходящих транзакций (нет "Переводов")
def test_no_matching_transactions():
    data = [{"Категория": "Покупка", "Описание": "Петр К.", "Сумма операции": 200, "Валюта операции": "RUB"}]
    result = get_personal_transfers(data)
    assert result == [], f"Expected [], but got {result}"


# Тест, когда описание не соответствует формату (нет фамилии или без точки)
def test_invalid_description_format():
    data = [{"Категория": "Переводы", "Описание": "Тимур", "Сумма операции": 100, "Валюта операции": "RUB"}]
    result = get_personal_transfers(data)
    assert result == [], f"Expected [], but got {result}"


# Тест с пустым списком транзакций
def test_empty_list():
    result = get_personal_transfers([])
    assert result == [], f"Expected [], but got {result}"


# Тест, когда все транзакции соответствуют
def test_all_transactions_match():
    data = [{"Категория": "Переводы", "Описание": "Иван С.", "Сумма операции": 100, "Валюта операции": "RUB"},
            {"Категория": "Переводы", "Описание": "Артем П.", "Сумма операции": 150, "Валюта операции": "USD"}]
    result = get_personal_transfers(data)
    assert result == data, f"Expected {data}, but got {result}"


# Тест на исключение (проверка на ошибки в функции)
def test_function_error_handling():
    data = [{"Категория": "Переводы", "Описание": None, "Сумма операции": 100, "Валюта операции": "RUB"}]
    result = get_personal_transfers(data)
    assert result == [], f"Expected [], but got {result}"
