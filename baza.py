import psycopg2
from psycopg2 import sql
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

parms = {
    "dbname": "users_bd",
    "user": "salamat",
    "password": "QWE123",
    "host": "localhost",
    "port": "5432"
}

logging.info("старт")

try:
    with psycopg2.connect(**parms) as baza:
        cursor = baza.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(30),
                telegram_id BIGINT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                message_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        baza.commit()
        logging.info("БАЗА ДАННЫХ СОЗДАНА")
except Exception as e:
    logging.error("Ошибка при создании базы данных: %s", e)
