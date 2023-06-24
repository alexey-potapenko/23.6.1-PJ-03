import json
import requests
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        # Обработка ошибок ввода
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        if base == quote:
            raise ConvertionException('Невозможно перевести одинаковые валюты')

        # Конец обработчика ошибок ввода

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_quote = json.loads(r.content)[keys[quote]] * amount

        return total_quote

