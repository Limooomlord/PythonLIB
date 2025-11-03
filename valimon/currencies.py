from typing import Dict, List, TypedDict, Union
from enum import Enum

class CurrencyInfo(TypedDict):
    code: str
    name: str
    symbol: str
    decimal_places: int

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CNY = "CNY"
    RUB = "RUB"
    INR = "INR"
    BRL = "BRL"
    CAD = "CAD"
    AUD = "AUD"
    CHF = "CHF"
    SEK = "SEK"
    NOK = "NOK"
    DKK = "DKK"
    PLN = "PLN"
    TRY = "TRY"
    UAH = "UAH"
    KZT = "KZT"

CURRENCIES: Dict[Currency, CurrencyInfo] = {
    Currency.USD: {
        "code": "USD",
        "name": "US Dollar",
        "symbol": "$",
        "decimal_places": 2
    },
    Currency.EUR: {
        "code": "EUR",
        "name": "Euro",
        "symbol": "€",
        "decimal_places": 2
    },
    Currency.GBP: {
        "code": "GBP",
        "name": "British Pound",
        "symbol": "£",
        "decimal_places": 2
    },
    Currency.JPY: {
        "code": "JPY",
        "name": "Japanese Yen",
        "symbol": "¥",
        "decimal_places": 0
    },
    Currency.RUB: {
        "code": "RUB",
        "name": "Russian Ruble",
        "symbol": "₽",
        "decimal_places": 2
    },
    Currency.UAH: {
        "code": "UAH",
        "name": "Ukrainian Hryvnia",
        "symbol": "₴",
        "decimal_places": 2
    },
    Currency.KZT: {
        "code": "KZT",
        "name": "Kazakhstani Tenge",
        "symbol": "₸",
        "decimal_places": 2
    },
}

def get_all_currencies() -> List[str]:
    return [currency.value for currency in Currency]

def is_valid_currency(currency: Union[str, Currency]) -> bool:
    if isinstance(currency, Currency):
        return True
    try:
        Currency(currency.upper())
        return True
    except ValueError:
        return False

def normalize_currency(currency: Union[str, Currency]) -> str:
    if isinstance(currency, Currency):
        return currency.value
    return currency.upper()
