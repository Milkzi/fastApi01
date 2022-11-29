"""empty message

Revision ID: 13fb2d897240
Revises: e40b9b27b4dd
Create Date: 2022-09-19 15:06:31.831490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13fb2d897240'
down_revision = 'e40b9b27b4dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('phone_bind_info', sa.Column('screen_address', sa.String(length=500), nullable=True))
    op.add_column('phone_bind_info', sa.Column('min_price', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('phone_bind_info', 'min_price')
    op.drop_column('phone_bind_info', 'screen_address')
    # ### end Alembic commands ###