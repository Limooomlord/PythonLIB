"""
Valimon - Библиотека для конвертации валют с поддержкой автодополнения в PyCharm
"""

from .core import CurrencyConverter, convert, get_supported_currencies
from .currencies import Currency, CURRENCIES, is_valid_currency
from .exceptions import ValimonError, CurrencyNotFoundError, InvalidAmountError, APIError

__version__ = "1.0.0"
__author__ = "Limooonlord"
__email__ = "?"

# Создаем экземпляр конвертера по умолчанию
converter = CurrencyConverter()

__all__ = [
    # Основные классы и функции
    'CurrencyConverter',
    'convert',
    'get_supported_currencies',
    'converter',  # Добавьте эту строку!

    # Валюты
    'Currency',
    'CURRENCIES',
    'is_valid_currency',

    # Исключения
    'ValimonError',
    'CurrencyNotFoundError',
    'InvalidAmountError',
    'APIError',
]
