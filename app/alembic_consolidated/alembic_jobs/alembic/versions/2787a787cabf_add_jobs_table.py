"""Add jobs table

Revision ID: 2787a787cabf
Revises: b9dae3873cb7
Create Date: 2022-03-16 22:15:19.320245

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '2787a787cabf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(sa.text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
    op.create_table(
        'jobs',
        sa.Column('id', sa.BigInteger, nullable=False, primary_key=True),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, default='DECLARED'),
        sa.Column('params', postgresql.JSONB),
        sa.Column('error', postgresql.JSONB),
        sa.Column('output', postgresql.JSONB),
        sa.Column('status_message', sa.String()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, default=datetime.now, onupdate=datetime.now)
    )
    op.create_index('index_jobs_uuid', 'jobs', ['uuid'])
    op.create_index('index_jobs_type', 'jobs', ['type'])


def downgrade():
    pass
