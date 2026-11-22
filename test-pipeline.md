name: API Health Check

on:
  pull_request:
    branches: [ main, develop ]
  push:
    branches: [ main, develop ]

jobs:
  health-check:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout kodu
        uses: actions/checkout@v4

      - name: Konfiguracja Pythona
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Instalacja zależności testowych
        run: pip install pytest requests

      - name: Uruchomienie health check API
        env:
          API_URL: ${{ vars.API_TEST_URL }}
        run: pytest tests/test_health.py -v
