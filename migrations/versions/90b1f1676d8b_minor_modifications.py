"""minor modifications

Revision ID: 90b1f1676d8b
Revises: bf494c9a2b1c
Create Date: 2019-02-08 15:52:59.888464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90b1f1676d8b'
down_revision = 'bf494c9a2b1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Person', sa.Column('personFirstName', sa.String(length=255), nullable=True))
    op.add_column('Person', sa.Column('personLastName', sa.String(length=255), nullable=True))
    op.add_column('Person', sa.Column('personSecondName', sa.String(length=255), nullable=True))
    op.drop_column('Person', 'personName')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Person', sa.Column('personName', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('Person', 'personSecondName')
    op.drop_column('Person', 'personLastName')
    op.drop_column('Person', 'personFirstName')
    # ### end Alembic commands ###
