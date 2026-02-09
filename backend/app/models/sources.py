from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    type = Column(String(50), nullable=False)  # database, excel, api
    db_type = Column(String(50), nullable=True)  # mysql, oracle, postgresql
    host = Column(String(255), nullable=True)
    port = Column(Integer, nullable=True)
    database = Column(String(255), nullable=True)
    username = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=True)  # for excel
    api_url = Column(String(500), nullable=True)  # for api
    api_method = Column(String(10), nullable=True)  # get, post
    api_headers = Column(JSON, nullable=True)  # for api
    api_body = Column(JSON, nullable=True)  # for api
    connection_pool = Column(Integer, default=10)
    refresh_interval = Column(Integer, default=300)  # seconds
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
