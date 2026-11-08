# Team Charter – Zespó Projektowy Dino App

## 1. Skad zespou i role bazowe
- **Adam Koczyba** – Product Owner / Project Manager (odpowiedzialny za backlog, zakres i relacj z klientem)
- **Jakub Góra** – UX / Frontend
- **Samuel Noszczyk** – Backend / Architektura
- **Piotr Panasiski** – DevOps / Platforma
- **Lucjan Klarecki** – QA / Tester

## 2. Kanay komunikacji
- **Gówny komunikator:** Discord / Teams (kanay tematyczne: `#general`, `#dev`, `#daily`, `#pytania-po`).
- **Repozytorium i zadania:** GitHub (Issues, Projects, Pull Requests).

## 3. Asynchroniczne Daily
- Odbywa si w dni robocze na dedykowanym kanale do godziny **10:00**.
- Kady czonek zespou wpisuje 3 punkty:
  1. Co zrobiem/am od ostatniego Daily?
  2. Co planuj zrobi dzisiaj?
  3. Czy mam jakiekolwiek blokery lub potrzebuj pomocy?

## 4. Rotacja Facylitatora (Scrum Mastera)
- Rola facylitatora sprintu rotuje co sprint pomidzy czonkami zespou deweloperskiego (Jakub -> Samuel -> Piotr -> Lucjan), aby kady zdoby dowiadczenie w prowadzeniu ceremonii.

## 5. Przepyw pracy i zasady Code Review
- Prace realizujemy na dedykowanych gaziach funkcjonalnych (`feature/nazwa-zadania`).
- Po ukoczeniu zadania deweloper otwiera **Pull Request** (PR) i przenosi kart do kolumny `In Review`.
- Do poczenia (merge) z gazi gówn wymagany jest co najmniej **jeden zatwierdzajcy review** od innego czonka zespou deweloperskiego.
- Po scaleniu kodu karta trafia do kolumny `Testing`, gdzie Lucjan weryfikuje kryteria akceptacji (UAT).
