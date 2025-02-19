"""empty message

Revision ID: cee03c6736e1
Revises: b311a7574a6e
Create Date: 2022-11-07 11:13:01.662991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cee03c6736e1'
down_revision = 'b311a7574a6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bike', sa.Column('cyclist_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'bike', 'cyclist', ['cyclist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bike', type_='foreignkey')
    op.drop_column('bike', 'cyclist_id')
    # ### end Alembic commands ###
