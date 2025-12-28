import csv
import json
import logging
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

csv_path = DATA_DIR / "transactions.csv"
xlsx_path = DATA_DIR / "transactions_excel.xlsx"
json_path = DATA_DIR / "operations.json"

# logger = logging.getLogger("reading_file.log")
# logger.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler("../logs/reading_file.log", mode="w", encoding="utf-8")
# file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: - %(message)s")
# file_handler.setFormatter(file_formatter)
# logger.addHandler(file_handler)


def read_data_from_csv(csv_path: Union[Path, str]) -> List[Dict[str, str]]:
    """Для обработки выбран CSV-файл."""
    try:
        # logger.info(f"открытие файла {csv_path}")
        with open(csv_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")

            return list(reader)

    except FileNotFoundError:
        # logger.error(f"Файл {csv_path} не найден.")
        raise FileNotFoundError(f"Файл {csv_path} не найден.")

    except csv.Error as e:
        # logger.error(f"Ошибка чтения CSV-файла: {e}")
        raise ValueError(f"Ошибка чтения CSV-файла: {e}")

    except Exception as e:
        # logger.error(f"Неизвестная ошибка при чтении CSV: {e}")
        raise RuntimeError(f"Неизвестная ошибка при чтении CSV: {e}")


def read_data_from_excel(xlsx_path: Union[Path, str]) -> List[Dict[str, str]]:
    """Для обработки выбран XLSX-файл."""
    try:
        # logger.info(f"открытие файла {xlsx_path}")
        df: DataFrame = pd.read_excel(xlsx_path)
        return df.to_dict(orient="records")

    except FileNotFoundError:
        # logger.error(f"Файл {xlsx_path} не найден.")
        raise FileNotFoundError("Файл не найден: {xl_path}")

    except Exception as e:
        # logger.error(f"Неизвестная ошибка при чтении xlsx: {e}")
        raise RuntimeError(f"Неизвестная ошибка при чтении xlsx: {e}")


def read_data_from_json(json_path: Union[Path, str]) -> List[Dict]:
    """Для обработки выбран JSON-файл."""
    try:
        # logger.info(f"открытие файла {json_path}")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            # logger.error("JSON-файл должен содержать список")
            raise ValueError("JSON-файл должен содержать список")

        result = []

        for item in data:
            if not item:
                continue
            result.append(
                {
                    "id": item["id"],
                    "state": item["state"],
                    "date": item["date"],
                    "amount": item["operationAmount"]["amount"],
                    "currency_name": item["operationAmount"]["currency"]["name"],
                    "currency_code": item["operationAmount"]["currency"]["code"],
                    "from": item.get("from"),
                    "to": item["to"],
                    "description": item["description"],
                }
            )

        return result

    except FileNotFoundError:
        # logger.error(f"Файл {json_path} не найден.")
        raise FileNotFoundError(f"Файл {json_path} не найден.")

    except json.JSONDecodeError as e:
        # logger.error(f"Ошибка чтения JSON-файла: {e}")
        raise ValueError(f"Ошибка чтения JSON-файла: {e}")

    except KeyError as e:
        # logger.error(f"Неизвестная ошибка при чтении JSON {e}")
        raise ValueError(f"Неизвестная ошибка при чтении JSON: {e}")
