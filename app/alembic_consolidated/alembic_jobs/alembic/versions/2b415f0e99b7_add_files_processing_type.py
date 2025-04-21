"""add files processing type

Revision ID: 2b415f0e99b7
Revises: 5e0ba7db5fcb
Create Date: 2022-10-25 11:50:34.945287

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '2b415f0e99b7'
down_revision = '5e0ba7db5fcb'
branch_labels = None
depends_on = None

job_types_table = sa.sql.table('job_types',
                               sa.sql.column('id', sa.BigInteger),
                               sa.sql.column('name', sa.String()),
                               sa.sql.column('dag_name', sa.String()),
                               sa.sql.column('params_schema',
                                             postgresql.JSONB),
                               sa.sql.column('default_params',
                                             postgresql.JSONB),
                               sa.Column('created_at', sa.DateTime(
                                   timezone=True), nullable=False, default=datetime.now),
                               sa.Column('updated_at', sa.DateTime(
                                   timezone=True), nullable=False, default=datetime.now, onupdate=datetime.now)
                               )


def upgrade():
    op.bulk_insert(
        job_types_table,
        [
            {'id': 2, 'name': 'FILES_PROCESSING',
             'dag_name': 'file_process_v1.0', 'params_schema': {}, 'default_params': {}}
        ]
    )
    op.execute("update job_types SET dag_name='file_process_v1.0' where name='FILES_PROCESSING'")


def downgrade():
    op.execute(job_types_table.delete().where(job_types_table.c.id == 2))
