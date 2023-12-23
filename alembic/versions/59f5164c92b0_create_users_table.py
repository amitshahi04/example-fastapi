"""create users table

Revision ID: 59f5164c92b0
Revises: 06fbc57798fb
Create Date: 2023-12-23 15:01:41.175889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59f5164c92b0'
down_revision: Union[str, None] = '06fbc57798fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String,nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
