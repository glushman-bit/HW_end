from typing import Iterator

from src.decorators import log


@log()
def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """Фильтрует транзакции по коду валюты."""
    currency_gen = (
        transaction
        for transaction in transactions if transaction.get("currency_code", {}) == currency
    )
    return currency_gen


@log()
def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """Генератор, который по очереди выдаёт описание транзакций.
    Если у транзакции нет поля description — пропускает её."""
    for tx in transactions:
        description = tx.get("description")
        if description is not None:
            yield description


@log()
def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генератор банковских карт.который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX"""
    if start > stop or start == stop:
        raise ValueError("Ошибка. Неверные значения диапазона")
    for num in range(start, stop + 1):
        # Преобразуем число в 16-значную строку с ведущими нулями
        digits = f"{num:016d}"
        # Форматируем по 4 цифры
        formatted = f"{digits[:4]} {digits[4:8]} {digits[8:12]} {digits[12:]}"
        yield formatted
