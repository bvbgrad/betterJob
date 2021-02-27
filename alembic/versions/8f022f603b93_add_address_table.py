"""Add Address table

Revision ID: 8f022f603b93
Revises: 09eff4796095
Create Date: 2021-02-27 05:58:26.790759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f022f603b93'
down_revision = '09eff4796095'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'address',
        sa.Column('address_Id', sa.INTEGER(), nullable=False),
        sa.Column('street', sa.VARCHAR(length=50), nullable=True),
        sa.Column('city', sa.VARCHAR(length=30), nullable=True),
        sa.Column('state', sa.VARCHAR(length=2), nullable=True),
        sa.Column('zip_code', sa.VARCHAR(length=5), nullable=True),
        sa.Column('company_IdFK', sa.Integer, nullable=True),
        sa.PrimaryKeyConstraint('address_Id')
    )


def downgrade():
    op.drop_table('address')
