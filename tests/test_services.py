import unittest
from unittest.mock import patch, MagicMock
import json
import pandas as pd
from src.services import analyze_cashback_categories_from_excel  # Замените на реальный импорт


class TestCashbackAnalysis(unittest.TestCase):

    @patch('pandas.read_excel')
    @patch('logging.info')  # Мокаем logging.info, чтобы проверять логи
    @patch('logging.error')  # Мокаем logging.error для проверки ошибок
    @patch('logging.warning')  # Мокаем logging.warning для проверки предупреждений
    def test_analyze_cashback_categories_from_excel_success(self, mock_warning, mock_error, mock_info, mock_read_excel):
        # Создаем тестовые данные
        data = {
            'Дата операции': ['2025-02-01', '2025-02-15'],
            'Категория': ['Еда', 'Транспорт'],
            'Сумма операции': [1000, 500]
        }
        df = pd.DataFrame(data)

        # Мокаем возвращаемое значение
        mock_read_excel.return_value = df

        # Вызов функции
        result = analyze_cashback_categories_from_excel('dummy_file.xlsx', 2025, 2)

        # Ожидаемый результат
        expected_result = {
            "Еда": 10.0,  # 1000 * 0.01
            "Транспорт": 5.0  # 500 * 0.01
        }

        # Преобразуем результат в словарь для сравнения
        result_dict = json.loads(result)

        # Проверяем, что результат верный
        self.assertEqual(result_dict, expected_result)

        # Проверяем, что логи содержат нужную информацию
        mock_info.assert_any_call('Данные успешно загружены из файла: dummy_file.xlsx')
        mock_info.assert_any_call(f"Преобразованные данные: {df[['Дата операции', 'Категория', 'Сумма операции']]}")
        mock_info.assert_any_call(f"Отфильтрованные данные: {df}")
        mock_info.assert_any_call(f"Результаты кешбэка по категориям: {expected_result}")
        mock_info.assert_any_call("Анализ завершен. Результат: {\"Еда\": 10.0, \"Транспорт\": 5.0}")

        # Проверяем, что не было ошибок или предупреждений
        mock_error.assert_not_called()
        mock_warning.assert_not_called()

    @patch('pandas.read_excel')
    def test_analyze_cashback_categories_from_excel_no_transactions(self, mock_read_excel):
        # Создаем данные без транзакций за февраль 2025
        data = {
            'Дата операции': ['2025-01-01', '2025-01-15'],
            'Категория': ['Еда', 'Транспорт'],
            'Сумма операции': [1000, 500]
        }
        df = pd.DataFrame(data)

        # Мокаем возвращаемое значение
        mock_read_excel.return_value = df

        # Вызов функции с фильтром по февралю 2025
        result = analyze_cashback_categories_from_excel('dummy_file.xlsx', 2025, 2)

        # Проверяем, что возвращено сообщение о том, что транзакций нет
        expected_result = json.dumps({})
        result_dict = json.loads(result)

        # Проверка, что результат пуст
        self.assertEqual(result_dict, {})

    @patch('pandas.read_excel')
    def test_analyze_cashback_categories_from_excel_missing_column(self, mock_read_excel):
        # Создаем данные с отсутствующим обязательным столбцом
        data = {
            'Дата операции': ['2025-02-01', '2025-02-15'],
            'Сумма операции': [1000, 500]
        }
        df = pd.DataFrame(data)

        # Мокаем возвращаемое значение
        mock_read_excel.return_value = df

        # Вызов функции
        result = analyze_cashback_categories_from_excel('dummy_file.xlsx', 2025, 2)

        # Проверяем, что функция вернула ошибку по отсутствующему столбцу
        expected_result = json.dumps({"error": "Отсутствует обязательный столбец: Категория"})
        result_dict = json.loads(result)

        # Проверка на соответствие результату
        self.assertEqual(result_dict, {"error": "Отсутствует обязательный столбец: Категория"})

    @patch('pandas.read_excel')
    def test_analyze_cashback_categories_from_excel_invalid_date_format(self, mock_read_excel):
        # Создаем данные с некорректными датами
        data = {
            'Дата операции': ['invalid_date', '2025-02-15'],
            'Категория': ['Еда', 'Транспорт'],
            'Сумма операции': [1000, 500]
        }
        df = pd.DataFrame(data)

        # Мокаем возвращаемое значение
        mock_read_excel.return_value = df

        # Вызов функции
        result = analyze_cashback_categories_from_excel('dummy_file.xlsx', 2025, 2)

        # Проверяем, что функция вернула ошибку по некорректному формату даты
        expected_result = json.dumps({"error": "Не удалось загрузить данные из Excel файла."})
        result_dict = json.loads(result)

        # Проверка на соответствие результату
        self.assertEqual(result_dict, {"error": "Не удалось загрузить данные из Excel файла."})
