# NorthwindApp — система учета клиентов и заказов

## Назначение системы

Информационная система предназначена для автоматизации учета клиентов,
заказов, сотрудников и складских запасов малого торгового предприятия.
Система решает проблему разрозненного хранения данных и ручного оформления
заказов, предоставляя сотрудникам разных отделов (склад, кадры, менеджеры,
руководство) единый интерфейс с разграничением прав доступа. В результате
повышается скорость обработки заказов, снижается количество ошибок и
обеспечивается оперативное получение отчетности для принятия управленческих
решений.

## Участники команды и роли

| Участник | Роли |
|---|---|
| Бердникова Виолетта | Аналитик, Руководитель проекта, Тестировщик |
| Филатова Анастасия | Разработчик, Архитектор, Специалист по развертыванию |

## Трекер задач

- Репозиторий: https://github.com/anastasiafilatova7/NorthwindApp
- Issues: https://github.com/anastasiafilatova7/NorthwindApp/issues
- Projects: https://github.com/users/anastasiafilatova7/projects/1

## Технологический стек

- **Язык:** Python 3.13
- **GUI:** Tkinter (ttk)
- **СУБД:** PostgreSQL 16 (БД Northwind)
- **Драйвер БД:** psycopg2-binary 2.9.12
- **VCS:** Git + GitHub
- **IDE:** IDLE (Python)

## Структура проекта
NorthwindApp/
├── main.py # точка входа, окно авторизации
├── auth.py # проверка логина и пароля
├── db_config.py # параметры подключения к PostgreSQL
├── warehouse_window.py # интерфейс работника склада
├── personnel_window.py # интерфейс отдела кадров
├── manager_window.py # интерфейс менеджера
├── boss_window.py # интерфейс начальника (отчеты)
├── requirements.txt
└── README.md


## Запуск проекта

1. Установить PostgreSQL 16 и развернуть БД Northwind.
2. Установить зависимости: pip install -r requirements.txt
3. Проверить параметры подключения в `db_config.py`.
4. Запустить: python main.py


## Тестовые учетные записи

| Логин | Пароль | Роль |
|---|---|---|
| warehouse | warehouse1 | Работник склада |
| personnel | personnel1 | Отдел кадров |
| manager | manager1 | Менеджер |
| boss | boss1 | Начальник |


## Документация

### Анализ предметной области
- [As-Is процесс](docs/bpmn/as_is.png)
- [To-Be процесс](docs/bpmn/to_be.png)
- [Функциональные требования](docs/requirements/functional.md)
- [Нефункциональные требования](docs/requirements/non_functional.md)

### Архитектура
- [Контекстная диаграмма (C4 Level 1)](docs/architecture/context_diagram.png)
- [Компоненты системы (C4 Level 2)](docs/architecture/components.png)

### Модель данных
- [ER-диаграмма БД Northwind](docs/data/er_diagram.png)
- ER-диаграмма включает 6 ключевых сущностей: `customers`, `orders`, `order_details`, `products`, `categories`, `employees`. Модель нормализована до 3НФ.

### Архитектурные решения
- [ADR 001: Выбор СУБД — PostgreSQL](docs/adr/001_database_choice.md)
