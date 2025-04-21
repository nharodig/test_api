import os
import sys
import cuid
import sqlalchemy as sa
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger
from sqlalchemy.dialects.postgresql import JSONB, UUID
from datetime import datetime
from ..database.conf import Base

sys.path.append(os.getcwd())


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), nullable=False, server_default=sa.text("uuid_generate_v4()"))
    email = Column(String, nullable=False, unique=True)
    name = Column(String)
    airtableID = Column(String)
    isAdmin = Column(Boolean, nullable=False, default=False)
    user_data = Column(JSONB)
    createdAt = Column(
        DateTime(timezone=True),
        default=datetime.now
    )
    modifiedAt = Column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now
    )



class UserTMP(Base):
    __tablename__ = 'user_tmp'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), nullable=False, server_default=sa.text("uuid_generate_v4()"))
    email = Column(String, nullable=False, unique=True)
    name = Column(String)
    user_data = Column(JSONB)
    createdAt = Column(
        DateTime(timezone=True),
        default=datetime.now
    )
    modifiedAt = Column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now
    )


