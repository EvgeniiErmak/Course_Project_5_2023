import psycopg2
import requests


def get_vacancies(employer_id):
    """Получение данных вакансий по API"""

    params = {
        'area': 1,
        'page': 0,
        'per_page': 10
    }
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    data_vacancies = requests.get(url, params=params).json()

    vacancies_data = []
    for item in data_vacancies["items"]:
        hh_vacancies = {
            'vacancy_id': int(item['id']),
            'vacancies_name': item['name'],
            'payment': item["salary"]["from"] if item.get("salary") else None,
            'requirement': item['snippet']['requirement'],
            'vacancies_url': item['alternate_url'],
            'employer_id': employer_id
        }
        if hh_vacancies['payment'] is not None:
            vacancies_data.append(hh_vacancies)

    return vacancies_data


def get_employer(employer_id):
    """Получение данных о работодателях по API"""

    url = f"https://api.hh.ru/employers/{employer_id}"
    data_vacancies = requests.get(url).json()
    hh_company = {
        "employer_id": int(employer_id),
        "company_name": data_vacancies['name'],
        "open_vacancies": data_vacancies.get('open_vacancies', 0)
    }

    return hh_company


def create_database():
    """Создание базы данных, если её нет"""

    conn = psycopg2.connect(host="localhost", database="postgres",
                            user="postgres", password="12345", client_encoding="utf-8")
    conn.autocommit = True
    cur = conn.cursor()

    # Проверка существования базы данных
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", ('course_work_5',))
    exists = cur.fetchone()

    if not exists:
        # Создание базы данных, если она не существует
        cur.execute("CREATE DATABASE course_work_5")

    conn.close()

def create_table():
    """Создание таблиц, если их ещё нет"""

    create_database()

    conn = psycopg2.connect(host="localhost", database="course_work_5",
                            user="postgres", password="12345", client_encoding="utf-8")
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS employers (
                    employer_id INTEGER PRIMARY KEY,
                    company_name varchar(255),
                    open_vacancies INTEGER
                    )""")

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    vacancies_name varchar(255),
                    payment INTEGER,
                    requirement TEXT,
                    vacancies_url TEXT,
                    employer_id INTEGER REFERENCES employers(employer_id)
                    )""")
    conn.commit()
    conn.close()


def add_to_table(employers_list):
    """Заполнение базы данных компании и вакансии"""

    with psycopg2.connect(host="localhost", database="course_work_5",
                          user="postgres", password="12345", client_encoding="utf-8") as conn:
        with conn.cursor() as cur:
            for employer_id in employers_list:
                # Получение данных о компании по API
                employer_data = get_employer(employer_id)

                # Добавление компании в таблицу с игнорированием конфликта
                cur.execute('INSERT INTO employers (employer_id, company_name, open_vacancies) '
                            'VALUES (%s, %s, %s) ON CONFLICT DO NOTHING RETURNING employer_id',
                            (employer_data['employer_id'], employer_data['company_name'],
                             employer_data['open_vacancies']))

                # Получение вакансий для компании по API
                vacancies_list = get_vacancies(employer_id)

                for v in vacancies_list:
                    # Добавление вакансии в таблицу с игнорированием конфликта
                    cur.execute('INSERT INTO vacancies (vacancy_id, vacancies_name, '
                                'payment, requirement, vacancies_url, employer_id) '
                                'VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
                                (v['vacancy_id'], v['vacancies_name'], v['payment'],
                                 v['requirement'], v['vacancies_url'], v['employer_id']))

        conn.commit()


def add_top_companies_and_vacancies():
    """Добавляет топ 10 компаний и вакансии от каждой компании в базу данных"""

    top_companies = [1740, 15478, 8620, 3529, 78638, 4006, 4504679, 561525, 64174, 8642172]

    for employer_id in top_companies:
        employer_data = get_employer(employer_id)
        vacancies_list = get_vacancies(employer_id)

        # Добавление компании в таблицу с игнорированием конфликта
        with psycopg2.connect(host="localhost", database="course_work_5",
                              user="postgres", password="12345", client_encoding="utf-8") as conn:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO employers (employer_id, company_name, open_vacancies) '
                            'VALUES (%s, %s, %s) ON CONFLICT DO NOTHING RETURNING employer_id',
                            (employer_data['employer_id'], employer_data['company_name'],
                             employer_data['open_vacancies']))

                for v in vacancies_list:
                    # Добавление вакансии в таблицу с игнорированием конфликта
                    cur.execute('INSERT INTO vacancies (vacancy_id, vacancies_name, '
                                'payment, requirement, vacancies_url, employer_id) '
                                'VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
                                (v['vacancy_id'], v['vacancies_name'], v['payment'],
                                 v['requirement'], v['vacancies_url'], v['employer_id']))

        conn.commit()
