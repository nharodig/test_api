import os
import sys
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, sql
from sqlalchemy.dialects.postgresql import JSONB, UUID
from ..database.conf import Base
from datetime import datetime

sys.path.append(os.getcwd())


class Notification(Base):
    __tablename__ = 'typeform_notifications'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), nullable=False, server_default=sa.text("uuid_generate_v4()"))
    event_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    notification_type = Column(String, nullable=False)
    submitted_at = Column(DateTime(timezone=True))
    landed_at = Column(DateTime(timezone=True))
    payload = Column(JSONB)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now
    )


