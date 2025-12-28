
def count_all_by_category(transactions, categories):
    """
    Функция подсчета количества операций по категориям
    :param transactions: Список словарей транзакции
    :param categories: Категории
    :return: Словарь количества по категориям
    """
    categories_map = {cat.lower(): cat for cat in categories}
    result = {cat: 0 for cat in categories}

    for trans in transactions:
        description = trans.get("description", "").lower()
        if description in categories_map:
            original_category = categories_map[description]
            result[original_category] += 1

    return result

