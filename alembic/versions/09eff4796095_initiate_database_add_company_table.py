"""Initiate database - Add Company table

Revision ID: 09eff4796095
Revises:
Create Date: 2021-02-27 05:50:11.072729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09eff4796095'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'company',
        sa.Column('company_Id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=30), nullable=True),
        sa.PrimaryKeyConstraint('company_Id')
    )


def downgrade():
    op.drop_table('company')
