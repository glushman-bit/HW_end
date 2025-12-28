import pytest

from src.processing import filter_by_state
from src.processing import sorted_by_date


@pytest.fixture
def filtered_list() -> list:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


""" Тестирование фильтрации списка словарей по заданному статусу state """


def test_filter_by_state_default(filtered_list):
    assert filter_by_state(filtered_list) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


""" Проверка при отсутствии словарей с указанным статусом state в списке """


def test_filter_by_state_none_found(filtered_list):
    assert filter_by_state(filtered_list, "CANCEL") == []


""" Проверка при передаче пустого списка """


def test_filter_empty_list():
    assert filter_by_state([], "CANCELED") == []


@pytest.fixture
def date():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


""" Проверка сортировки по возрастанию и убыванию """


def test_sorted_by_date_real_data_ascending(date) -> bool:
    assert sorted_by_date(date, ascending=True)
    assert sorted_by_date(date, ascending=False)


""" Проверка при сортировке пустого списка """


def test_sorted_by_date_empty_list() -> None:
    assert filter_by_state([]) == []
