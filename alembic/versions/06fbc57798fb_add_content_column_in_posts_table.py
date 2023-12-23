"""add content column in posts table

Revision ID: 06fbc57798fb
Revises: a860fd2d6e21
Create Date: 2023-12-23 14:57:48.116104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06fbc57798fb'
down_revision: Union[str, None] = 'a860fd2d6e21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
