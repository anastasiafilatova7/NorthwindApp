from db_config import DB_CONFIG

def test_db_config_keys():
    """Проверяем, что в конфигурации есть все нужные ключи."""
    required_keys = ['host', 'port', 'database', 'user', 'password']
    for key in required_keys:
        assert key in DB_CONFIG

def test_db_config_values():
    """Проверяем базовые значения конфигурации."""
    assert DB_CONFIG['host'] == 'localhost'
    assert DB_CONFIG['port'] == 5432
    assert DB_CONFIG['database'] == 'Northwind'
