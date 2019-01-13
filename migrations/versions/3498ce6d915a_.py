"""empty message

Revision ID: 3498ce6d915a
Revises: 584d8f013093
Create Date: 2019-01-07 10:34:20.727122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3498ce6d915a'
down_revision = '584d8f013093'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Organization', sa.Column('orgName', sa.String(length=255), nullable=True))
    op.drop_column('Organization', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Organization', sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('Organization', 'orgName')
    # ### end Alembic commands ###
