"""adding new fields

Revision ID: 888443fcac6b
Revises: 626591323746
Create Date: 2024-08-10 14:32:33.003815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '888443fcac6b'
down_revision: Union[str, None] = '626591323746'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('fee', sa.Numeric(), nullable=True))
    op.add_column('transactions', sa.Column('nonce', sa.Integer(), nullable=True))
    op.add_column('transactions', sa.Column('time', sa.DateTime(), nullable=True))
    op.add_column('transactions', sa.Column('input_hex', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'input_hex')
    op.drop_column('transactions', 'time')
    op.drop_column('transactions', 'nonce')
    op.drop_column('transactions', 'fee')
    # ### end Alembic commands ###
