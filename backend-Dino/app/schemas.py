from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Generic, TypeVar
from uuid import UUID
from datetime import datetime

# Typ generyczny pozwalający opakować dowolne dane w standardową odpowiedź API
T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    Ujednolicona koperta odpowiedzi JSON dla frontendu mobilnego.
    Każdy endpoint zwraca tę samą strukturę: success, message oraz data.
    """

    success: bool = True
    message: str
    data: Optional[T] = None


# --- SCHEMATY WEJŚCIOWE (Walidacja danych przychodzących z aplikacji mobilnej) ---


class UserCreate(BaseModel):
    """Dane wymagane podczas rejestracji nowego konta."""

    email: EmailStr  # Automatyczna walidacja formatu e-mail
    password: str = Field(
        ..., min_length=8, max_length=128
    )  # Wymagane minimum 8 znaków
    phone_number: Optional[str] = Field(None, pattern=r"^\+?[0-9]{9,15}$")
    first_name: Optional[str] = Field(None, max_length=100)
    terms_accepted: bool
    privacy_policy_accepted: bool
    marketing_push: bool = False
    marketing_sms: bool = False


class UserLogin(BaseModel):
    """Dane przesyłane w formacie JSON podczas logowania."""

    email: EmailStr
    password: str


class ConsentsUpdate(BaseModel):
    """Dane do aktualizacji opcjonalnych zgód marketingowych w ustawieniach."""

    marketing_push: Optional[bool] = None
    marketing_sms: Optional[bool] = None


# --- SCHEMATY WYJŚCIOWE (Formatowanie danych wysyłanych do frontendu) ---


class LoyaltyCardOut(BaseModel):
    card_number: str
    points_balance: int
    barcode_format: str = (
        "EAN13"  # Wskazówka dla biblioteki rysującej kod kreskowy na ekranie telefonu
    )
    model_config = ConfigDict(
        from_attributes=True
    )  # Pozwala konwertować obiekt SQLAlchemy bezpośrednio na JSON


class ConsentsOut(BaseModel):
    terms_accepted: bool
    privacy_policy_accepted: bool
    marketing_push: bool
    marketing_sms: bool
    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    """Pełny profil użytkownika wysyłany do aplikacji (celowo pomijamy password_hash!)."""

    id: UUID
    email: EmailStr
    first_name: Optional[str]
    phone_number: Optional[str]
    created_at: datetime
    loyalty_card: Optional[LoyaltyCardOut]
    consents: Optional[ConsentsOut]
    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Czas ważności w sekundach (ułatwia frontendowi planowanie odświeżenia sesji)


class AuthResponse(BaseModel):
    """Pakiet startowy zwracany po poprawnym zalogowaniu lub rejestracji."""

    token: TokenData
    user: UserOut
