from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '3d866bd21ffe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'short_urls',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('original_url', sa.String(), nullable=False),
        sa.Column('short_code', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_short_urls_id'), 'short_urls', ['id'], unique=False)
    op.create_index(op.f('ix_short_urls_original_url'), 'short_urls', ['original_url'], unique=False)
    op.create_index(op.f('ix_short_urls_short_code'), 'short_urls', ['short_code'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_short_urls_short_code'), table_name='short_urls')
    op.drop_index(op.f('ix_short_urls_original_url'), table_name='short_urls')
    op.drop_index(op.f('ix_short_urls_id'), table_name='short_urls')
    op.drop_table('short_urls')
