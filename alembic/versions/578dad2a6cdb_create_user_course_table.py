"""create user course table

Revision ID: 578dad2a6cdb
Revises: aca90b96dc3a
Create Date: 2023-06-30 21:48:35.205073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '578dad2a6cdb'
down_revision = 'aca90b96dc3a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user_course',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('course_id', sa.String(length=255), nullable=False),
                    sa.Column('course_role', sa.Enum('OWNER', 'MEMBER', name='course_role_enum'), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )

def downgrade() -> None:
    op.drop_table('user_course')
