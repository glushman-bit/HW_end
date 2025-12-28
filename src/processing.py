from typing import Iterable

from src.decorators import log


@log()
def filter_by_state(local_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция возвращающая отфильтрованный по статусу список"""
    filtered_list: list = []
    for item in local_list:
        if item.get("state") == state:
            filtered_list.append(item)
    return filtered_list


@log()
def sorted_by_date(local_list: Iterable[dict], ascending: bool = True) -> list[dict]:
    """Функция сортировки по дате"""
    return sorted(local_list, key=lambda item: item["date"], reverse=ascending)
