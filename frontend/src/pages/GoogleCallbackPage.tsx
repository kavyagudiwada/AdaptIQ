import { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { Loader2 } from "lucide-react";
import { Button } from "@/components/common/Button";
import { useAuth } from "@/hooks/useAuth";
import { exchangeGoogleCode } from "@/services/authService";
import { toFriendlyError } from "@/services/api";
import { AuthError } from "@/types/auth";

/**
 * Landing point for the Google OAuth round trip.
 *
 * The backend redirects here with either a single-use `code` or an `error`
 * message. The code is swapped for a bearer token over POST, so no token ever
 * travels in a URL. React's StrictMode double-invokes effects in development,
 * which would burn the single-use code, so the exchange is guarded to run once
 * with a ref. No cleanup/cancel flag is used: the exchange must be allowed to
 * complete and navigate even if StrictMode tears the effect down and remounts.
 */
export default function GoogleCallbackPage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const { establishFromOAuth } = useAuth();

  const [error, setError] = useState<string | null>(
    params.get("error") ?? null,
  );
  const started = useRef(false);

  useEffect(() => {
    if (started.current) return;
    started.current = true;

    const code = params.get("code");
    if (!code) {
      if (!error) setError("Google sign-in did not complete.");
      return;
    }

    exchangeGoogleCode(code)
      .then((session) => establishFromOAuth(session))
      .then((session) => {
        if (!session) return;
        navigate(session.learner ? "/dashboard" : "/profile", { replace: true });
      })
      .catch((err) => {
        setError(
          err instanceof AuthError ? err.message : toFriendlyError(err),
        );
      });

    // Intentionally runs once: the code is single-use, so a re-run would fail.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-white px-5">
        <div className="w-full max-w-sm text-center">
          <h1 className="text-2xl font-bold tracking-tight text-ink-900">
            Google sign-in didn&apos;t finish
          </h1>
          <p role="alert" className="mt-3 text-sm text-ink-600">
            {error}
          </p>
          <div className="mt-7 space-y-3">
            <Button block size="lg" onClick={() => navigate("/login", { replace: true })}>
              Back to sign in
            </Button>
            <Link
              to="/signup"
              className="inline-block text-sm font-semibold text-brand-700 underline-offset-4 hover:underline"
            >
              Create an account instead
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-white px-5">
      <div className="text-center">
        <Loader2 className="mx-auto h-7 w-7 animate-spin text-brand-600" aria-hidden />
        <p className="mt-4 text-sm text-ink-600" role="status">
          Completing your Google sign-in…
        </p>
      </div>
    </div>
  );
}
