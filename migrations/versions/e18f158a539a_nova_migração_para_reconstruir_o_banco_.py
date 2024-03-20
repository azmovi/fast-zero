"""Nova migração para reconstruir o banco de dados

Revision ID: e18f158a539a
Revises: 215c890fddf4
Create Date: 2024-03-19 18:28:38.179717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e18f158a539a'
down_revision: Union[str, None] = '215c890fddf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
