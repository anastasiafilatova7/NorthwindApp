import psycopg2
from db_config import get_connection

def authenticate(username, password):
    #проверка логина и пароля пользователя
    #cписок допустимых пользователей и их ролей
    users = {'warehouse': 'warehouse1', 'personnel': 'personnel1',
'manager': 'manager1', 'boss': 'boss1'}
    
    if username in users and users[username] == password:
        return username  #возвращаем роль пользователя
    return None
