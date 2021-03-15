"""Add Job table

Revision ID: 65c678ae00c6
Revises: 8f022f603b93
Create Date: 2021-03-14 17:34:01.734815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65c678ae00c6'
down_revision = '8f022f603b93'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'job',
        sa.Column('job_Id', sa.INTEGER(), primary_key=True),
        sa.Column('job_name', sa.VARCHAR(length=50), nullable=False),
        sa.Column('job_nbr', sa.VARCHAR(length=30), nullable=True),
        sa.Column('priority', sa.VARCHAR(length=10), nullable=True),
        sa.Column('job_type', sa.VARCHAR(length=10), nullable=True),
        sa.Column('job_post_date', sa.DATE(), nullable=True),
        sa.Column('job_expire_date', sa.DATE(), nullable=True),
        sa.Column('salary_min', sa.INTEGER, nullable=True),
        sa.Column('salary_max', sa.INTEGER, nullable=True),
        sa.Column('company_IdFK', sa.Integer, nullable=True)
    )


def downgrade():
    op.drop_table('job')
