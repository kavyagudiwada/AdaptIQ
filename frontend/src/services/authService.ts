import axios from "axios";
import { API_URL, api, toFriendlyError } from "./api";
import { AuthError } from "@/types/auth";
import type { AuthSession, LoginCredentials, RegisterCredentials } from "@/types/auth";

/**
 * Auth endpoints are configurable so the base URL is never hardcoded. Both are
 * relative to the existing `VITE_API_URL` base (see `services/api.ts`).
 */
export const AUTH_LOGIN_PATH: string =
  import.meta.env.VITE_AUTH_LOGIN_PATH || "/auth/login";

export const AUTH_REGISTER_PATH: string =
  import.meta.env.VITE_AUTH_REGISTER_PATH || "/auth/register";

const AUTH_ME_PATH = "/auth/me";
const AUTH_LINK_LEARNER_PATH = "/auth/me/learner";
const AUTH_GOOGLE_STATUS_PATH = "/auth/google/status";
const AUTH_GOOGLE_EXCHANGE_PATH = "/auth/google/exchange";

const SESSION_KEY = "learnai.auth.session";

/* -------------------------------------------------------------------------- */
/* Response normalisation                                                      */
/* -------------------------------------------------------------------------- */

interface AuthPayload {
  access_token?: string;
  token?: string;
  expires_in?: number;
  learner_id?: number | null;
  account?: {
    id?: number;
    email?: string;
    name?: string;
    learner_id?: number | null;
  };
  id?: number;
  email?: string;
  name?: string;
}

function toSession(payload: unknown, fallbackEmail: string): AuthSession {
  const data = (payload ?? {}) as AuthPayload;
  const account = data.account ?? {};

  const token = data.access_token ?? data.token ?? "";
  const email = account.email ?? data.email ?? fallbackEmail;
  const name = account.name ?? data.name ?? displayNameFromEmail(email);
  const accountId = account.id ?? data.id ?? null;
  const learnerId = account.learner_id ?? data.learner_id ?? null;

  return {
    user: { email, name, token, accountId: accountId ?? null },
    learner: learnerId ? { id: learnerId, name } : null,
    issuedAt: new Date().toISOString(),
    expiresIn: typeof data.expires_in === "number" ? data.expires_in : null,
  };
}

/** "kavya.rao@example.com" -> "Kavya Rao" */
function displayNameFromEmail(email: string): string {
  const local = email.split("@")[0] ?? email;
  const words = local
    .replace(/[._-]+/g, " ")
    .trim()
    .split(/\s+/)
    .filter(Boolean);

  if (words.length === 0) return "Learner";
  return words.map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(" ");
}

/* -------------------------------------------------------------------------- */
/* Errors                                                                      */
/* -------------------------------------------------------------------------- */

function toAuthError(error: unknown): AuthError {
  if (error instanceof AuthError) return error;

  if (axios.isAxiosError(error)) {
    const status = error.response?.status ?? null;
    const detail = (error.response?.data as { detail?: unknown } | undefined)?.detail;
    const detailText = typeof detail === "string" ? detail : null;

    if (!error.response) {
      return new AuthError(
        `Cannot reach the backend at ${API_URL}. Is it running?`,
        "network",
      );
    }
    if (status === 409) {
      return new AuthError(
        detailText ?? "An account with that email already exists.",
        "email-taken",
        status,
      );
    }
    if (status === 401 || status === 403) {
      return new AuthError(
        detailText ?? "That email and password combination is incorrect.",
        "invalid-credentials",
        status,
      );
    }
    if (status === 422) {
      return new AuthError(
        detailText ?? "Check the details you entered, then try again.",
        "validation",
        status,
      );
    }
    return new AuthError(toFriendlyError(error), "server", status);
  }

  return new AuthError(
    "Something went wrong while signing in. Please try again.",
    "unexpected",
  );
}

/* -------------------------------------------------------------------------- */
/* Public API                                                                  */
/* -------------------------------------------------------------------------- */

/** Sign in with email + password and return a bearer-token session. */
export async function login(credentials: LoginCredentials): Promise<AuthSession> {
  const email = credentials.email.trim();
  try {
    const { data } = await api.post(AUTH_LOGIN_PATH, {
      email,
      password: credentials.password,
    });
    return toSession(data, email);
  } catch (error) {
    throw toAuthError(error);
  }
}

