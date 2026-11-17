"""Добавление внешних ключей, проверок и индексов"""
from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    #внешние ключи
    op.create_foreign_key('fk_orders_customer', 'orders', 'customers', ['customer_id'], ['customer_id'], ondelete='RESTRICT')
    op.create_foreign_key('fk_orders_employee', 'orders', 'employees', ['employee_id'], ['employee_id'], ondelete='SET NULL')
    op.create_foreign_key('fk_order_details_order', 'order_details', 'orders', ['order_id'], ['order_id'], ondelete='CASCADE')
    op.create_foreign_key('fk_order_details_product', 'order_details', 'products', ['product_id'], ['product_id'], ondelete='RESTRICT')
    op.create_foreign_key('fk_products_category', 'products', 'categories', ['category_id'], ['category_id'], ondelete='SET NULL')

    #ограничение CHECK (цена не может быть отрицательной)
    op.create_check_constraint('chk_products_price', 'products', 'unit_price >= 0')
    op.create_check_constraint('chk_order_details_qty', 'order_details', 'quantity > 0')

    #индексы для ускорения запросов
    op.create_index('idx_orders_customer', 'orders', ['customer_id'])
    op.create_index('idx_products_category', 'products', ['category_id'])

def downgrade():
    op.drop_index('idx_products_category', table_name='products')
    op.drop_index('idx_orders_customer', table_name='orders')
    op.drop_constraint('chk_order_details_qty', 'order_details', type_='check')
    op.drop_constraint('chk_products_price', 'products', type_='check')
    op.drop_constraint('fk_products_category', 'products', type_='foreignkey')
    op.drop_constraint('fk_order_details_product', 'order_details', type_='foreignkey')
    op.drop_constraint('fk_order_details_order', 'order_details', type_='foreignkey')
    op.drop_constraint('fk_orders_employee', 'orders', type_='foreignkey')
    op.drop_constraint('fk_orders_customer', 'orders', type_='foreignkey')
