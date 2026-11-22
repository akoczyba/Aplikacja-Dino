import { http, HttpResponse } from "msw";

interface Consents {
  terms_accepted: boolean;
  privacy_policy_accepted: boolean;
  marketing_push: boolean;
  marketing_sms: boolean;
}

interface LoyaltyCard {
  card_number: string;
  points_balance: number;
  barcode_format: string;
}

interface MockUser {
  id: string;
  email: string;
  password: string; // tylko w mocku (w prawdziwym backendzie jest password_hash)
  first_name: string | null;
  phone_number: string | null;
  created_at: string;
  loyalty_card: LoyaltyCard;
  consents: Consents;
}

const generateCardNumber = () =>
  "290" + Array.from({ length: 10 }, () => Math.floor(Math.random() * 10)).join("");

const sanitizeUser = ({ password: _, ...user }: MockUser) => user;

let mockUsers: MockUser[] = [
  {
    id: "11111111-1111-4111-8111-111111111111",
    email: "test@email.pl",
    password: "Password1",
    first_name: "Jan",
    phone_number: "+48500600700",
    created_at: new Date().toISOString(),
    loyalty_card: {
      card_number: "2901234567890",
      points_balance: 120,
      barcode_format: "EAN13",
    },
    consents: {
      terms_accepted: true,
      privacy_policy_accepted: true,
      marketing_push: true,
      marketing_sms: false,
    },
  },
];

const MOCK_TOKEN_PREFIX = "mock-jwt-token-";

function getUserFromAuthHeader(authHeader: string | null): MockUser | null {
  if (!authHeader?.startsWith(`Bearer ${MOCK_TOKEN_PREFIX}`)) return null;
  const userId = authHeader.replace(`Bearer ${MOCK_TOKEN_PREFIX}`, "").trim();
  return mockUsers.find((u) => u.id === userId) ?? null;
}

export const handlers = [
  // POST /auth/register
  http.post("*/auth/register", async ({ request }) => {
    const body = (await request.json()) as {
      email?: string;
      password?: string;
      phone_number?: string | null;
      first_name?: string | null;
      terms_accepted?: boolean;
      privacy_policy_accepted?: boolean;
      marketing_push?: boolean;
      marketing_sms?: boolean;
    };

    const fieldErrors: Record<string, string> = {};
    if (!body.email || !body.email.includes("@")) {
      fieldErrors.email = "Podaj poprawny adres e-mail.";
    }
    if (!body.password || body.password.length < 8) {
      fieldErrors.password = "Hasło musi mieć co najmniej 8 znaków.";
    }
    if (Object.keys(fieldErrors).length > 0) {
      return HttpResponse.json(
        {
          success: false,
          error_code: "VALIDATION_ERROR",
          message: "Sprawdź poprawność wprowadzonych danych.",
          field_errors: fieldErrors,
          data: null,
        },
        { status: 422 }
      );
    }

    if (!body.terms_accepted || !body.privacy_policy_accepted) {
      return HttpResponse.json(
        {
          success: false,
          error_code: "HTTP_400",
          message: "Akceptacja regulaminu i polityki prywatności jest wymagana.",
          data: null,
        },
        { status: 400 }
      );
    }

    if (mockUsers.some((u) => u.email.toLowerCase() === body.email!.toLowerCase())) {
      return HttpResponse.json(
        {
          success: false,
          error_code: "HTTP_409",
          message: "Konto z tym adresem e-mail już istnieje.",
          data: null,
        },
        { status: 409 }
      );
    }

    if (body.phone_number && mockUsers.some((u) => u.phone_number === body.phone_number)) {
      return HttpResponse.json(
        {
          success: false,
          error_code: "HTTP_409",
          message: "Ten numer telefonu jest już przypisany do innego konta.",
          data: null,
        },
        { status: 409 }
      );
    }

    const newUser: MockUser = {
      id: crypto.randomUUID(),
      email: body.email!,
      password: body.password!,
      first_name: body.first_name ?? null,
      phone_number: body.phone_number ?? null,
      created_at: new Date().toISOString(),
      loyalty_card: {
        card_number: generateCardNumber(),
        points_balance: 0,
        barcode_format: "EAN13",
      },
      consents: {
        terms_accepted: Boolean(body.terms_accepted),
        privacy_policy_accepted: Boolean(body.privacy_policy_accepted),
        marketing_push: Boolean(body.marketing_push),
        marketing_sms: Boolean(body.marketing_sms),
      },
    };

    mockUsers.push(newUser);

    return HttpResponse.json(
      {
        success: true,
        message: "Konto zostało utworzone pomyślnie.",
        data: {
          token: {
            access_token: `${MOCK_TOKEN_PREFIX}${newUser.id}`,
            token_type: "bearer",
            expires_in: 3600,
          },
          user: sanitizeUser(newUser),
        },
      },
      { status: 201 }
    );
  }),

  // POST /auth/login
  http.post("*/auth/login", async ({ request }) => {
    const body = (await request.json()) as { email?: string; password?: string };

    const user = mockUsers.find(
      (u) =>
        u.email.toLowerCase() === (body.email ?? "").toLowerCase() &&
        u.password === body.password
    );

    if (!user) {
      return HttpResponse.json(
        {
          success: false,
          error_code: "HTTP_401",
          message: "Nieprawidłowy adres e-mail lub hasło.",
          data: null,
        },
        { status: 401 }
      );
    }

    return HttpResponse.json({
      success: true,
      message: "Zalogowano pomyślnie.",
      data: {
        token: {
          access_token: `${MOCK_TOKEN_PREFIX}${user.id}`,
          token_type: "bearer",
          expires_in: 3600,
        },
        user: sanitizeUser(user),
      },
    });
  }),

  // GET /users/me
  http.get("*/users/me", ({ request }) => {
    const user = getUserFromAuthHeader(request.headers.get("Authorization"));

    if (!user) {
      return HttpResponse.json(
        {
          success: false,
          error_code: "HTTP_401",
          message: "Sesja wygasła lub token jest nieprawidłowy.",
          data: null,
        },
        { status: 401 }
      );
    }

    return HttpResponse.json({
      success: true,
      message: "Pobrano dane profilu.",
      data: sanitizeUser(user),
    });
  }),

  // PATCH /users/me/consents
  http.patch("*/users/me/consents", async ({ request }) => {
    const user = getUserFromAuthHeader(request.headers.get("Authorization"));

    if (!user) {
      return HttpResponse.json(
        {
          success: false,
          error_code: "HTTP_401",
          message: "Sesja wygasła lub token jest nieprawidłowy.",
          data: null,
        },
        { status: 401 }
      );
    }

    const body = (await request.json()) as {
      marketing_push?: boolean | null;
      marketing_sms?: boolean | null;
    };

    if (typeof body.marketing_push === "boolean") {
      user.consents.marketing_push = body.marketing_push;
    }
    if (typeof body.marketing_sms === "boolean") {
      user.consents.marketing_sms = body.marketing_sms;
    }

    return HttpResponse.json({
      success: true,
      message: "Zaktualizowano zgody marketingowe.",
      data: user.consents,
    });
  }),
];