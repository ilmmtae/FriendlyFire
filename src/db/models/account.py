from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, UUID, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base
from db.types.account import AccountType


class Account(Base):

    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    image = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    type = Column(String, default=AccountType.STUDENT)

    contact_data = relationship(
        "ContactData",
        back_populates="account",
        cascade="all, delete-orphan",
    )

class ContactData(Base):

    __tablename__ = "contact_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"))
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    street = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    account = relationship("Account", back_populates="contact_data")
