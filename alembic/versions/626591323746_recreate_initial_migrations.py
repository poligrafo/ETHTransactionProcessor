"""Recreate initial migrations

Revision ID: 626591323746
Revises: 
Create Date: 2024-08-09 09:33:23.470537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '626591323746'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hash', sa.String(), nullable=True),
    sa.Column('from_address', sa.String(), nullable=True),
    sa.Column('to_address', sa.String(), nullable=True),
    sa.Column('value', sa.Numeric(), nullable=True),
    sa.Column('gas', sa.Integer(), nullable=True),
    sa.Column('gas_price', sa.Numeric(), nullable=True),
    sa.Column('block_number', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_block_number'), 'transactions', ['block_number'], unique=False)
    op.create_index(op.f('ix_transactions_from_address'), 'transactions', ['from_address'], unique=False)
    op.create_index('ix_transactions_hash', 'transactions', ['hash'], unique=False)
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)
    op.create_index('ix_transactions_to_address', 'transactions', ['to_address'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_transactions_to_address', table_name='transactions')
    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')
    op.drop_index('ix_transactions_hash', table_name='transactions')
    op.drop_index(op.f('ix_transactions_from_address'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_block_number'), table_name='transactions')
    op.drop_table('transactions')
    # ### end Alembic commands ###
