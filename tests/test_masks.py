import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


@pytest.fixture
def number_card():
    return ["1234567890", "1234567890123456", "1234567890123456789"]


@pytest.fixture
def mask_char():
    return ["*"]


@pytest.fixture
def group_size():
    return 4


""" Проверка правильности работы кода """


@pytest.mark.parametrize(
    "number_card, " "mask_char, " "group_size, " "expected", [("1234567890123456", "*", 4, "1234 56** **** 3456")]
)
def test_mask_card_origin_func(number_card, mask_char, group_size, expected):
    assert get_mask_card_number(number_card, mask_char, group_size=4) == expected


""" Проверка на нестандартную длину номера """


@pytest.mark.parametrize(
    "number_card," "expected", [("1234567890", "**** **78 90"), ("1234567890123456789", "1234 56** **** ***6 789")]
)
def test_mask_unusual_length_number(number_card: str, expected):
    assert get_mask_card_number(number_card) == expected


""" Проверка на вывод исключения при вводе пустой строки """


def test_length_number_card(number_card):
    with pytest.raises(ValueError):
        get_mask_card_number("")


""" Проверка на неверные длины номера """


@pytest.mark.parametrize(
    "number",
    [
        "",
        "1",
        "1234",
        "123456789",  # 9
        "12345678901",  # 11
        "1234567890123",  # 13
        "123456789012345",  # 15
        "12345678901234567",  # 17
        "123456789012345678",  # 18
        "12345678901234567890",  # > 19
    ],
)
def test_invalid_lengths(number):
    with pytest.raises(ValueError):
        get_mask_card_number(number)


@pytest.fixture
def number_account():
    return ["12345678901234567890"]


""" Проверка что номер состоит из чисел """


@pytest.mark.parametrize("number_account, " "expected", [("12345678901234567890", "**7890")])
def test_get_mask_account_all_digits(number_account: str, expected):
    assert get_mask_account(number_account) == expected


""" Проверка на вывод исключения при неверной длине номера счета """


def test_length_number_account() -> None:
    with pytest.raises(ValueError):
        get_mask_account("1234567890123456789")


""" Проверка что номер состоит из цифр """


def test_mask_number_non_digits() -> None:
    with pytest.raises(ValueError):
        get_mask_account("1234abcd5678")
        get_mask_card_number("1234abcd5678")
