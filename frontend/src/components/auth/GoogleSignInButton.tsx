import { useState } from "react";
import { cn } from "@/utils/cn";
import { API_URL } from "@/services/api";

/**
 * Original LearnAI mark for the Google button: a four-point sparkle, kept
 * inline so there is no extra network request and no third-party asset.
 */
function GoogleMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={cn("h-4 w-4", className)} aria-hidden>
      <path
        fill="#4285F4"
        d="M23.5 12.27c0-.79-.07-1.54-.2-2.27H12v4.51h6.47a5.54 5.54 0 0 1-2.4 3.63v3.02h3.88c2.27-2.09 3.55-5.17 3.55-8.89Z"
      />
      <path
        fill="#34A853"
        d="M12 24c3.24 0 5.96-1.08 7.95-2.91l-3.88-3.01c-1.08.72-2.45 1.16-4.07 1.16-3.13 0-5.78-2.11-6.73-4.96H1.29v3.13A12 12 0 0 0 12 24Z"
      />
      <path
        fill="#FBBC05"
        d="M5.27 14.28a7.2 7.2 0 0 1 0-4.56V6.59H1.29a12 12 0 0 0 0 10.82l3.98-3.13Z"
      />
      <path
        fill="#EA4335"
        d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.43-3.43C17.95 1.19 15.24 0 12 0A12 12 0 0 0 1.29 6.59l3.98 3.13C6.22 6.87 8.87 4.75 12 4.75Z"
      />
    </svg>
  );
}

/** "OR" rule between the email form and third-party sign-in. */
export function AuthDivider({ label = "OR" }: { label?: string }) {
  return (
    <div className="flex items-center gap-3" role="separator">
      <span className="h-px flex-1 bg-ink-200" />
      <span className="text-[11px] font-semibold uppercase tracking-wider text-ink-400">
        {label}
      </span>
      <span className="h-px flex-1 bg-ink-200" />
    </div>
  );
}

/**
 * "Continue with Google".
 *
 * When the backend has Google credentials configured the button hands off to
 * the OAuth flow. When it does not, the button stays visible (it is part of the
 * page design) but explains that the deployment has not enabled it, rather than
 * silently doing nothing when clicked.
 */
export function GoogleSignInButton({
  enabled,
  onUnavailable,
  className,
}: {
  enabled: boolean;
  onUnavailable: () => void;
  className?: string;
}) {
  const [busy, setBusy] = useState(false);

  function handleClick() {
    if (!enabled) {
      onUnavailable();
      return;
    }
    setBusy(true);
    // Full navigation: the OAuth round trip returns to the frontend origin.
    // Same-origin by default (deployed single-origin); dev machines override
    // with VITE_API_URL in frontend/.env (e.g. http://127.0.0.1:8000).
    window.location.assign(`${API_URL}/api/auth/google/start`);
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={busy}
      aria-describedby={enabled ? undefined : "google-unavailable"}
      className={cn(
        "inline-flex h-12 w-full items-center justify-center gap-2.5 rounded-xl",
        "bg-white text-sm font-semibold text-ink-800 ring-1 ring-ink-200",
        "transition-all hover:bg-ink-50 active:bg-ink-100",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500",
        "focus-visible:ring-offset-2 disabled:opacity-60",
        className,
      )}
    >
      <GoogleMark />
      {busy ? "Opening Google…" : "Continue with Google"}
    </button>
  );
}
