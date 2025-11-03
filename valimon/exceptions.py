class ValimonError(Exception):
    pass

class CurrencyNotFoundError(ValimonError):
    def __init__(self, currency_code: str):
        self.currency_code = currency_code
        super().__init__(f"Валюта '{currency_code}' не найдена")

class InvalidAmountError(ValimonError):
    pass

class APIError(ValimonError):
    pass
