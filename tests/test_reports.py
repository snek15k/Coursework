import pytest
import json
from unittest.mock import patch, mock_open, call
from datetime import datetime
import logging
from src.reports import log_report_to_file


# Пример функции с декоратором
@log_report_to_file()
def generate_report():
    return {"data": "sample report"}


# Тест 1: Проверка записи в файл с автоматически сгенерированным именем
@patch("builtins.open", new_callable=mock_open)
@patch("logging.info")
def test_log_report_to_file_default(mock_logging, mock_open_file):
    # Поскольку имя файла не передано, будет использоваться автоматическое имя
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    expected_filename = f"../data/report_{now}.json"

    # Вызываем функцию с декоратором
    result = generate_report()

    # Проверяем, что результат возвращается правильно
    assert result == {"data": "sample report"}

    # Проверяем, что файл был открыт для записи с правильным именем
    mock_open_file.assert_called_once_with(expected_filename, 'w', encoding='utf-8')

    # Ожидаем строку JSON с отступами
    expected_json = json.dumps(result, ensure_ascii=False, indent=4)

    # Получаем строку, записанную методом write
    written_data = ''.join(call[0][0] for call in mock_open_file().write.call_args_list)

    # Проверяем, что записанные данные соответствуют ожидаемой строке JSON
    assert written_data == expected_json

    # Проверяем, что логирование произошло
    mock_logging.assert_called_once_with(f"Отчет записан в файл: {expected_filename}")

# Тест 2: Проверка записи в файл с переданным именем
@patch("builtins.open", new_callable=mock_open)
@patch("logging.info")
def test_log_report_to_file_with_filename(mock_logging, mock_open_file):
    # Передаем конкретное имя файла
    filename = "custom_report.json"

    # Подменяем поведение генератора имени файла в декораторе
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 2, 15, 19, 35, 32)  # Фиксированная дата и время
        result = generate_report(filename=filename)  # Передаем имя файла в тестируемую функцию

    # Проверяем, что результат возвращается правильно
    assert result == {"data": "sample report"}

    # Проверяем, что файл был открыт с переданным именем
    mock_open_file.assert_called_once_with(filename, 'w', encoding='utf-8')

    # Проверяем, что данные записаны в файл
    expected_json = json.dumps(result, ensure_ascii=False, indent=4)

    # Ожидаем несколько вызовов write, так как json.dump записывает данные частями
    write_calls = [
        call('{'),
        call('\n    '),
        call('"data"'),
        call(': '),
        call('"sample report"'),
        call('\n'),
        call('}')
    ]
    mock_open_file().write.assert_has_calls(write_calls)

    # Проверяем, что логирование произошло с правильным сообщением
    mock_logging.assert_called_once_with(f"Отчет записан в файл: {filename}")
