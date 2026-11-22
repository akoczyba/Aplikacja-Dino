# Raport z Testów – Aplikacja mobilna Dino
**Zakres raportu:** [np. Sprint 1 (10.11.2026 – 23.11.2026) / Faza Stabilizacji / Wydanie v0.1]
**Data sporządzenia:** [DD.MM.RRRR]
**Autor (QA / Tester):** Lucjan Klarecki
**Product Owner / PM:** Adam Koczyba
**Facylitator Sprintu:** [Jakub / Samuel / Piotr / Lucjan – zgodnie z rotacją]

---

## 1. Podsumowanie wykonawcze (Executive Summary)
* **Rekomendacja QA:** `[GO / WARUNKOWE GO / NO-GO]`
* **Cel testów w danym okresie:** [np. Weryfikacja modułu autentykacji (`EPIC-01`) oraz wirtualnej DinoKarty (`EPIC-02`) na środowisku testowym]
* **Ogólna ocena jakości:** [2–3 zdania podsumowujące stabilność przetestowanych funkcji, zgodność z kryteriami sukcesu oraz ewentualne blokery]

---

## 2. Zakres testów i środowiska
* **Przetestowane funkcjonalności (In Scope):**
  * [np. `US-01`: Rejestracja użytkownika]
  * [np. `US-02`: Logowanie użytkownika]
  * [np. `US-03`: Wyświetlenie kodu karty]
* **Wyłączenia z testów (Out of Scope):** Płatności online, zamówienia z dostawą, integracja z fizycznymi kasami POS, weryfikacja SMS
* **Środowiska i konfiguracja testowa:**
  * Backend / API: `[Local Docker / Środowisko CI / Staging]`
  * Aplikacja kliencka: `[Emulator Android / Urządzenie fizyczne / Podgląd webowy]`
  * Wersja kodu (Commit / Tag): `[np. main @ a1b2c3d]`

---

## 3. Metryki wykonania testów i jakości
| Kategoria | Metryka | Wynik | Próg docelowy (DoD) | Status |
| :--- | :--- | :---: | :---: | :---: |
| **Postęp testów** | Wykonane przypadki testowe (Executed) | `[X / Y] ([Z]%)` | `100%` dla MUST HAVE[cite: 9] | `[OK / NOK]` |
| **Skuteczność** | Testy zakończone sukcesem (Passed) | `[A / X] ([B]%)` | `>= 95%` | `[OK / NOK]` |
| **Błędy w testach** | Testy zakończone błędem (Failed) | `[C]` | `0` dla krytycznych ścieżek | `[OK / NOK]` |
| **Jakość kodu (CI)** | Pokrycie testami jednostkowymi (Coverage) | `[D]%` | `>= 70%` | `[OK / NOK]` |
| **Defekty krytyczne** | Otwarte błędy `Blocker` / `Critical` | `[E]` | `0` | `[OK / NOK]` |
| **Defekty pozostałe** | Otwarte błędy `Major` / `Minor` | `[F]` | Wg akceptacji PO | `[INFO]` |

---

## 4. Wyniki szczegółowe wg User Stories / Epików
| Epik / ID | Nazwa User Story | Priorytet MoSCoW | Liczba TC | Passed | Failed | Status QA | Powiązane GitHub Issues |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `EPIC-01` / `US-01` | Rejestracja użytkownika[cite: 9] | MUST HAVE[cite: 9] | `[X]` | `[X]` | `[0]` | `Zaliczony` | Brak |
| `EPIC-01` / `US-02` | Logowanie użytkownika[cite: 9] | MUST HAVE[cite: 9] | `[X]` | `[X]` | `[0]` | `Zaliczony` | `#14` (Minor) |
| `EPIC-02` / `US-03` | Wyświetlenie kodu karty[cite: 9] | MUST HAVE[cite: 9] | `[X]` | `[X]` | `[0]` | `Zaliczony` | Brak |

---

## 5. Rejestr otwartych defektów
*Lista aktywnych zgłoszeń z zakładki GitHub Issues (etykieta `bug`):*

| ID Issue | Tytuł defektu | Priorytet | Przypisany do | Status | Wpływ na wydanie / UWAGI |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `#14` | [np. Brak komunikatu walidacji przy pustym polu e-mail] | `Minor` | Jakub Góra (FE)[cite: 1, 8] | `In Progress` | Nie blokuje prezentacji Demo |

---

## 6. Ocena ryzyk projektowych i rekomendacje QA
*Odniesienie do `REJESTR_RYZYK.md`:*
* **R-01 (Rozbieżność modeli danych FE-BE):** [np. Zweryfikowano kontrakty API dla autentykacji – brak niezgodności]
* **R-03 (Brak spójnych danych testowych):** [np. Oczekujemy na plik JSON z gazetką i promocjami od PO przed startem testów Sprintu 2]
* **R-04 (Uruchamianie aplikacji na różnych urządzeniach):** [np. Potwierdzono poprawne działanie w emulatorze oraz podglądzie webowym]
* **Rekomendacje na kolejny krok:** [np. Uzupełnienie testów użyteczności pod kątem czytelności interfejsu dla osób mniej technicznych]