/** Create an account and return a ready-to-use session. */
export async function register(
  credentials: RegisterCredentials,
): Promise<AuthSession> {
  const email = credentials.email.trim();
  try {
    const { data } = await api.post(AUTH_REGISTER_PATH, {
      name: credentials.name.trim(),
      email,
      password: credentials.password,
    });
    return toSession(data, email);
  } catch (error) {
    throw toAuthError(error);
  }
}

function bearer(token: string) {
  return { Authorization: `Bearer ${token}` };
}

/**
 * Whether the backend has Google sign-in configured.
 *
 * A failure here is not an error worth surfacing: it just means the button
 * falls back to its "not enabled on this deployment" explanation.
 */
export async function googleSignInEnabled(): Promise<boolean> {
  try {
    const { data } = await api.get<{ enabled?: boolean }>(
      AUTH_GOOGLE_STATUS_PATH,
      { timeout: 8000 },
    );
    return data?.enabled === true;
  } catch {
    return false;
  }
}

/**
 * Redeem the single-use code handed back by the OAuth callback for a session.
 * The code is consumed server-side, so a replayed callback cannot mint a second
 * token.
 */
export async function exchangeGoogleCode(
  code: string,
): Promise<AuthSession> {
  try {
    const { data } = await api.post(AUTH_GOOGLE_EXCHANGE_PATH, { code });
    return toSession(data, "");
  } catch (error) {
    throw toAuthError(error);
  }
}

/** Fetch the account behind a stored token (used to validate a restored session). */
export async function getMe(token: string): Promise<{ email: string; name: string }> {
  try {
    const { data } = await api.get(AUTH_ME_PATH, { headers: bearer(token) });
    const account = (data ?? {}) as { email?: string; name?: string };
    return {
      email: account.email ?? "",
      name: account.name ?? displayNameFromEmail(account.email ?? ""),
    };
  } catch (error) {
    throw toAuthError(error);
  }
}

/** Attach a learner record so the next sign-in restores that progress. */
export async function linkLearner(
  token: string,
  learnerId: number,
): Promise<number | null> {
  try {
    const { data } = await api.post(
      AUTH_LINK_LEARNER_PATH,
      { learner_id: learnerId },
      { headers: bearer(token) },
    );
    const account = (data ?? {}) as { learner_id?: number | null };
    return account.learner_id ?? learnerId;
  } catch (error) {
    throw toAuthError(error);
  }
}

/* -------------------------------------------------------------------------- */
/* Session persistence (mirrors the `learnai.learnerId` localStorage approach)  */
/* -------------------------------------------------------------------------- */

/**
 * Read the persisted session, preferring a remembered one. A session stored
 * without "remember me" lives in `sessionStorage`, so it dies with the tab.
 */
export function getStoredSession(): AuthSession | null {
  for (const store of [window.localStorage, window.sessionStorage]) {
    try {
      const raw = store.getItem(SESSION_KEY);
      if (!raw) continue;
      const parsed = JSON.parse(raw) as AuthSession | null;
      if (parsed?.user?.email && parsed?.user?.token) return parsed;
    } catch {
      // Unreadable entry: fall through and try the other store.
    }
  }
  return null;
}

/**
 * Persist the session. `remember: true` (the default) keeps it across browser
 * restarts; `false` scopes it to this tab. Whichever store is not used is
 * cleared, so toggling the checkbox can never leave a stale token behind.
 */
export function storeSession(session: AuthSession, remember = true): void {
  const target = remember ? window.localStorage : window.sessionStorage;
  const other = remember ? window.sessionStorage : window.localStorage;

  try {
    other.removeItem(SESSION_KEY);
  } catch {
    // Ignore storage failures.
  }
  try {
    target.setItem(SESSION_KEY, JSON.stringify(session));
  } catch {
    // Private browsing / quota errors should never break sign-in.
  }
}

export function clearStoredSession(): void {
  for (const store of [window.localStorage, window.sessionStorage]) {
    try {
      store.removeItem(SESSION_KEY);
    } catch {
      // Ignore storage failures.
    }
  }
}
