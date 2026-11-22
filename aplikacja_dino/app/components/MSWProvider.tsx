"use client";
import { useEffect } from "react";

// Zmienna globalna chroniąca przed podwójnym wywołaniem w React StrictMode
let isMockingStarted = false;

export function MSWProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    if (typeof window !== "undefined" && process.env.NODE_ENV === "development") {
      if (!isMockingStarted) {
        isMockingStarted = true;

        import("@/mocks/browser").then(({ worker }) => {
          worker.start({
            // Zamiast prostego "bypass", używamy funkcji filtrującej
            onUnhandledRequest(request, print) {
              // Całkowicie ignorujemy wewnętrzny ruch Next.js (w tym WebSocket _next/hmr)
              if (request.url.includes("_next")) {
                return;
              }
              // Dla reszty zapytań zostawiamy standardowe zachowanie (ostrzeżenie)
              print.warning();
            },
          }).catch(() => {
            // Ciche zignorowanie błędu, jeśli worker mimo wszystko spróbuje wstać ponownie
          });
        });
      }
    }
  }, []);

  return <>{children}</>;
}