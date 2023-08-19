"""Restore url_views table

Revision ID: c8bf423b6a5f
Revises: f4b5db915adb
Create Date: 2023-02-07 19:45:04.033468

Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8bf423b6a5f'
down_revision = 'f4b5db915adb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url_views',
    sa.Column('url_id', sa.Integer(), nullable=True),
    sa.Column('paste_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=15), nullable=False),
    sa.Column('user_agent_id', sa.Integer(), nullable=False),
    sa.Column('referer_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['paste_id'], ['paste_urls.id'], ),
    sa.ForeignKeyConstraint(['referer_id'], ['referers.id'], ),
    sa.ForeignKeyConstraint(['url_id'], ['redirect_urls.id'], ),
    sa.ForeignKeyConstraint(['user_agent_id'], ['user_agents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('url_views')
    # ### end Alembic commands ###
