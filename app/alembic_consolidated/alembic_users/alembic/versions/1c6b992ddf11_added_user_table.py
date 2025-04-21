"""Added Users table

Revision ID: 1c6b992ddf11
Revises: 
Create Date: 2022-08-04 21:20:11.983038

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '1c6b992ddf11'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(sa.text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
    op.create_table(
        'user',
        sa.Column('id', sa.BigInteger, nullable=False, primary_key=True, autoincrement=True),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), unique=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('name', sa.String),
        sa.Column('airtableID', sa.String),
        sa.Column('isAdmin', sa.Boolean, default=False),
        sa.Column('active', sa.Boolean, default=True),
        sa.Column('user_data', postgresql.JSONB, nullable=False),
        sa.Column('createdAt', sa.DateTime(timezone=True), nullable=False, default=datetime.now()),
        sa.Column('modifiedAt', sa.DateTime(timezone=True), nullable=False, default=datetime.now())
    )
    op.create_index('index_user_uuid', 'user', ['uuid'])
    op.create_index('index_user_email', 'user', ['email'])
    op.create_index('index_user_airtable_id', 'user', ['airtableID'])
    op.create_index('index_user_query_created_date', 'user', ['createdAt'])
    op.create_index('index_user_query_modified_date', 'user', ['modifiedAt'])


def downgrade():
    op.drop_table('user')
