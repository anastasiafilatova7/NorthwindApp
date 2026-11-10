import pytest
from auth import authenticate

def test_authenticate_success():
    """Позитивный тест: верный логин и пароль для всех 4 ролей."""
    assert authenticate('manager', 'manager1') == 'manager'
    assert authenticate('boss', 'boss1') == 'boss'
    assert authenticate('warehouse', 'warehouse1') == 'warehouse'
    assert authenticate('personnel', 'personnel1') == 'personnel'

def test_authenticate_wrong_password():
    """Негативный тест: верный логин, но неверный пароль."""
    assert authenticate('manager', 'wrongpassword') is None
    assert authenticate('warehouse', '12345') is None
    assert authenticate('boss', 'boss123') is None

def test_authenticate_unknown_user():
    """Негативный тест: пользователя не существует."""
    assert authenticate('unknown_user', 'somepassword') is None
    assert authenticate('admin', 'admin') is None

def test_authenticate_empty_values():
    """Граничный случай: пустые строки."""
    assert authenticate('', '') is None
    assert authenticate(None, None) is None

def test_authenticate_register_sensitive():
    """Граничный случай: проверка регистра (логин должен быть строго с маленькой буквы)."""
    assert authenticate('Manager', 'manager1') is None
    assert authenticate('BOSS', 'boss1') is None
