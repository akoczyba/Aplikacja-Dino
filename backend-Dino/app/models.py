import uuid
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    """Model ORM odpowiadający tabeli 'users' w PostgreSQL."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacje po stronie Pythona ułatwiające pobieranie powiązanych danych (np. user.loyalty_card)
    # uselist=False oznacza relację 1-do-1 (jeden użytkownik ma jedną kartę i jeden zestaw zgód)
    consents = relationship(
        "UserConsent",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    loyalty_card = relationship(
        "LoyaltyCard",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    receipts = relationship(
        "Receipt", back_populates="user", cascade="all, delete-orphan"
    )


class UserConsent(Base):
    """Model ORM odpowiadający tabeli 'user_consents' (zgody RODO)."""

    __tablename__ = "user_consents"

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    terms_accepted = Column(Boolean, nullable=False, default=False)
    privacy_policy_accepted = Column(Boolean, nullable=False, default=False)
    marketing_push = Column(Boolean, nullable=False, default=False)
    marketing_sms = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="consents")


class LoyaltyCard(Base):
    """Model ORM odpowiadający tabeli 'loyalty_cards' (karta klienta Dino)."""

    __tablename__ = "loyalty_cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    card_number = Column(String(20), unique=True, index=True, nullable=False)
    points_balance = Column(Integer, default=0)

    user = relationship("User", back_populates="loyalty_card")


class Receipt(Base):
    """Model ORM odpowiadający tabeli 'receipts' (e-paragony)."""

    __tablename__ = "receipts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    store_code = Column(String(20), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    receipt_date = Column(DateTime(timezone=True), nullable=False)
    items_json = Column(JSONB, nullable=False)

    user = relationship("User", back_populates="receipts")
