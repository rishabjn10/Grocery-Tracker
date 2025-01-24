"""Allow for nullable fields

Revision ID: 2a76c2744c25
Revises: 15260d56ee49
Create Date: 2025-01-25 04:19:38.781944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a76c2744c25'
down_revision: Union[str, None] = '15260d56ee49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('order_source', sa.String(), nullable=True))
    op.alter_column('orders', 'order_date',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('orders', 'payment_method',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('orders', 'processed')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('processed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.alter_column('orders', 'payment_method',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('orders', 'order_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.drop_column('orders', 'order_source')
    # ### end Alembic commands ###
