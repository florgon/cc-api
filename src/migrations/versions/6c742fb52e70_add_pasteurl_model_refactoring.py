"""Add PasteUrl model, refactoring

Revision ID: 6c742fb52e70
Revises: 5f9cee34c025
Create Date: 2023-02-06 19:39:17.970808

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6c742fb52e70'
down_revision = '5f9cee34c025'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paste_urls',
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=True),
    sa.Column('stats_is_public', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('redirect_urls',
    sa.Column('redirect', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=True),
    sa.Column('stats_is_public', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('urls')
    with op.batch_alter_table('url_views', schema=None) as batch_op:
        batch_op.add_column(sa.Column('paste_id', sa.Integer(), nullable=True))
        batch_op.alter_column('url_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_constraint('url_views_url_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'paste_urls', ['paste_id'], ['id'])
        batch_op.create_foreign_key(None, 'redirect_urls', ['url_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('url_views', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('url_views_url_id_fkey', 'urls', ['url_id'], ['id'])
        batch_op.alter_column('url_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('paste_id')

    op.create_table('urls',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('redirect', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('expiration_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('stats_is_public', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.user_id'], name='urls_owner_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='urls_pkey')
    )
    op.drop_table('redirect_urls')
    op.drop_table('paste_urls')
    # ### end Alembic commands ###
