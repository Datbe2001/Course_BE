"""create lesson table

Revision ID: 4052e11c6e36
Revises: 578dad2a6cdb
Create Date: 2023-06-30 21:53:39.706355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4052e11c6e36'
down_revision = '578dad2a6cdb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('lesson',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('video_id', sa.String(length=255), nullable=True),
                    sa.Column('course_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )

def downgrade() -> None:
    op.drop_table('lesson')
