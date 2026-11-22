-- Włączenie rozszerzenia do automatycznego generowania bezpiecznych identyfikatorów UUID v4
-- (zapobiega zgadywaniu ID kolejnych użytkowników w URL-ach, np. /users/1, /users/2)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Tabela główna użytkowników
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,             -- Login użytkownika (unikalny w skali systemu)
    phone_number VARCHAR(15) UNIQUE,                -- Opcjonalny numer telefonu (np. do logowania SMS lub odzyskiwania konta)
    password_hash VARCHAR(255) NOT NULL,            -- Zahashowane hasło (nigdy nie przechowujemy czystego tekstu!)
    first_name VARCHAR(100),                        -- Imię wyświetlane na ekranie powitalnym w aplikacji
    is_active BOOLEAN DEFAULT TRUE,                 -- Flaga pozwalająca zablokować konto bez usuwania historii
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabela zgód RODO i marketingowych (relacja 1:1 z tabelą users)
-- ON DELETE CASCADE oznacza, że usunięcie konta użytkownika automatycznie usuwa jego zgody
CREATE TABLE user_consents (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    terms_accepted BOOLEAN NOT NULL DEFAULT FALSE,          -- Wymagana akceptacja regulaminu
    privacy_policy_accepted BOOLEAN NOT NULL DEFAULT FALSE, -- Wymagana akceptacja polityki prywatności
    marketing_push BOOLEAN NOT NULL DEFAULT FALSE,          -- Zgoda na powiadomienia push o promocjach
    marketing_sms BOOLEAN NOT NULL DEFAULT FALSE,           -- Zgoda na SMS-y z gazetką
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabela wirtualnych kart lojalnościowych Dino (relacja 1:1 z tabelą users)
CREATE TABLE loyalty_cards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    card_number VARCHAR(20) UNIQUE NOT NULL,        -- 13-cyfrowy numer karty (EAN-13) generowany jako kod kreskowy na ekranie
    points_balance INTEGER DEFAULT 0,               -- Saldo punktów/naklejek lojalnościowych
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabela e-paragonów i historii zakupów (relacja 1:N - jeden użytkownik ma wiele paragonów)
CREATE TABLE receipts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    store_code VARCHAR(20) NOT NULL,                -- Kod konkretnego marketu Dino (np. "DINO-1042")
    total_amount NUMERIC(10, 2) NOT NULL,           -- Kwota całkowita paragonu (NUMERIC zapobiega błędom zaokrągleń float)
    receipt_date TIMESTAMP WITH TIME ZONE NOT NULL, -- Data i godzina zakupu przy kasie
    items_json JSONB NOT NULL                       -- Elastyczna lista produktów z paragonu zapisana jako binarny JSON
);

-- Indeksy przyspieszające najczęstsze zapytania (logowanie po e-mailu oraz skanowanie karty przy kasie)
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_loyalty_card_number ON loyalty_cards(card_number);
CREATE INDEX idx_receipts_user_id ON receipts(user_id);