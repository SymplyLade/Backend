"""alter user table

Revision ID: 76d7b3c0995a
Revises: 
Create Date: 2025-10-23 11:19:37.647454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76d7b3c0995a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema. """
    op.execute("""
    ALTER TABLE users
    ADD COLUMN gender varchar(100) DEFAULT 'male'
    """)
    pass


def downgrade() -> None:
    """Downgrade schema. """
    op.execute("""
    ALTER TABLE users
    DROP COLUMN gender
    """)
    pass

