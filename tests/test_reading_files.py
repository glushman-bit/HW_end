import csv
import json
from unittest.mock import mock_open
from unittest.mock import patch

import pandas as pd
import pytest

from src.reading_files import read_data_from_csv
from src.reading_files import read_data_from_excel
from src.reading_files import read_data_from_json


def test_csv_read():
    """Тест на правильность работы функции"""
    mock_csv_content = "id;amount;currency\n1;100;RUB\n2;200;USD\n"
    with patch("src.reading_files.Path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=mock_csv_content)
    ):
        result = read_data_from_csv("dummy.csv")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "1"
        assert result[1]["currency"] == "USD"


def test_csv_not_found():
    """Тест: ошибка при отсутствии csv-файла"""
    with patch("src.reading_files.Path.exists", return_value=False):
        fake_csv_content = "non.csv"
        with pytest.raises(FileNotFoundError):
            read_data_from_csv(fake_csv_content)


def test_csv_error_read():
    """Тест: ошибка чтения csv-файла"""
    with patch("src.reading_files.Path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data="error.csv")
    ), patch("csv.DictReader", side_effect=csv.Error):
        with pytest.raises(ValueError, match="Ошибка чтения CSV-файла"):
            read_data_from_csv("file.csv")


def test_csv_unknown_error():
    """Тест: неизвестная ошибка csv-файла"""
    with patch("src.reading_files.Path.exists", return_value=True), patch("builtins.open", side_effect=RuntimeError):
        with pytest.raises(RuntimeError, match="Неизвестная ошибка при чтении CSV"):
            read_data_from_csv("file.csv")


def test_excel_read():
    """Тест на правильность работы функции"""
    df = pd.DataFrame(
        [
            {"id": "3", "amount": "300", "currency": "EUR"},
            {"id": "4", "amount": "400", "currency": "GBP"},
        ]
    )
    with patch("src.reading_files.Path.exists", return_value=True), patch(
        "src.reading_files.pd.read_excel", return_value=df
    ):
        result = read_data_from_excel("dummy.xlsx")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["amount"] == "300"
        assert result[1]["currency"] == "GBP"


def test_excel_not_found(tmp_path):
    """Тест: ошибка при отсутствии xlsx-файла"""
    missing_file = tmp_path / "missing.xlsx"
    with pytest.raises(FileNotFoundError, match="Файл не найден"):
        read_data_from_excel(missing_file)


def test_xlsx_unknown_error():
    """Тест: неизвестная ошибка xlsx-файла"""
    with patch("src.reading_files.Path.exists", return_value=True), patch(
        "src.reading_files.pd.read_excel", side_effect=Exception
    ):
        with pytest.raises(RuntimeError, match="Неизвестная ошибка при чтении xlsx"):
            read_data_from_excel("file.csv")


def test_read_data_from_json_success():
    """Тест на правильность работы функции"""
    data = json.dumps(
        [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01",
                "operationAmount": {
                    "amount": "100",
                    "currency": {"name": "руб.", "code": "RUB"},
                },
                "description": "Перевод",
                "to": "Счет 123",
            }
        ]
    )

    with patch("builtins.open", mock_open(read_data=data)):
        result = read_data_from_json("operations.json")

    assert result == [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01",
            "amount": "100",
            "currency_name": "руб.",
            "currency_code": "RUB",
            "from": None,
            "to": "Счет 123",
            "description": "Перевод",
        }
    ]


def test_read_data_from_json_error():
    """Некорректный JSON"""
    with patch("builtins.open", mock_open(read_data="")):
        with pytest.raises(ValueError):
            read_data_from_json("operations.json")


def test_read_data_from_csv_not_found():
    """Файл не найден"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            read_data_from_json("operations.json")


def test_read_data_from_csv_not_list():
    """JSON не список"""
    data = json.dumps({"id": 1})

    with patch("builtins.open", mock_open(read_data=data)):
        with pytest.raises(ValueError):
            read_data_from_json("operations.json")
