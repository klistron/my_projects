"""add seats to order

Revision ID: 0859cdee13b5
Revises: a42f23741576
Create Date: 2024-11-04 17:57:21.724405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0859cdee13b5'
down_revision = 'a42f23741576'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seats', sa.JSON(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_column('seats')

    # ### end Alembic commands ###