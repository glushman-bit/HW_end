
print("""
Программа: Привет! Добро пожаловать в программу работы 
с банковскими транзакциями. 
""")

import os
from src.reading_files import read_data_from_excel
from src.reading_files import read_data_from_csv
from src.reading_files import read_data_from_json
from src.processing import filter_by_state, sorted_by_date
from src.generators import filter_by_currency
from src.word_find import filter_by_word
from src.widget import get_date, mask_account_card
from typing import Callable

BASE_DIR = os.path.dirname(__file__)

dict_choose_file = {
    1: read_data_from_json,
    2: read_data_from_csv,
    3: read_data_from_excel
}
path_choose_file = {
    1: BASE_DIR + "/data/operations.json",
    2: BASE_DIR + "/data/transactions.csv",
    3: BASE_DIR + "/data/transactions_excel.xlsx"
}
STATUS = ["EXECUTED", "CANCELED", "PENDING"]

def main():
    while True:
        print(
            "Выберете необходимый пункт меню:\n"
            "1: Получить информацию о транзакциях из JSON-файла\n"
            "2: Получить информацию о транзакциях из CSV-файла\n"
            "3: Получить информацию о транзакциях из XLSX-файла"
        )
        user_input: int = int(input())
        get_func: Callable | None = dict_choose_file.get(user_input)
        if dict_choose_file.get(user_input):
            print(get_func.__doc__)
            path_: str = path_choose_file.get(user_input)
            transaction = get_func(path_)
            break

    while True:
        print ("Введите статус, по которому необходимо выполнить фильтрацию.\n" 
                f"Доступные для фильтровки статусы: {', '.join(STATUS)}" )
        user_input_status = input().upper()

        if user_input_status in STATUS:
            transaction = filter_by_state(transaction, user_input_status)
            print(f"Операции отфильтрованы по статусу '{user_input_status}'")
            break
        else:
            print(f"Статус операции '{user_input_status}' недоступен.")

    print("Отсортировать операции по дате? Да/Нет")
    user_input: bool = input().lower() == "да"
    if user_input:
        print("Отсортировать по возрастанию или по убыванию?")
        user_sort_reverse: bool = input().lower() == "по убыванию"
        transaction = sorted_by_date(transaction, user_sort_reverse)

    print("Выводить только рублевые транзакции? Да/Нет")
    user_input: bool = input().lower() == "да"
    if user_input:
        transaction = list(filter_by_currency(transaction, "RUB"))


    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    user_input: bool = input().lower() == "да"
    if user_input:
        print("Введите слово для фильтрации: ")
        user_word: str = input()
        transaction = filter_by_word(transaction, user_word)

    print("Распечатываю итоговый список транзакций...")

    print(f"Всего банковских операций в выборке: {len(transaction)}")

    for trans in transaction:
        state = trans.get("state")
        date = get_date(trans.get("date"))
        amount = trans.get("amount")
        currency_name = trans.get("currency_name")
        currency_code = trans.get("currency_code")
        to_from = trans.get("from") if isinstance(trans.get("from"), str) else None
        to = mask_account_card(trans.get("to"))
        description = trans.get("description")

        out_print = f"{date} {description}"
        check_to = f"{to}"
        check_from = " -> " + mask_account_card(to_from) if to_from else ""
        summ_print = f"Сумма: {amount} {currency_code}"
        print(f"{out_print}\n{check_to}{check_from}\n{summ_print}")


if __name__ == '__main__':
    main()