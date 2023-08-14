"""create comment table

Revision ID: 40799e063491
Revises: 4052e11c6e36
Create Date: 2023-08-12 12:17:04.892732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40799e063491'
down_revision = '4052e11c6e36'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('comment',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('content', sa.String(length=255), nullable=False),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('lesson_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )

def downgrade() -> None:
    op.drop_table('comment')
