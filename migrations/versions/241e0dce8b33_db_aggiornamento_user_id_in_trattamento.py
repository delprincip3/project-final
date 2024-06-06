"""DB aggiornamento user id in trattamento 

Revision ID: 241e0dce8b33
Revises: 4118bc532b76
Create Date: 2024-06-06 15:18:36.983378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '241e0dce8b33'
down_revision = '4118bc532b76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trattamenti', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trattamenti', schema=None) as batch_op:
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
