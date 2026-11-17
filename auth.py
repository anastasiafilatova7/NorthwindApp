"""Модуль авторизации пользователей"""
def authenticate(username, password):
    """Проверяет логин и пароль пользователя, возвращает его роль"""
    # проверка логина и пароля пользователя
    # cписок допустимых пользователей и их ролей
    users = {
        "warehouse": "warehouse1",
        "personnel": "personnel1",
        "manager": "manager1",
        "boss": "boss1",
    }

    if username in users and users[username] == password:
        return username  # возвращаем роль пользователя
    return None
