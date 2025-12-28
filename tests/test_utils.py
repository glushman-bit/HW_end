from src.utils import count_all_by_category

def test_count_all_by_category_success():
    """Проверяем правильность работы функции"""
    transactions = [
        {"description": "Перевод"},
        {"description": "Перевод"},
        {"description": "открытие вклада"}
    ]
    categories = ["Перевод", "открытие вклада"]
    result = count_all_by_category(transactions, categories)
    assert result == {
        "Перевод": 2,
        "открытие вклада": 1
    }

