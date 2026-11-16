# Словарь данных проекта NorthwindApp

## 1. Таблица `customers` (Клиенты)

| Столбец | Тип данных | Описание | Ограничения |
|---|---|---|---|
| customer_id | VARCHAR(5) | Уникальный код клиента (например, VINET) | PRIMARY KEY, NOT NULL |
| company_name | VARCHAR | Название компании | NOT NULL |
| contact_name | VARCHAR | Имя контактного лица | NULL |
| city | VARCHAR | Город | NULL |
| country | VARCHAR | Страна | NULL |

## 2. Таблица `categories` (Категории)

| Столбец | Тип данных | Описание | Ограничения |
|---|---|---|---|
| category_id | INTEGER | ID категории | PRIMARY KEY, NOT NULL |
| category_name | VARCHAR | Название категории | NOT NULL |
| description | TEXT | Описание категории | NULL |

## 3. Таблица `products` (Продукты)

| Столбец | Тип данных | Описание | Ограничения |
|---|---|---|---|
| product_id | INTEGER | ID продукта | PRIMARY KEY, NOT NULL |
| product_name | VARCHAR | Название продукта | NOT NULL |
| category_id | INTEGER | ID категории | FOREIGN KEY, NULL |
| unit_price | NUMERIC(10,2) | Цена за единицу | CHECK (unit_price >= 0) |
| units_in_stock | INTEGER | Количество на складе | CHECK (units_in_stock >= 0) |
| discontinued | INTEGER | Статус (0 - активен, 1 - снят) | NOT NULL |

## 4. Таблица `employees` (Сотрудники)

| Столбец | Тип данных | Описание | Ограничения |
|---|---|---|---|
| employee_id | INTEGER | ID сотрудника | PRIMARY KEY, NOT NULL |
| last_name | VARCHAR | Фамилия | NOT NULL |
| first_name | VARCHAR | Имя | NOT NULL |
| title | VARCHAR | Должность | NULL |
| city | VARCHAR | Город | NULL |
| country | VARCHAR | Страна | NULL |

## 5. Таблица `orders` (Заказы)

| Столбец | Тип данных | Описание | Ограничения |
|---|---|---|---|
| order_id | INTEGER | ID заказа | PRIMARY KEY, NOT NULL |
| customer_id | VARCHAR(5) | ID клиента | FOREIGN KEY, NOT NULL |
| employee_id | INTEGER | ID сотрудника | FOREIGN KEY, NULL |
| order_date | DATE | Дата заказа | NOT NULL |
| shipped_date | DATE | Дата отгрузки | NULL |
| ship_country | VARCHAR | Страна доставки | NULL |

## 6. Таблица `order_details` (Детали заказов)

| Столбец | Тип данных | Описание | Ограничения |
|---|---|---|---|
| order_id | INTEGER | ID заказа | PRIMARY KEY (составной), FOREIGN KEY |
| product_id | INTEGER | ID продукта | PRIMARY KEY (составной), FOREIGN KEY |
| unit_price | NUMERIC(10,2) | Цена | CHECK (unit_price >= 0) |
| quantity | SMALLINT | Количество | CHECK (quantity > 0) |

## Расшифровка перечислений (Enum)
- **`discontinued`** в таблице `products`: `0` — продукт доступен, `1` — продукт снят с продажи.
