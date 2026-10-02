import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { ReactNode } from "react";
import { useLearner } from "@/hooks/useLearner";
import { api } from "@/services/api";
import {
  clearStoredSession,
  getStoredSession,
  linkLearner as linkLearnerRequest,
  login as loginRequest,
  register as registerRequest,
  storeSession,
} from "@/services/authService";
import type {
  AuthSession,
  LoginCredentials,
  RegisterCredentials,
} from "@/types/auth";

interface AuthContextValue {
  session: AuthSession | null;
  isAuthenticated: boolean;
  loading: boolean;
  signIn: (credentials: LoginCredentials) => Promise<AuthSession>;
  signUp: (credentials: RegisterCredentials) => Promise<AuthSession>;
  /** Adopt a session that arrived via the Google OAuth round trip. */
  establishFromOAuth: (session: AuthSession) => Promise<AuthSession>;
  /** Attach a learner profile to the signed-in account. */
  linkLearner: (learnerId: number) => Promise<void>;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

/** Keep the default Authorization header in step with the active session. */
function applyAuthHeader(token: string | null) {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common.Authorization;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const { learner, adoptLearner } = useLearner();
  const [session, setSession] = useState<AuthSession | null>(null);
  const [loading, setLoading] = useState(true);

  // Restore the last session so a refresh does not sign the user out.
  useEffect(() => {
    const stored = getStoredSession();
    setSession(stored);
    applyAuthHeader(stored?.user.token ?? null);
    setLoading(false);
  }, []);

  const establish = useCallback(
    async (result: AuthSession, remember = true): Promise<AuthSession> => {
      // The rest of the app identifies people by learner id, so when the
      // account is already linked, adopt that learner straight away.
      if (result.learner) {
        try {
          await adoptLearner(result.learner.id);
        } catch {
          // Learner record missing or unreachable: keep the session, the
          // profile page can re-link a learner record.
        }
      } else if (learner) {
        // First sign-in on a device that already has a local learner profile.
        try {
          await linkLearnerRequest(result.user.token, learner.id);
          result = { ...result, learner: { id: learner.id, name: learner.name } };
        } catch {
          // Linking is best-effort; sign-in still succeeds.
        }
      }

      storeSession(result, remember);
      setSession(result);
      applyAuthHeader(result.user.token);
      return result;
    },
    [adoptLearner, learner],
  );

  const signIn = useCallback(
    (credentials: LoginCredentials) =>
      loginRequest(credentials).then((session) => establish(session, credentials.remember)),
    [establish],
  );

  const signUp = useCallback(
    (credentials: RegisterCredentials) => registerRequest(credentials).then(establish),
    [establish],
  );

  // Google hands back an already-formed session, so it only needs the same
  // adopt/link/persist treatment a password sign-in would get.
  const establishFromOAuth = useCallback(
    (session: AuthSession) => establish(session),
    [establish],
  );

  const linkLearner = useCallback(
    async (learnerId: number) => {
      if (!session) return;
      const confirmed = await linkLearnerRequest(session.user.token, learnerId);
      const next: AuthSession = {
        ...session,
        learner: session.learner ?? {
          id: confirmed ?? learnerId,
          name: session.user.name,
        },
      };
      storeSession(next);
      setSession(next);
    },
    [session],
  );

  const signOut = useCallback(() => {
    clearStoredSession();
    setSession(null);
    applyAuthHeader(null);
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      session,
      isAuthenticated: session !== null,
      loading,
      signIn,
      signUp,
      establishFromOAuth,
      linkLearner,
      signOut,
    }),
    [session, loading, signIn, signUp, establishFromOAuth, linkLearner, signOut],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used inside <AuthProvider>");
  }
  return ctx;
}
