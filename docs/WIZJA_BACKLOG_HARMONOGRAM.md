# Wizja Produktu, Product Backlog i Harmonogram (Dino App)
Autor: Adam Koczyba (Product Owner / Project Manager)
Status: Sprint 0

---

## 1. Wizja Produktu (Product Vision) i MVP
Aplikacja mobilna Dino to proste, intuicyjne narzędzie wspierające stacjonarne zakupy w sieci marketów Dino. Łączy funkcje programu lojalnościowego (wirtualna DinoKarta) oraz katalogu okazji (gazetka cyfrowa, lista przecenionych produktów) z interaktywną listą zakupów.

- **Dla kogo:** Dla klientów ceniących oszczędność i szybkie zakupy (m.in. studenci, osoby starsze, zapracowani mieszkańcy mniejszych miejscowości).
- **Zakres MVP (Minimalna Wersja Produktu):**
  1. Rejestracja i logowanie użytkownika.
  2. Wirtualna karta z kodem kreskowym/QR i saldem punktów.
  3. Przeglądanie aktualnej gazetki i promocji.
  4. Interaktywna lista zakupów z możliwością dodawania artykułów z promocji.
- **Poza zakresem (Out of Scope):** Płatności online, zamówienia z dostawą (e-grocery), integracja z fizycznymi kasami POS, weryfikacja SMS.

---

## 2. Product Backlog: Epiki i Priorytetyzacja (MoSCoW)

W ramach produktu zdefiniowano 6 Epików, do których przypisano szczegółowe User Stories:

### [EPIC-01] Moduł autentykacji i konta użytkownika
- **Priorytet:** MUST HAVE
- **Powiązane User Stories:** US-01 (Rejestracja), US-02 (Logowanie).

### [EPIC-02] DinoKarta i program lojalnościowy
- **Priorytet:** MUST HAVE
- **Powiązane User Stories:** US-03 (Wyświetlenie kodu karty), US-04 (Naliczanie punktów - tryb demo).

### [EPIC-03] Cyfrowa gazetka promocyjna
- **Priorytet:** SHOULD HAVE
- **Powiązane User Stories:** US-05 (Przeglądanie stron gazetki).

### [EPIC-04] Katalog produktów i promocji
- **Priorytet:** MUST HAVE
- **Powiązane User Stories:** US-06 (Siatka przecenionych artykułów).

### [EPIC-05] Mobilna lista zakupów
- **Priorytet:** MUST HAVE
- **Powiązane User Stories:** US-07 (Ręczne dodawanie), US-08 (Dodawanie z promocji), US-09 (Odznaczanie kupionych).

### [EPIC-06] Wyszukiwarka i lokalizacja marketów
- **Priorytet:** SHOULD HAVE
- **Powiązane User Stories:** US-10 (Lista i godziny otwarcia sklepów).

---

## 3. Kalendarz Sprintów (Harmonogram semestralny - Zima 2026/2027)

- **Sprint 0 (Zakończenie do 15.11):** Koncepcja produktu, Backlog, architektura, rejestr ryzyk, DoR/DoD.
- **Sprint 1 (16.11 – 29.11):** 
  - Cel: Baza danych, szkielet aplikacji, autentykacja (EPIC-01) oraz wirtualna DinoKarta (EPIC-02).
  - Zadania: US-01, US-02, US-03, US-04.
- **Sprint 2 (30.11 – 13.12):**
  - Cel: Moduł gazetki cyfrowej (EPIC-03) oraz katalog promocji (EPIC-04) zasilany danymi JSON.
  - Zadania: US-05, US-06.
- **Sprint 3 (14.12 – 10.01) *[Uwzględnia przerwę świąteczną]*:**
  - Cel: Interaktywna lista zakupów (EPIC-05) z integracją z katalogiem oraz lista sklepów (EPIC-06).
  - Zadania: US-07, US-08, US-09, US-10.
- **Sprint 4 / Faza Stabilizacji (11.01 – 24.01):**
  - Cel: Testy akceptacyjne UAT, usunięcie błędów regresyjnych, przygotowanie końcowej prezentacji Demo.

---

## 4. Pytania do Klienta (Prowadzącego) na spotkanie walidujące
1. Jaka forma prezentacji końcowej aplikacji mobilnej jest preferowana (fizyczny telefon / instalator .apk czy emulator w Android Studio / przeglądarka)?
2. Czy backend aplikacji może być uruchamiany lokalnie (localhost)?
3. W jakiej formie prowadzący będzie weryfikował artefakty PO (wgląd do repozytorium GitHub i tablicy Projects czy eksport raportu)?