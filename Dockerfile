# --- ETAP 1: Budowanie zależności ---
FROM python:3.12-slim AS builder

# Zapobiega tworzeniu plików .pyc i buforowaniu logów w konsoli Dockera
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Instalacja kompilatorów potrzebnych m.in. dla biblioteki argon2-cffi
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Tworzymy wirtualne środowisko, które łatwo przeniesiemy do docelowego obrazu
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# --- ETAP 2: Docelowy lekki obraz produkcyjny ---
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Instalacja wyłącznie biblioteki uruchomieniowej PostgreSQL (libpq5) oraz curl (do healthchecka)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Tworzymy dedykowanego użytkownika bez uprawnień roota (wymóg bezpieczeństwa DevOps)
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Kopiujemy gotowe biblioteki z etapu 1 oraz kod aplikacji
COPY --from=builder /opt/venv /opt/venv
COPY ./app /app/app

# Nadajemy prawa własności użytkownikowi appuser
RUN chown -R appuser:appgroup /app
USER appuser

# Dokumentujemy port, na którym nasłuchuje FastAPI
EXPOSE 8000

# Weryfikacja czy proces API odpowiada (wykorzystywane przez Docker / Kubernetes / Load Balancer)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Uruchomienie serwera Uvicorn z wieloma workerami (w produkcji bez flagi --reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]