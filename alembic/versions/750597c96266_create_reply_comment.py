"""create reply comment

Revision ID: 750597c96266
Revises: 40799e063491
Create Date: 2023-08-17 11:10:37.293142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '750597c96266'
down_revision = '40799e063491'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('reply_comment',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('content', sa.String(length=255), nullable=False),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('comment_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('reply_comment')
