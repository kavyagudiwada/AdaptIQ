/**
 * Authentication shapes.
 *
 * Kept apart from the domain types in `@/types` because sign-in talks to a
 * different endpoint family than the learner/assessment APIs.
 */

export interface LoginCredentials {
  email: string;
  password: string;
  /**
   * When false the session is kept in `sessionStorage` only, so closing the
   * tab signs the user out. Defaults to true (persist across restarts).
   */
  remember?: boolean;
}

export interface RegisterCredentials extends LoginCredentials {
  name: string;
}

export interface AuthUser {
  email: string;
  name: string;
  /** Bearer token issued by the backend. */
  token: string;
  accountId: number | null;
}

/** Links the session to the learner record the rest of the app already uses. */
export interface AuthLearnerRef {
  id: number;
  name: string;
}

export interface AuthSession {
  user: AuthUser;
  learner: AuthLearnerRef | null;
  issuedAt: string;
  /** Seconds until the bearer token expires. */
  expiresIn: number | null;
}

export type AuthField = "name" | "email" | "password" | "confirmPassword";

export type AuthFieldErrors = Partial<Record<AuthField, string>>;

export type AuthErrorCode =
  | "invalid-credentials"
  | "email-taken"
  | "validation"
  | "server"
  | "network"
  | "unexpected";

/** Typed failure so the UI can show a specific, friendly message per case. */
export class AuthError extends Error {
  readonly code: AuthErrorCode;
  readonly status: number | null;

  constructor(message: string, code: AuthErrorCode, status: number | null = null) {
    super(message);
    this.name = "AuthError";
    this.code = code;
    this.status = status;
  }
}
