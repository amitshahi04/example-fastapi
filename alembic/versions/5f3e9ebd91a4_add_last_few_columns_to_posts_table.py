"""add last few columns to posts table

Revision ID: 5f3e9ebd91a4
Revises: 572c54dc0817
Create Date: 2023-12-23 16:22:25.663363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f3e9ebd91a4'
down_revision: Union[str, None] = '572c54dc0817'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), 
                                     nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                     nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
