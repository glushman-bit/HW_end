import logging

from src.decorators import log

logger = logging.getLogger("masks.log")
logger.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler("../logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: - %(message)s")
# file_handler.setFormatter(file_formatter)
# logger.addHandler(file_handler)


@log()
def get_mask_card_number(number_card: str, mask_char: str = "*", group_size: int = 4) -> str:
    # Проверяем что номер состоит из цифр
    if not number_card.isdigit():
        raise ValueError("Номер должен содержать только цифры")

    length = len(number_card)
    # Исключаем номера не верной длинны
    if length not in (10, 16, 19):
        logger.error(f"Неверная длинна номера карты: {length} цифр")
        raise ValueError("Неверная длина номера карты")
    if length == 0:
        logger.error("Ничего не введено")
        raise ValueError("Ничего не введено")
    # Маскировка номера длинной 10
    if length == 10:
        mask_section = mask_char * (len(number_card) - 4)
        mask_number = mask_section + number_card[-4:]
    # Маскировка номеров длинной 16 и 19
    else:
        mask_section = mask_char * (len(number_card) - 10)
        mask_number = number_card[:6] + mask_section + number_card[-4:]
    # Группировка номера
    group_number = " ".join([mask_number[i : i + group_size] for i in range(0, len(mask_number), group_size)])
    logger.info("Успешный ввод номера карты.")

    return group_number




@log()
def get_mask_account(number_account: str, mask_char: str = "*") -> str:
    """Функция, скрывающая номер банковского счета"""
    if not number_account.isdigit():
        logger.error("Неверный номер карты")
        raise ValueError("Номер должен содержать только цифры")

    mask_part = mask_char * 2
    # указывает сколько символов перед открытым номером
    mask_number = mask_part + number_account[-4:]

    if len(number_account) != 20:
        logger.error(f"Неверная длинна номера счета: {len(number_account)} цифр")
        raise ValueError("Введен не верный номер")

    logger.info("Успешный ввод номера счета.")

    return mask_number


