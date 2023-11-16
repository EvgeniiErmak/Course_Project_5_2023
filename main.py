from utils import create_table, add_to_table, add_top_companies_and_vacancies
from db_manager import DBManager


def main():
    db_manager = DBManager()

    # Перенесено в utils.py
    create_table()

    # Добавление топ 10 компаний и 10 вакансий от каждой компании
    add_top_companies_and_vacancies()

    while True:
        task = input(
                    "Меню:\n"
                    "1. Получить список компаний и количество вакансий.\n"
                    "2. Получить список всех вакансий с указанием названия компании и зарплаты.\n"
                    "3. Получить среднюю зарплату по вакансиям.\n"
                    "4. Получить список вакансий с зарплатой выше средней.\n"
                    "5. Поиск вакансий по ключевому слову.\n"
                    "0. Завершить программу.\n"
                    )

        if task == '0':
            break
        elif task == '1':
            print(db_manager.get_companies_and_vacancies_count())
            print()
        elif task == '2':
            print(db_manager.get_all_vacancies())
            print()
        elif task == '3':
            print(db_manager.get_avg_salary())
            print()
        elif task == '4':
            print(db_manager.get_vacancies_with_higher_salary())
            print()
        elif task == '5':
            keyword = input('Введите ключевое слово: ')
            print(db_manager.get_vacancies_with_keyword(keyword))
            print()
        else:
            print('Неправильный запрос')


if __name__ == "__main__":
    create_table()
    add_top_companies_and_vacancies()
    main()
