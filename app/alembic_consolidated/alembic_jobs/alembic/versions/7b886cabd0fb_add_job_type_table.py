"""add job type table

Revision ID: 7b886cabd0fb
Revises: 2787a787cabf
Create Date: 2022-04-11 16:20:58.558495

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '7b886cabd0fb'
down_revision = '2787a787cabf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'job_types',
        sa.Column('id', sa.BigInteger, nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('dag_name', sa.String(), nullable = False),
        sa.Column('params_schema', postgresql.JSONB, nullable=False, default={}),
        sa.Column('default_params', postgresql.JSONB, nullable=False, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, default=datetime.now),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, default=datetime.now, onupdate=datetime.now)
    )


def downgrade():
    op.drop_table('job_types')