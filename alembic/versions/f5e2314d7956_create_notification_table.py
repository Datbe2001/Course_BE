"""create notification table

Revision ID: f5e2314d7956
Revises: 750597c96266
Create Date: 2023-08-18 20:57:47.485684

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f5e2314d7956'
down_revision = '750597c96266'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('notification',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('data', sa.JSON(), nullable=False),
                    sa.Column('unread', sa.Boolean(), server_default=sa.text("True")),
                    sa.Column('notification_type',
                              sa.Enum('SYSTEM_NOTIFICATION', 'COURSE_NOTIFICATION', 'POST_NOTIFICATION',
                                      'COMMENT_NOTIFICATION', name='notification_type_enum'), nullable=False),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('notification')
