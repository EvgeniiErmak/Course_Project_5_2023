import os

DB_CREDS = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': os.environ.get('DB_PASS', 'postgres'),
    'port': 5433,
    'client_encoding': 'utf-8',
}