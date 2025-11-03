from typing import Union, Dict, Optional, List
from decimal import Decimal, ROUND_HALF_UP
import requests
from datetime import datetime, timedelta

from .currencies import Currency, CURRENCIES, is_valid_currency, normalize_currency
from .exceptions import CurrencyNotFoundError, InvalidAmountError, APIError

class CurrencyConverter:

    def __init__(self, api_key: str = None, cache_timeout: int = 3600):
        self.api_key = api_key
        self.cache_timeout = cache_timeout
        self._rates_cache: Dict[str, Dict[str, Decimal]] = {}
        self._cache_timestamp: Dict[str, datetime] = {}

        self._base_rates = {
            'USD': Decimal('1.0'),
            'EUR': Decimal('0.93'),
            'GBP': Decimal('0.80'),
            'JPY': Decimal('148.0'),
            'RUB': Decimal('92.0'),
            'UAH': Decimal('38.5'),
            'KZT': Decimal('450.0'),
        }

    def _get_cached_rates(self, base_currency: str) -> Optional[Dict[str, Decimal]]:
        if base_currency in self._rates_cache:
            cache_time = self._cache_timestamp.get(base_currency)
            if cache_time and datetime.now() - cache_time < timedelta(seconds=self.cache_timeout):
                return self._rates_cache[base_currency]
        return None

    def _fetch_exchange_rates(self, base_currency: str) -> Dict[str, Decimal]:
        return self._base_rates

    def get_exchange_rates(self, base_currency: str = 'USD') -> Dict[str, Decimal]:
        base_currency_str = normalize_currency(base_currency)

        if not is_valid_currency(base_currency_str):
            raise CurrencyNotFoundError(base_currency_str)

        cached_rates = self._get_cached_rates(base_currency_str)
        if cached_rates:
            return cached_rates

        rates = self._fetch_exchange_rates(base_currency_str)

        self._rates_cache[base_currency_str] = rates
        self._cache_timestamp[base_currency_str] = datetime.now()

        return rates

    def convert(
        self,
        amount: Union[float, Decimal, str],
        from_currency: Union[str, Currency],
        to_currency: Union[str, Currency],
        base_currency: str = 'USD'
    ) -> Decimal:
        from_currency_str = normalize_currency(from_currency)
        to_currency_str = normalize_currency(to_currency)
        base_currency_str = normalize_currency(base_currency)

        if not is_valid_currency(from_currency_str):
            raise CurrencyNotFoundError(from_currency_str)
        if not is_valid_currency(to_currency_str):
            raise CurrencyNotFoundError(to_currency_str)

        try:
            amount_decimal = Decimal(str(amount))
            if amount_decimal < 0:
                raise InvalidAmountError("Сумма не может быть отрицательной")
        except:
            raise InvalidAmountError("Некорректная сумма")

        if from_currency_str == to_currency_str:
            return amount_decimal

        rates = self.get_exchange_rates(base_currency_str)

        if from_currency_str != base_currency_str:
            if from_currency_str not in rates:
                raise CurrencyNotFoundError(from_currency_str)
            amount_in_base = amount_decimal / rates[from_currency_str]
        else:
            amount_in_base = amount_decimal

        if to_currency_str not in rates:
            raise CurrencyNotFoundError(to_currency_str)

        converted_amount = amount_in_base * rates[to_currency_str]

        try:
            currency_enum = Currency(to_currency_str)
            currency_info = CURRENCIES.get(currency_enum)
            if currency_info:
                decimal_places = currency_info['decimal_places']
                converted_amount = converted_amount.quantize(
                    Decimal('1.' + '0' * decimal_places),
                    rounding=ROUND_HALF_UP
                )
        except ValueError:
            pass

        return converted_amount

_default_converter = CurrencyConverter()

def convert(
    amount: Union[float, Decimal, str],
    from_currency: Union[str, Currency],
    to_currency: Union[str, Currency]
) -> Decimal:
    return _default_converter.convert(amount, from_currency, to_currency)

def get_supported_currencies() -> List[str]:
    return [currency.value for currency in Currency]
