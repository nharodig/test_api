"""adding new job types

Revision ID: 5e0ba7db5fcb
Revises: 7b886cabd0fb
Create Date: 2022-04-21 15:42:48.127549

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '5e0ba7db5fcb'
down_revision = '7b886cabd0fb'
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
            {'id': 1, 'name': 'APPLICATION_PROCESSING',
             'dag_name': 'application_process', 'params_schema': {}, 'default_params': {}}
        ]
    )
    op.execute("update job_types SET dag_name='application_process' where name='APPLICATION_PROCESSING'")

def downgrade():
    op.execute(job_types_table.delete().where(job_types_table.c.id == 1))
