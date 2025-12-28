import re


def filter_by_word(data: List[Dict], search: str) -> List[Dict]:
    """
    Фильтрует список банковских операций по вхождению строки поиска в описание.

    :param data: список словарей с операциями
    :param search: строка поиска
    :return: список операций, в описании которых есть строка поиска
    """
    if not search:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    result = []
    for operation in data:
        description = operation.get("description", "")
        if isinstance(description, str) and pattern.search(description):
            result.append(operation)

    return result



