Poziomy testów:

- Testy jednostkowe (Unit): Weryfikują pojedyncze funkcje, komponenty i logikę biznesową (np. walidację formularzy autentykacji,
  obsługę punktów w trybie demo, logikę listy zakupów), realizowane przez zespół deweloperski.
  
- Testy API (integracyjne i kontraktowe): Sprawdzają komunikację między warstwą kliencką a backendem, kody odpowiedzi HTTP,
  obsługę błędów oraz zgodność struktur JSON (w tym danych zasilających typu seed data dla promocji i gazetek).
  
- Testy E2E i UI: Weryfikują pełne ścieżki użytkownika od startu aplikacji po główne akcje w interfejsie
  (logowanie, wyświetlenie karty z kodem kreskowym/QR, przeglądanie promocji/gazetki, zarządzanie listą zakupów).

- Testy użyteczności i dostępności (Usability / Accessibility): Skupiają się na prostocie i czytelności interfejsu pod kątem odbiorców opisanych w projekcie,
  m.in. klientów szukających oszczędności i szybkiego planowania zakupów (jak Marcin) oraz osób mniej przekonanych do współczesnej technologii lub starszych (jak Andrzej).

- Testy regresyjne i akceptacyjne (UAT): Prowadzone szczególnie w fazie stabilizacji po wdrożeniu kolejnych sprintów, aby upewnić się, że nowe zmiany nie popsuły wcześniej działających funkcji.

  Pomijamy obszary wskazae jako Out of scope (brak płatności online, brak zamówień i dostaw, brak integracji z realnymi systemami/kasami Dino oraz brak weryfikacji SMS)

Narzędzia:

- Zarządzanie zadaniami, błędami, procesem: GitHub
- 
- Testy API: Pytest (automatyczne testy), Bruno lub Postman (ręczne testy)
- 
- Testy E2E mobilne: Maestro

Kryteria zakończenia testów:

Testy dla danego sprintu uznaje się za zakończone gdy spełnione są następujące warunki

- Wykonanie planu testów: Wykonano 100% zaplanowanych przypadków testowych dla funkcji o priorytecie MUST HAVE oraz co najmniej 90% dla SHOULD HAVE (zgodnie z zakresem MVP i backlogiem).

- Brak błędów krytycznych: Liczba otwartych defektów o priorytecie Blocker oraz Critical wynosi 0, a ewentualne błędy niższej wagi (Major / Minor) są opisane i zaakceptowane przez Product Ownera

- Potwierdzenie kryteriów akceptacji: Wszystkie zrealizowane historyjki użytkownika w testowanym zakresie spełniają uzgodnione kryteria akceptacji i przeszły weryfikację w kolumnie Testing.
