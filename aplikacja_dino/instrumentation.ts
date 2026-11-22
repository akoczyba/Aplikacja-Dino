export async function register() {
  if (
    process.env.NODE_ENV === "development" &&
    process.env.NEXT_RUNTIME === "nodejs"
  ) {
    if (!(globalThis as any)._mswServerStarted) {
      const { server } = await import("./mocks/server");

      // Dodanie "as any" wycisza błąd TypeScriptu, pozwalając na kompilację
      server.listen({ onUnhandledRequest: "bypass" } as any);

      (globalThis as any)._mswServerStarted = true;
      console.log("[MSW] Serwer mocków dla Node.js został uruchomiony.");
    }
  }
}