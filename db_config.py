import psycopg2
from psycopg2 import sql

#параметры подключения
DB_CONFIG = {'host': 'localhost', 'port': 5432, 'database': 'Northwind',
'user': 'postgres', 'password': '12345'}

def get_connection():
    return psycopg2.connect(**DB_CONFIG) #возвращает соединение с базой данных
