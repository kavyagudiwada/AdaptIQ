import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { ReactNode } from "react";
import type { HealthResponse, LearnerProfile } from "@/types";
import { getHealth } from "@/services/progressService";
import { getLearner } from "@/services/learnerService";

const STORAGE_KEY = "learnai.learnerId";

interface LearnerContextValue {
  learner: LearnerProfile | null;
  learnerId: number | null;
  health: HealthResponse | null;
  setLearner: (learner: LearnerProfile) => void;
  /** Point localStorage at a learner id and load that profile. */
  adoptLearner: (id: number) => Promise<void>;
  refreshHealth: () => Promise<void>;
  resetLearner: () => void;
  loading: boolean;
  healthError: string | null;
}

const LearnerContext = createContext<LearnerContextValue | undefined>(undefined);

export function LearnerProvider({ children }: { children: ReactNode }) {
  const [learner, setLearnerState] = useState<LearnerProfile | null>(null);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [healthError, setHealthError] = useState<string | null>(null);

  const refreshHealth = useCallback(async () => {
    try {
      setHealth(await getHealth());
      setHealthError(null);
    } catch {
      setHealthError("Backend is not reachable. Start it on port 8000.");
    }
  }, []);

  // Restore the last learner so a page refresh does not lose progress.
  useEffect(() => {
    let cancelled = false;

    async function bootstrap() {
      await refreshHealth();
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored && !cancelled) {
        try {
          const id = Number(stored);
          if (Number.isFinite(id) && id > 0) {
            setLearnerState(await getLearner(id));
          }
        } catch {
          window.localStorage.removeItem(STORAGE_KEY);
        }
      }
      if (!cancelled) setLoading(false);
    }

    void bootstrap();
    return () => {
      cancelled = true;
    };
  }, [refreshHealth]);

  const setLearner = useCallback((next: LearnerProfile) => {
    setLearnerState(next);
    window.localStorage.setItem(STORAGE_KEY, String(next.id));
  }, []);

  // Used after sign-in, when the backend reports which learner the account is
  // linked to, so a returning user lands on their own progress.
  const adoptLearner = useCallback(async (id: number) => {
    window.localStorage.setItem(STORAGE_KEY, String(id));
    setLearnerState(await getLearner(id));
  }, []);

  const resetLearner = useCallback(() => {
    setLearnerState(null);
    window.localStorage.removeItem(STORAGE_KEY);
  }, []);

  const value = useMemo<LearnerContextValue>(
    () => ({
      learner,
      learnerId: learner?.id ?? null,
      health,
      setLearner,
      adoptLearner,
      refreshHealth,
      resetLearner,
      loading,
      healthError,
    }),
    [
      learner,
      health,
      setLearner,
      adoptLearner,
      refreshHealth,
      resetLearner,
      loading,
      healthError,
    ],
  );

  return (
    <LearnerContext.Provider value={value}>{children}</LearnerContext.Provider>
  );
}

export function useLearner(): LearnerContextValue {
  const ctx = useContext(LearnerContext);
  if (!ctx) {
    throw new Error("useLearner must be used inside <LearnerProvider>");
  }
  return ctx;
}
