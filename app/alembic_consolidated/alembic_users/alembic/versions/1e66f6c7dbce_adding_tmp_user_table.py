"""adding tmp user table

Revision ID: 1e66f6c7dbce
Revises: 1100a3c8c5e9
Create Date: 2024-04-30 16:27:20.432639

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime



# revision identifiers, used by Alembic.
revision = '1e66f6c7dbce'
down_revision = '1100a3c8c5e9'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(sa.text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
    op.create_table(
        'user_tmp',
        sa.Column('id', sa.BigInteger, nullable=False, primary_key=True, autoincrement=True),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), unique=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('name', sa.String),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('user_data', postgresql.JSONB, nullable=False),
        sa.Column('createdAt', sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column('modifiedAt', sa.DateTime(timezone=True), nullable=False, default=datetime.now())
    )
    op.create_index('index_user_tmp_uuid', 'user_tmp', ['uuid'])
    op.create_index('index_user_tmp_email', 'user_tmp', ['email'])
    op.create_index('index_user_tmp_query_created_date', 'user_tmp', ['createdAt'])
    op.create_index('index_user_tmp_query_modified_date', 'user_tmp', ['modifiedAt'])



def downgrade():
    pass
