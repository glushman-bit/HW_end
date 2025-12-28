import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")


def converter_currency(transaction: float, currency: str) -> float:
    """Функция конвертации валюты в рубли"""

    currency_convert = ["USD", "EUR"]

    if not isinstance(transaction, (int, float)):
        # Проверка, что transaction число
        raise ValueError("Введена неверная сумма транзакции")

    if transaction < 0:
        # Проверка ввод отрицательного числа
        raise ValueError("Сумма транзакции не может быть отрицательной")

    if currency not in currency_convert:
        # Проверка на введенный код валюты
        raise ValueError("Код валюты не поддерживается")

    if currency in currency_convert:

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={transaction}"

        params = {
            "to": "RUB",
            "from": currency,
            "amount": transaction,
        }
        headers = {"apikey": API_KEY}

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            # Проверка на ошибки запроса
            raise Exception(f"Ошибка запроса: {response.status_code}")

        response_json = response.json()

        result: float = round(response_json["result"], 2)
        return result

    return transaction
