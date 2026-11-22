"use client";

import { useEffect, useState } from "react";

let workerStartPromise: Promise<unknown> | null = null;
let isWorkerStarted = false;

async function startMockWorkerOnce() {
  if (isWorkerStarted) return;
  if (workerStartPromise) {
    await workerStartPromise;
    return;
  }

  workerStartPromise = (async () => {
    const { worker } = await import("../../mocks/browser");
    await worker.start({
      onUnhandledRequest: "bypass",
    } as Parameters<typeof worker.start>[0]);
    isWorkerStarted = true;
  })();

  try {
    await workerStartPromise;
  } finally {
    workerStartPromise = null;
  }
}

export function MSWProvider({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(process.env.NODE_ENV !== "development");

  useEffect(() => {
    if (process.env.NODE_ENV !== "development") return;
    if (typeof window === "undefined") return;

    let active = true;

    startMockWorkerOnce()
      .catch((err) => {
        console.error("MSW start error:", err);
      })
      .finally(() => {
        if (active) setReady(true);
      });

    return () => {
      active = false;
    };
  }, []);

  // Nie blokuj drzewa przez zwracanie `null` — zachowuje hydratację i nawigację segmentów
  void ready;
  return <>{children}</>;
}