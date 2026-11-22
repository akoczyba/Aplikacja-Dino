import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Pobieramy adres bazy ze zmiennej środowiskowej (zdefiniowanej w docker-compose.yml).
# Jeśli zmienna nie istnieje (np. przy uruchamianiu lokalnym bez Dockera), używamy wartości domyślnej.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://dino_user:dino_pass@localhost:5432/dino_db"
)

# Silnik SQLAlchemy zarządzający pulą połączeń do bazy PostgreSQL
engine = create_engine(DATABASE_URL)

# Fabryka sesji - każde żądanie HTTP otrzyma własną, niezależną sesję bazodanową
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Klasa bazowa, po której będą dziedziczyć wszystkie nasze modele tabel
Base = declarative_base()


def get_db():
    """
    Generator (Dependency w FastAPI) dostarczający sesję bazy danych do endpointów.
    Blok 'finally' gwarantuje, że połączenie zostanie bezpiecznie zamknięte po obsłużeniu żądania,
    nawet jeśli w trakcie wystąpi błąd.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
