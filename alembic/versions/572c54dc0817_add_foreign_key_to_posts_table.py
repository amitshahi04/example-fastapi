"""add foreign key to posts table

Revision ID: 572c54dc0817
Revises: 59f5164c92b0
Create Date: 2023-12-23 15:12:13.819377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '572c54dc0817'
down_revision: Union[str, None] = '59f5164c92b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'],remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
