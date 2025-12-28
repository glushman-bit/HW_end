from datetime import datetime

from src.decorators import log
from src.masks import get_mask_account
from src.masks import get_mask_card_number


@log()
def mask_account_card(number_account: str) -> str:
    """Функция обработки информации о картах и счетах"""

    # убираем пробелы по краям строки
    number_account = number_account.strip()
    # разбиваем строку на части по пробелам
    parts = number_account.split()
    # выделяем часть с номером по последнему индексу
    number_part = parts[-1]
    # соединяем части слов
    name_part = " ".join(parts[:-1])
    # if not number_part.isdigit():
    #     raise ValueError("Номер должен содержать только цифры")
    if len(number_part.strip()) == 0:
        raise ValueError("Ничего не введено")
    if "счет" in name_part.lower():  # определяем что это счет
        return f"{name_part} {get_mask_account(number_part)}"
    else:
        return f"{name_part} {get_mask_card_number(number_part)}"


@log()
def get_date(date_str: str) -> str:
    """Функция преобразования даты"""
    date_obj = datetime.fromisoformat(date_str)
    return date_obj.strftime("%d.%m.%Y")
