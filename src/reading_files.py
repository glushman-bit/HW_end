import csv
import json
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union, Callable
import logging

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
    """ Для обработки выбран CSV-файл. """
    try:
        #logger.info(f"открытие файла {csv_path}")
        with open(csv_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")

            return list(reader)

    except FileNotFoundError:
        #logger.error(f"Файл {csv_path} не найден.")
        raise FileNotFoundError(f"Файл {csv_path} не найден.")

    except csv.Error as e:
        #logger.error(f"Ошибка чтения CSV-файла: {e}")
        raise ValueError(f"Ошибка чтения CSV-файла: {e}")

    except Exception as e:
        #logger.error(f"Неизвестная ошибка при чтении CSV: {e}")
        raise RuntimeError(f"Неизвестная ошибка при чтении CSV: {e}")


def read_data_from_excel(xlsx_path: Union[Path, str]) -> List[Dict[str, str]]:
    """ Для обработки выбран XLSX-файл. """
    try:
        #logger.info(f"открытие файла {xlsx_path}")
        df: DataFrame = pd.read_excel(xlsx_path)
        return df.to_dict(orient="records")

    except FileNotFoundError:
        #logger.error(f"Файл {xlsx_path} не найден.")
        raise FileNotFoundError("Файл не найден: {xl_path}")

    except Exception as e:
        #logger.error(f"Неизвестная ошибка при чтении xlsx: {e}")
        raise RuntimeError(f"Неизвестная ошибка при чтении xlsx: {e}")

