"""Добавление тестовых данных"""
from alembic import op

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade():
    #вставляем категории
    op.execute("""
        INSERT INTO categories (category_id, category_name) VALUES
        (1, 'Beverages'), (2, 'Condiments'), (3, 'Confections')
    """)
    #вставляем клиентов
    op.execute("""
        INSERT INTO customers (customer_id, company_name, contact_name, city, country) VALUES
        ('ALFKI', 'Alfreds Futterkiste', 'Maria Anders', 'Berlin', 'Germany'),
        ('ANATR', 'Ana Trujillo', 'Ana Trujillo', 'Mexico D.F.', 'Mexico')
    """)
    #вставляем продукты
    op.execute("""
        INSERT INTO products (product_id, product_name, category_id, unit_price, units_in_stock) VALUES
        (1, 'Chai', 1, 18.00, 39),
        (2, 'Chang', 1, 19.00, 17)
    """)

def downgrade():
    op.execute("DELETE FROM products WHERE product_id IN (1, 2)")
    op.execute("DELETE FROM customers WHERE customer_id IN ('ALFKI', 'ANATR')")
    op.execute("DELETE FROM categories WHERE category_id IN (1, 2, 3)")
