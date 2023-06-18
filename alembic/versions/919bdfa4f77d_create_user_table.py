"""create user table

Revision ID: 919bdfa4f77d
Revises: 
Create Date: 2023-05-17 12:29:07.653042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '919bdfa4f77d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('username', sa.String(length=255), nullable=False),
                    sa.Column('avatar', sa.String(length=255), nullable=True),
                    sa.Column('phone', sa.String(length=255), nullable=True),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    )

def downgrade() -> None:
    op.drop_table('user')
