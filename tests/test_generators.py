from types import GeneratorType

import pytest

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions

""" Входные данные для проверки работы генератора фильтрации по валюте."""
transactions_sample_currency = [
    {
        "id": 939719570,
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
    },
    {
        "id": 142264268,
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
    },
    {
        "id": 873106923,
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
    },
]


def test_filter_by_currency_usd() -> None:
    """Проверяем, что правильно возвращаются только USD-транзакции."""
    result = list(filter_by_currency(transactions_sample_currency, "USD"))

    assert len(result) == 2
    assert result[0]["id"] == 939719570
    assert result[1]["id"] == 142264268


def test_filter_by_currency_rub() -> None:
    """Проверяем фильтрацию по RUB."""
    result = list(filter_by_currency(transactions_sample_currency, "RUB"))
    assert len(result) == 1
    assert result[0]["id"] == 873106923


def test_filter_by_currency_no_matches() -> None:
    """Нет транзакций с заданной валютой."""
    result = list(filter_by_currency(transactions_sample_currency, "EUR"))
    assert result == []


def test_filter_by_currency_empty_list() -> None:
    """Генератор должен работать без ошибок на пустом списке."""
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_filter_by_currency_is_generator() -> None:
    """Проверяем, что функция возвращает генератор."""
    gen = filter_by_currency(transactions_sample_currency, "USD")
    assert isinstance(gen, GeneratorType)


transactions_sample_descriptions = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод с карты на карту"},
    {"description": "Перевод организации"},
]


def test_transaction_descriptions_basic() -> None:
    """Проверяем корректную выдачу описаний по очереди."""
    gen = transaction_descriptions(transactions_sample_descriptions)

    result = [next(gen) for _ in range(5)]

    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


def test_transaction_descriptions_skips_empty() -> list[dict]:
    """Если description нет — генератор должен пропустить транзакцию."""
    data = [
        {"description": "Есть"},
        {"id": 123},  # description нет → пропускаем
        {"description": "Есть2"},
    ]

    result = list(transaction_descriptions(data))

    assert result == ["Есть", "Есть2"]


def test_transaction_descriptions_empty_list() -> None:
    """Пустой список не должен вызывать ошибок."""
    result = list(transaction_descriptions([]))
    assert result == []


def test_transaction_descriptions_is_generator() -> None:
    """Возвращаемый объект должен быть генератором."""
    gen = transaction_descriptions(transactions_sample_descriptions)
    from types import GeneratorType

    assert isinstance(gen, GeneratorType)


@pytest.fixture
def simple_range() -> list[str]:
    return list(card_number_generator(1, 5))


"""Проверяем правильность номеров в заданном диапазоне"""


def test_generator_count(simple_range) -> None:
    assert len(simple_range) == 5


"""Проверяем правильность формата XXXX XXXX XXXX XXXX"""


def test_format_of_card_number(simple_range) -> None:
    for number in simple_range:
        parts = number.split()
        assert len(parts) == 4
        assert all(len(part) == 4 for part in parts)


"""Проверяем ведущие нули"""


def test_leading_zeros() -> None:
    result = next(card_number_generator(1, 5))
    assert result == "0000 0000 0000 0001"


"""Проверяем последовательную генерацию нескольких значений"""


def test_sequence_values() -> None:
    numbers = list(card_number_generator(9, 11))
    assert numbers == [
        "0000 0000 0000 0009",
        "0000 0000 0000 0010",
        "0000 0000 0000 0011",
    ]


"""Проверяем работу при старте с нуля и минимальное значение номера"""


def test_zero_start_min_number_card() -> None:
    numbers = list(card_number_generator(0, 2))
    assert numbers == [
        "0000 0000 0000 0000",
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
    ]


"""Проверяем работу при максимальном значении номера"""


def test_max_number_card() -> None:
    num = 9999999999999999
    result = next(card_number_generator(num, num + 1))
    assert result == "9999 9999 9999 9999"


"""Проверка при одинаковых значениях начала и конца"""


def test_error_when_start_equals_end() -> None:
    with pytest.raises(ValueError):
        list(card_number_generator(5, 5))


"""Проверка если значение начала выше значения конца"""


def test_error_when_start_greater_than_end() -> None:
    with pytest.raises(ValueError):
        list(card_number_generator(10, 5))
