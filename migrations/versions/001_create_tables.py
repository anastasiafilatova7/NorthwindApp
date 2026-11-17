"""Создание базовых таблиц"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    #таблица клиентов
    op.create_table('customers',
        sa.Column('customer_id', sa.String(5), primary_key=True),
        sa.Column('company_name', sa.String(40), nullable=False),
        sa.Column('contact_name', sa.String(30)),
        sa.Column('city', sa.String(15)),
        sa.Column('country', sa.String(15))
    )
    #таблица сотрудников
    op.create_table('employees',
        sa.Column('employee_id', sa.SmallInteger, primary_key=True),
        sa.Column('last_name', sa.String(20), nullable=False),
        sa.Column('first_name', sa.String(10), nullable=False),
        sa.Column('title', sa.String(30))
    )
    #таблица категорий
    op.create_table('categories',
        sa.Column('category_id', sa.SmallInteger, primary_key=True),
        sa.Column('category_name', sa.String(15), nullable=False)
    )
    #таблица продуктов
    op.create_table('products',
        sa.Column('product_id', sa.SmallInteger, primary_key=True),
        sa.Column('product_name', sa.String(40), nullable=False),
        sa.Column('category_id', sa.SmallInteger),
        sa.Column('unit_price', sa.Numeric(10, 2)),
        sa.Column('units_in_stock', sa.SmallInteger)
    )
    #таблица заказов
    op.create_table('orders',
        sa.Column('order_id', sa.SmallInteger, primary_key=True),
        sa.Column('customer_id', sa.String(5)),
        sa.Column('employee_id', sa.SmallInteger),
        sa.Column('order_date', sa.Date)
    )
    #таблица деталей заказов
    op.create_table('order_details',
        sa.Column('order_id', sa.SmallInteger, primary_key=True),
        sa.Column('product_id', sa.SmallInteger, primary_key=True),
        sa.Column('unit_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('quantity', sa.SmallInteger, nullable=False),
        sa.Column('discount', sa.Float, nullable=False)
    )

def downgrade():
    op.drop_table('order_details')
    op.drop_table('orders')
    op.drop_table('products')
    op.drop_table('categories')
    op.drop_table('employees')
    op.drop_table('customers')
