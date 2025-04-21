"""adding column keep old_user_uuids and old airtable_id 

Revision ID: 1100a3c8c5e9
Revises: 1c6b992ddf11
Create Date: 2023-01-10 10:33:58.773755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1100a3c8c5e9'
down_revision = '1c6b992ddf11'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('old_user_uuid',  sa.ARRAY(sa.String), default={}))
    op.add_column('user', sa.Column('old_user_airtable_id',  sa.ARRAY(sa.String), default={}))

def downgrade():
    pass
