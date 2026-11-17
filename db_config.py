"""Модуль конфигурации подключения к бд PostgreSQL"""
import psycopg2
# параметры подключения
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "Northwind",
    "user": "postgres",
    "password": "12345",
}


def get_connection():
    """Возвращает соединение с бд"""
    return psycopg2.connect(**DB_CONFIG)  # возвращает соединение с базой данных
