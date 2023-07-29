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
                    sa.Column('full_name', sa.String(length=255), nullable=True),
                    sa.Column('avatar', sa.String(length=255), nullable=True),
                    sa.Column('phone', sa.String(length=255), nullable=True),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('birthday', sa.Date(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), server_default=sa.text('false'), nullable=False),
                    sa.Column('hashed_password', sa.String(), nullable=True),
                    sa.Column('verify_code', sa.String(), nullable=True),
                    sa.Column('qr_code', sa.String(length=255), nullable=True),
                    sa.Column('system_role', sa.Enum('ADMIN', 'MANAGER', 'MEMBER', name='system_role_enum'),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )

def downgrade() -> None:
    op.drop_table('user')
