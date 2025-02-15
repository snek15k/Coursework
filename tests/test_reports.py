import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
import json
import os
from src.reports import spending_by_category  # Замените на реальный путь

class TestSpendingByCategory(unittest.TestCase):

    @patch('builtins.open')  # Мокаем open для проверки записи в файл
    @patch('json.dump')  # Мокаем json.dump для проверки правильности записи
    def test_spending_by_category_decorator(self, mock_json_dump, mock_open):
        # Делаем пример транзакций
        data = {
            'Дата операции': ['2025-02-01', '2025-02-15', '2025-01-01'],
            'Категория': ['Супермаркеты', 'Супермаркеты', 'Транспорт'],
            'Сумма операции': [1000, 500, 200],
            'Описание': ['Покупка еды', 'Покупка напитков', 'Поездка']
        }
        df = pd.DataFrame(data)

        # Мокаем результат функции
        mock_json_dump.return_value = None

        # Вызовем функцию
        result = spending_by_category(transactions=df, category="Супермаркеты", date="2025-02-01")

        # Проверяем, что файл был открыт
        mock_open.assert_called_once_with("spending_by_category_report.json", 'w', encoding='utf-8')

        # Проверяем, что json.dump был вызван с правильным результатом
        mock_json_dump.assert_called_once()

        # Проверяем результат
        expected_result = {
            'category': 'Супермаркеты',
            'total_spending': 1500,
            'transactions': [
                {'Дата операции': '2025-02-01 00:00:00', 'Сумма операции': 1000, 'Описание': 'Покупка еды'},
                {'Дата операции': '2025-02-15 00:00:00', 'Сумма операции': 500, 'Описание': 'Покупка напитков'}
            ]
        }
        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, expected_result)

    @patch('pandas.read_excel')  # Мокаем чтение Excel файла
    def test_spending_by_category_no_transactions(self, mock_read_excel):
        # Создаем DataFrame с данными
        data = {
            'Дата операции': ['2025-01-01', '2025-01-15'],
            'Категория': ['Транспорт', 'Транспорт'],
            'Сумма операции': [1000, 500],
            'Описание': ['Поездка на такси', 'Поездка на автобусе']
        }
        df = pd.DataFrame(data)

        # Мокаем чтение Excel файла
        mock_read_excel.return_value = df

        # Вызов функции с категорией, по которой нет транзакций
        result = spending_by_category(transactions=df, category="Супермаркеты", date="2025-02-01")

        # Ожидаемый результат
        expected_result = {
            'category': 'Супермаркеты',
            'total_spending': 0,
            'transactions': []
        }

        # Проверяем, что результат пустой
        self.assertEqual(result, expected_result)

    @patch('pandas.read_excel')  # Мокаем чтение Excel файла
    def test_spending_by_category_no_category(self, mock_read_excel):
        # Создаем DataFrame с данными
        data = {
            'Дата операции': ['2025-01-01', '2025-01-15'],
            'Категория': ['Транспорт', 'Транспорт'],
            'Сумма операции': [1000, 500],
            'Описание': ['Поездка на такси', 'Поездка на автобусе']
        }
        df = pd.DataFrame(data)

        # Мокаем чтение Excel файла
        mock_read_excel.return_value = df

        # Вызов функции с категорией, которой нет в данных
        result = spending_by_category(transactions=df, category="Еда", date="2025-02-01")

        # Ожидаемый результат (пустой)
        expected_result = {
            'category': 'Еда',
            'total_spending': 0,
            'transactions': []
        }

        # Проверяем, что результат пустой
        self.assertEqual(result, expected_result)

    @patch('pandas.read_excel')  # Мокаем чтение Excel файла
    def test_spending_by_category_invalid_date_format(self, mock_read_excel):
        # Создаем DataFrame с данными
        data = {
            'Дата операции': ['2025-01-01', '2025-01-15'],
            'Категория': ['Транспорт', 'Транспорт'],
            'Сумма операции': [1000, 500],
            'Описание': ['Поездка на такси', 'Поездка на автобусе']
        }
        df = pd.DataFrame(data)

        # Мокаем чтение Excel файла
        mock_read_excel.return_value = df

        # Вызов функции с некорректной датой
        result = spending_by_category(transactions=df, category="Транспорт", date="invalid-date")

        # Ожидаемое поведение: дата невалидна, она не должна попасть в фильтрацию
        expected_result = {
            'category': 'Транспорт',
            'total_spending': 0,
            'transactions': []
        }

        # Проверяем, что результат пустой
        self.assertEqual(result, expected_result)
