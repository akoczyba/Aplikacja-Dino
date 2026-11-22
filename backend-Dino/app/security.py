import os
import random
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash

# Klucz tajny używany do podpisywania tokenów JWT.
# W środowisku produkcyjnym MUSI być wczytany z bezpiecznej zmiennej środowiskowej.
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ZMIEN TO W ENV")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Czas życia tokena (60 minut)

# Konfiguracja rekomendowanego algorytmu Argon2 do bezpiecznego hashowania haseł
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Zamienia czyste hasło użytkownika na bezpieczny skrót (hash) z losową solą."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Sprawdza, czy wpisane przy logowaniu hasło pasuje do hasha zapisanego w bazie."""
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user_id: str) -> str:
    """
    Tworzy podpisany kryptograficznie token JWT zawierający ID użytkownika ('sub')
    oraz datę wygaśnięcia ('exp').
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),  # Subject - identyfikator właściciela tokena
        "exp": expire,  # Expiration Time - czas wygaśnięcia
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def generate_dino_card_number() -> str:
    """
    Generuje 13-cyfrowy numer wirtualnej karty lojalnościowej.
    Prefiks '290' oznacza wewnętrzną numerację sklepową, reszta to losowe cyfry.
    """
    random_digits = "".join([str(random.randint(0, 9)) for _ in range(10)])
    return f"290{random_digits}"
