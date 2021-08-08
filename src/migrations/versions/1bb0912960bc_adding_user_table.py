"""adding user table

Revision ID: 1bb0912960bc
Revises: 
Create Date: 2021-08-08 15:15:46.651510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bb0912960bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'editors',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('emailId', sa.String(length=100), unique=True, nullable=False),
        sa.Column('fullName', sa.String(100), nullable=False),
        sa.Column('passwordHash', sa.String(length=512), nullable=False),
        sa.Column('phoneNumber', sa.Integer(), unique=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at',sa.DateTime)
    )


def downgrade():
    op.drop_table("editors")
