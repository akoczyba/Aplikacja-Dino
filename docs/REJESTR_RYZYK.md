# Rejestr Ryzyk Projektu
Opiekun rejestru: Adam Koczyba (Product Owner / Project Manager)
Ostatnia aktualizacja: Sprint 0

| ID | Ryzyko / Zagrożenie | Prawdopodobieństwo (1-5) | Wpływ (1-5) | Waga (P × W) | Plan mitygacji i reakcji | Status |
|:--:|---|:---:|:---:|:---:|---|:---:|
| **R-01** | Opóźnienie integracji Frontend-Backend z powodu rozbieżności modeli danych | 4 | 4 | 16 | Ustalenie ścisłego kontraktu API (OpenAPI/Swagger) i mocków JSON na starcie każdego sprintu | Otwarte |
| **R-02** | Rozrost zakresu (Scope Creep) | 3 | 5 | 15 | Ścisłe egzekwowanie sekcji Out of Scope; odrzucanie żądań spoza MVP przez PO | Otwarte |
| **R-03** | Brak spójnych danych testowych (ceny, zdjęcia produktów, gazetki Dino) | 4 | 3 | 12 | PO dostarcza kompletny pakiet seed data (pliki JSON z promocjami i gazetkami) przed implementacją modułów | Otwarte |
| **R-04** | Trudności z uruchomieniem aplikacji na urządzeniach członków zespołu | 3 | 4 | 12 | DevOps konfiguruje środowisko z opcją podglądu webowego oraz precyzyjną instrukcją instalacji | Otwarte |
| **R-05** | Spadek zaangażowania i dostępności zespołu w okresie kolokwiów i egzaminów | 4 | 3 | 12 | Planowanie mniejszej liczby Story Points (Velocity) w tygodniach zaliczeniowych; wcześniejsze dowożenie zadań krytycznych (Must) | Otwarte |
