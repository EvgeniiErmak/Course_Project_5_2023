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
            "Введите 1, чтобы получить список всех компаний и количество вакансий у каждой компании\n"
            "Введите 2, чтобы получить список всех вакансий с указанием названия компании, "
            "названия вакансии и зарплаты и ссылки на вакансию\n"
            "Введите 3, чтобы получить среднюю зарплату по вакансиям\n"
            "Введите 4, чтобы получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
            "Введите 5, чтобы получить список всех вакансий, в названии которых содержатся переданные в метод слова\n"
            "Введите Стоп, чтобы завершить работу\n"
        )

        if task == "Стоп":
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
