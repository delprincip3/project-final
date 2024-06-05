"""DB Init

Revision ID: 3f1e4a593633
Revises: 
Create Date: 2024-06-05 10:24:14.728511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f1e4a593633'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('piante',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('specie', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('utenza',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tipo', sa.String(length=50), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('cognome', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('trattamenti',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pianta_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('descrizione', sa.Text(), nullable=False),
    sa.Column('data_inizio', sa.Date(), nullable=False),
    sa.Column('data_fine', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['pianta_id'], ['piante.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['utenza.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_plant_treatment',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('plant_id', sa.Integer(), nullable=False),
    sa.Column('treatment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['plant_id'], ['piante.id'], ),
    sa.ForeignKeyConstraint(['treatment_id'], ['trattamenti.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['utenza.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'plant_id', 'treatment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_plant_treatment')
    op.drop_table('trattamenti')
    op.drop_table('utenza')
    op.drop_table('piante')
    # ### end Alembic commands ###