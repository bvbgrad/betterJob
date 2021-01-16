"""Add Company table

Revision ID: 01cc34599d1e
Revises: 
Create Date: 2021-01-16 17:16:47.710030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01cc34599d1e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Company',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('Id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Company')
    # ### end Alembic commands ###