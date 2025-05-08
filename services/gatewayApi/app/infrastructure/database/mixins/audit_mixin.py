from sqlalchemy import Column, DateTime
from datetime import datetime

class AuditMixin:
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)