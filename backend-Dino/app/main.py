from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from uuid import UUID

from . import models, schemas, security
from .database import engine, get_db

# Automatyczne utworzenie tabel w bazie, jeśli jeszcze nie istnieją
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dino Mobile API",
    description="Backend obsługujący autoryzację użytkowników i karty lojalnościowe aplikacji Dino.",
    version="1.0.0",
)

# Konfiguracja CORS - pozwala aplikacji mobilnej/webowej łączyć się z API z innych domen/portów
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji warto ograniczyć do konkretnych domen aplikacji
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemat autoryzacji oczekujący nagłówka HTTP: "Authorization: Bearer <twój_token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --- GLOBALNA OBSŁUGA BŁĘDÓW (Spójny format JSON dla frontendu) ---


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """Przechwytuje standardowe błędy HTTP (400, 401, 404, 409) i formatuje je pod frontend."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": f"HTTP_{exc.status_code}",
            "message": exc.detail,
            "data": None,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Przechwytuje błędy walidacji Pydantic (422) i mapuje je na konkretne pola formularza."""
    field_errors = {}
    for err in exc.errors():
        field_name = str(
            err["loc"][-1]
        )  # Nazwa błędnego pola (np. 'email' lub 'password')
        field_errors[field_name] = err["msg"]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error_code": "VALIDATION_ERROR",
            "message": "Sprawdź poprawność wprowadzonych danych.",
            "field_errors": field_errors,
            "data": None,
        },
    )


# --- MECHANIZM AUTORYZACJI ŻĄDAŃ ---


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    """
    Funkcja pomocnicza (Dependency) wstrzykiwana do chronionych endpointów.
    Weryfikuje podpis tokena JWT i zwraca obiekt zalogowanego użytkownika z bazy.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sesja wygasła lub token jest nieprawidłowy.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Dekodowanie tokena z jawnym wymuszeniem algorytmu HS256
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    # Pobranie użytkownika z bazy na podstawie ID zaszytego w tokenie
    user = db.query(models.User).filter(models.User.id == UUID(user_id)).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user


# --- ENDPOINTY API ---


@app.post(
    "/auth/register",
    response_model=schemas.ApiResponse[schemas.AuthResponse],
    status_code=status.HTTP_201_CREATED,
)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """Rejestruje nowego użytkownika, zapisuje zgody RODO, tworzy kartę Dino i od razu loguje."""
    # 1. Sprawdzenie obowiązkowych zgód prawnych
    if not (user_in.terms_accepted and user_in.privacy_policy_accepted):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Akceptacja regulaminu i polityki prywatności jest wymagana.",
        )

    # 2. Sprawdzenie unikalności adresu e-mail
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Konto z tym adresem e-mail już istnieje.",
        )

    # 3. Sprawdzenie unikalności numeru telefonu (jeśli został podany)
    if (
        user_in.phone_number
        and db.query(models.User)
        .filter(models.User.phone_number == user_in.phone_number)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ten numer telefonu jest już przypisany do innego konta.",
        )

    # 4. Utworzenie rekordu użytkownika z zahashowanym hasłem
    new_user = models.User(
        email=user_in.email,
        phone_number=user_in.phone_number,
        first_name=user_in.first_name,
        password_hash=security.hash_password(user_in.password),
    )
    db.add(new_user)
    db.flush()  # Wysyła INSERT do bazy bez zamykania transakcji, aby uzyskać wygenerowane new_user.id

    # 5. Zapisanie zgód RODO powiązanych z nowym użytkownikiem
    consents = models.UserConsent(
        user_id=new_user.id,
        terms_accepted=user_in.terms_accepted,
        privacy_policy_accepted=user_in.privacy_policy_accepted,
        marketing_push=user_in.marketing_push,
        marketing_sms=user_in.marketing_sms,
    )
    db.add(consents)

    # 6. Wygenerowanie unikalnej wirtualnej karty Dino dla użytkownika
    loyalty_card = models.LoyaltyCard(
        user_id=new_user.id, card_number=security.generate_dino_card_number()
    )
    db.add(loyalty_card)

    # Zatwierdzenie całej transakcji (wszystkie 3 tabele zapisują się atomowo)
    db.commit()
    db.refresh(new_user)

    # 7. Wygenerowanie tokena JWT, aby frontend od razu przekierował użytkownika do ekranu głównego
    access_token = security.create_access_token(user_id=str(new_user.id))
    token_data = schemas.TokenData(
        access_token=access_token, expires_in=security.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return schemas.ApiResponse(
        message="Konto zostało utworzone pomyślnie.",
        data=schemas.AuthResponse(token=token_data, user=new_user),
    )


@app.post("/auth/login", response_model=schemas.ApiResponse[schemas.AuthResponse])
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Weryfikuje e-mail oraz hasło i zwraca token dostępowy wraz z danymi karty."""
    user = db.query(models.User).filter(models.User.email == credentials.email).first()

    # Celowo zwracamy ten sam komunikat błędu dla złego e-maila i złego hasła (ochrona przed enumeracją kont)
    if not user or not security.verify_password(
        credentials.password, user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowy adres e-mail lub hasło.",
        )

    access_token = security.create_access_token(user_id=str(user.id))
    token_data = schemas.TokenData(
        access_token=access_token, expires_in=security.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return schemas.ApiResponse(
        message="Zalogowano pomyślnie.",
        data=schemas.AuthResponse(token=token_data, user=user),
    )


@app.get("/users/me", response_model=schemas.ApiResponse[schemas.UserOut])
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Zwraca aktualne dane zalogowanego użytkownika (w tym numer karty i saldo punktów).
    Wywoływane przez aplikację mobilną podczas uruchamiania.
    """
    return schemas.ApiResponse(message="Pobrano dane profilu.", data=current_user)


@app.patch(
    "/users/me/consents", response_model=schemas.ApiResponse[schemas.ConsentsOut]
)
def update_consents(
    consents_in: schemas.ConsentsUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Aktualizuje ustawienia powiadomień push i SMS w profilu użytkownika."""
    if consents_in.marketing_push is not None:
        current_user.consents.marketing_push = consents_in.marketing_push
    if consents_in.marketing_sms is not None:
        current_user.consents.marketing_sms = consents_in.marketing_sms

    db.commit()
    db.refresh(current_user.consents)

    return schemas.ApiResponse(
        message="Zaktualizowano zgody marketingowe.", data=current_user.consents
    )
