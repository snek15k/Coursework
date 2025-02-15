import logging
import re
from typing import Dict, List

# Конфигурируем логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_personal_transfers(transactions: List[Dict]) -> List[Dict]:
    """
    Функция для получения списка транзакций на переводы физлицам.

    Параметры:
    - transactions: список словарей с транзакциями.

    Возвращает:
    - Список словарей с транзакциями перевода физическим лицам.
    """
    try:
        # Регулярное выражение для поиска имен в формате "Имя Ф."
        name_pattern = re.compile(r'^[А-Яа-яЁё]+ [А-Яа-яЁё]\.$')

        # Используем функциональные элементы для фильтрации данных
        transfers = [
            transaction
            for transaction in transactions
            if transaction.get("Категория") == "Переводы" and transaction.get("Описание") and name_pattern.match(
                transaction.get("Описание"))
        ]

        # Логируем количество найденных переводов
        logger.info(f"Найдено {len(transfers)} транзакций на переводы физлицам.")

        return transfers

    except Exception as e:
        logger.error(f"Ошибка при обработке данных: {e}")
        return []
