from typing import List, Dict
from collections import Counter

def count_all_by_category(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Функция подсчета количества операций по категориям
    :param transactions: Список словарей транзакции
    :param categories: Категории
    :return: Словарь количества по категориям
    """
    descriptions = [trans.get("description", "").lower() for trans in transactions]

    counter = Counter(descriptions)

    result = {cat: counter.get(cat.lower(), 0) for cat in categories}

    return result
