"""create course table

Revision ID: aca90b96dc3a
Revises: 919bdfa4f77d
Create Date: 2023-06-30 21:40:08.506374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aca90b96dc3a'
down_revision = '919bdfa4f77d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('course',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('banner', sa.String(length=255), nullable=True),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('course_type', sa.Enum('FREE', 'PRO', name='course_type_enum'), nullable=False),
                    sa.Column('KEY', sa.String(length=255), nullable=True),
                    sa.Column('created_by', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )

def downgrade() -> None:
    op.drop_table('course')
