import os
import sys
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, sql
from sqlalchemy.dialects.postgresql import JSONB, UUID
from ..database.conf import Base
from datetime import datetime

sys.path.append(os.getcwd())


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), nullable=False, server_default=sa.text("uuid_generate_v4()"))
    type = Column(String, nullable=False)
    status = Column(String, nullable=False, default='DECLARED')
    params = Column(JSONB)
    error = Column(JSONB)
    output = Column(JSONB)
    status_message = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now
    )

class Job_Type(Base):
    __tablename__ = 'job_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dag_name = Column(String, nullable=False)
    params_schema = Column(JSONB)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now
    )
    default_params = Column(JSONB)
