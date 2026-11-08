# Rejestr Ryzyk Projektu (Dino App)
Opiekun rejestru: Adam Koczyba (Product Owner / Project Manager)
Ostatnia aktualizacja: Sprint 0

| ID | Ryzyko / Zagroenie | Prawdopodobiestwo (1-5) | Wpyw (1-5) | Waga (P × W) | Plan mitygacji i reakcji | Status |
|:--:|---|:---:|:---:|:---:|---|:---:|
| **R-01** | Opónienie integracji Frontend-Backend z powodu rozbienoci modeli danych | 4 | 4 | 16 | Ustalenie cisego kontraktu API (OpenAPI/Swagger) i mocków JSON na starcie kadego sprintu | Otwarte |
| **R-02** | Rozrost zakresu (Scope Creep) – pokusa dodawania patnoci lub e-commerce | 3 | 5 | 15 | cise egzekwowanie sekcji Out of Scope; odrzucanie da spoza MVP przez PO | Otwarte |
| **R-03** | Brak spójnych danych testowych (ceny, zdjcia produktów, gazetki Dino) | 4 | 3 | 12 | PO dostarcza kompletny pakiet seed data (pliki JSON z promocjami i gazetkami) przed implementacj moduów | Otwarte |
| **R-04** | Trudnoci z uruchomieniem aplikacji na urzdzeniach czonków zespou (iOS/Android) | 3 | 4 | 12 | DevOps (Piotr) konfiguruje rodowisko z opcj podgldu webowego oraz precyzyjn instrukcj instalacji | Otwarte |
| **R-05** | Spadek zaangaowania i dostpnoci zespou w okresie kolokwiów i egzaminów | 4 | 3 | 12 | Planowanie mniejszej liczby Story Points (Velocity) w tygodniach zaliczeniowych; wczeniejsze dowoenie zada krytycznych (Must) | Otwarte |
