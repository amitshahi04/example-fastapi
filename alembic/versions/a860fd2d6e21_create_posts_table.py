"""Create Posts Table

Revision ID: a860fd2d6e21
Revises: 
Create Date: 2023-12-23 14:37:44.596071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a860fd2d6e21'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer(), primary_key=True, nullable=False), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
