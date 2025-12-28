
from src.word_find import filter_by_word


def test_word_find_success():
    """Проверяем правильность работы"""
    data = [
        {"description": "Перевод с карты на счет"},
        {"description": "перевод между картами"},
        {"description": "Открытие счета"}
    ]
    result = filter_by_word(data, "перевод")
    assert result == [
        {"description": "Перевод с карты на счет"},
        {"description": "перевод между картами"}
    ]


def test_word_find_simbols():
    """Тест на правильность отображения символов"""
    data = [
        {"description": "Перевод (карта -> счет)"},
        {"description": "Открытие счета"}
    ]
    result = filter_by_word(data, "счет)")
    assert result == [
        {"description": "Перевод (карта -> счет)"}]

def test_word_find_empty():
    """Проверяем на пустой файл"""
    data = []
    result = filter_by_word(data, "счет)")
    assert result == []