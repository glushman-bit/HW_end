import json

def read_data_from_json(json_path: Union[Path, str]) -> List[Dict]:
    """ Для обработки выбран JSON-файл. """
    try:
        #logger.info(f"открытие файла {json_path}")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            # logger.error("JSON-файл должен содержать список")
            raise ValueError("JSON-файл должен содержать список")

        result = []

        for item in data:
            if not item:
                continue
            result.append({
                "id": item["id"],
                "state": item["state"],
                "date": item["date"],
                "amount": item["operationAmount"]["amount"],
                "currency_name": item["operationAmount"]["currency"]["name"],
                "currency_code": item["operationAmount"]["currency"]["code"],
                "from": item.get("from"),
                "to": item["to"],
                "description": item["description"]
            })

        return result

    except FileNotFoundError:
        #logger.error(f"Файл {json_path} не найден.")
        raise FileNotFoundError(f"Файл {json_path} не найден.")

    except json.JSONDecodeError as e:
        #logger.error(f"Ошибка чтения JSON-файла: {e}")
        raise ValueError(f"Ошибка чтения JSON-файла: {e}")

    except KeyError as e:
        #logger.error(f"Неизвестная ошибка при чтении JSON {e}")
        raise ValueError(f"Неизвестная ошибка при чтении JSON: {e}")



