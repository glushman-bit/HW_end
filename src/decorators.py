from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable
from typing import Optional

log_folder = Path(__file__).parent.parent / "logs"
log_folder.mkdir(parents=True, exist_ok=True)
log_file = log_folder / "mylog.txt"
# создание файла mylog.txt в директории logs


def write_to_file(content: str, log_file: Optional[str]) -> None:
    """Функция записи log-файла"""
    if log_file:
        with open(log_file, "a", encoding="utf-8") as file:
            file.write(content + "\n")
    else:
        print(content)


def log(filename: Optional[str] = log_file) -> Callable:
    """Декоратор, который создает log-и на работу функции и ее результат в файл или консоль."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            datetime.now()
            try:
                result = func(*args, **kwargs)
                datetime.now()
                result_log = f"{func.__name__} ok."
                write_to_file(result_log, filename)
                return result
            except Exception as e:
                error_log = f"{func.__name__}: {type(e).__name__}: {e}"
                write_to_file(error_log, filename)
                raise

        return wrapper

    return decorator


def my_func(x, y):
    """Функция для проверки декоратора"""
    return x + y
