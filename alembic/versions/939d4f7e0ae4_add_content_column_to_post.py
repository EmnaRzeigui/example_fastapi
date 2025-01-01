"""add content column to post

Revision ID: 939d4f7e0ae4
Revises: dca232848e1d
Create Date: 2024-12-31 13:50:32.466814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '939d4f7e0ae4'
down_revision: Union[str, None] = 'dca232848e1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
