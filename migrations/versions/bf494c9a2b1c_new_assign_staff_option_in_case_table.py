"""new assign staff option in case table

Revision ID: bf494c9a2b1c
Revises: 69e336c86df9
Create Date: 2019-02-08 09:58:42.124756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf494c9a2b1c'
down_revision = '69e336c86df9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('case_staff',
    sa.Column('case_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['case_id'], ['Case.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['Staff.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('case_staff')
    # ### end Alembic commands ###
