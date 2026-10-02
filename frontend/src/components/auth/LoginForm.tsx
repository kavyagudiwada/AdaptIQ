import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { LogIn, Mail } from "lucide-react";
import { Button } from "@/components/common/Button";
import { FieldError, Input, Label } from "@/components/common/Form";
import { PasswordInput } from "@/components/auth/PasswordInput";
import { AuthDivider, GoogleSignInButton } from "@/components/auth/GoogleSignInButton";
import { useAuth } from "@/hooks/useAuth";
import { toFriendlyError } from "@/services/api";
import { googleSignInEnabled } from "@/services/authService";
import { AuthError } from "@/types/auth";
import type { AuthFieldErrors, AuthSession } from "@/types/auth";
import { cn } from "@/utils/cn";

/** Pragmatic check: something@something.tld, no exotic rules. */
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export function LoginForm({
  onAuthenticated,
}: {
  onAuthenticated: (session: AuthSession) => void;
}) {
  const { signIn } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(true);
  const [errors, setErrors] = useState<AuthFieldErrors>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [googleReady, setGoogleReady] = useState(false);
  const [googleChecked, setGoogleChecked] = useState(false);

  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);

  // Ask the backend whether Google sign-in is configured, so the page can
  // explain an unconfigured deployment instead of dead-ending the user.
  useEffect(() => {
    let cancelled = false;
    googleSignInEnabled()
      .then((enabled) => {
        if (!cancelled) setGoogleReady(enabled);
      })
      .catch(() => undefined)
      .finally(() => {
        if (!cancelled) setGoogleChecked(true);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  function validate(): AuthFieldErrors | null {
    const next: AuthFieldErrors = {};

    const trimmedEmail = email.trim();
    if (!trimmedEmail) {
      next.email = "Please enter your email.";
    } else if (!EMAIL_PATTERN.test(trimmedEmail)) {
      next.email = "Enter a valid email address.";
    }

    if (!password) {
      next.password = "Please enter your password.";
    }

    setErrors(next);
    return Object.keys(next).length === 0 ? null : next;
  }

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setSubmitError(null);

    const invalid = validate();
    if (invalid) {
      if (invalid.email) {
        emailRef.current?.focus();
      } else {
        passwordRef.current?.focus();
      }
      return;
    }

    setSubmitting(true);
    try {
      const session = await signIn({
        email: email.trim(),
        password,
        remember,
      });
      onAuthenticated(session);
    } catch (error) {
      setSubmitError(
        error instanceof AuthError ? error.message : toFriendlyError(error),
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-5" noValidate>
      <div>
        <Label htmlFor="login-email">Email</Label>
        <div className="relative">
          <Mail
            className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-400"
            aria-hidden
          />
          <Input
            ref={emailRef}
            id="login-email"
            type="email"
            value={email}
            onChange={(event) => {
              setEmail(event.target.value);
              setErrors((previous) => ({ ...previous, email: undefined }));
            }}
            placeholder="you@example.com"
            autoComplete="email"
            inputMode="email"
            aria-invalid={Boolean(errors.email)}
            className="pl-10"
          />
        </div>
        {errors.email ? <FieldError>{errors.email}</FieldError> : null}
      </div>

      <div>
        <Label htmlFor="login-password">Password</Label>
        <PasswordInput
          id="login-password"
          inputRef={passwordRef}
          value={password}
          onChange={(value) => {
            setPassword(value);
            setErrors((previous) => ({ ...previous, password: undefined }));
          }}
          error={errors.password}
          placeholder="Enter your password"
        />
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3">
        <label className="inline-flex cursor-pointer items-center gap-2 text-sm text-ink-600 select-none">
          <input
            id="login-remember"
            type="checkbox"
            checked={remember}
            onChange={(event) => setRemember(event.target.checked)}
            className={cn(
              "h-4 w-4 shrink-0 cursor-pointer rounded border-ink-300 text-brand-600",
              "accent-brand-600 focus-visible:outline-none focus-visible:ring-2",
              "focus-visible:ring-brand-500 focus-visible:ring-offset-2",
            )}
          />
          Remember me
        </label>

        <Link
          to="/forgot-password"
          className="text-sm font-medium text-ink-600 underline-offset-4 transition hover:text-ink-900 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500"
        >
          Forgot password?
        </Link>
      </div>

      <Button
        type="submit"
        size="lg"
        block
        loading={submitting}
        icon={submitting ? undefined : <LogIn className="h-4 w-4" />}
      >
        {submitting ? "Signing in…" : "Sign In"}
      </Button>

      {submitError ? (
        <p
          role="alert"
          className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700"
        >
          {submitError}
        </p>
      ) : null}

      {googleChecked ? (
        <>
          <AuthDivider />

          <div className="space-y-2">
            <GoogleSignInButton
              enabled={googleReady}
              onUnavailable={() =>
                setSubmitError(
                  "Google sign-in is not enabled on this deployment. Use your email and password instead.",
                )
              }
            />
            {!googleReady ? (
              <p
                id="google-unavailable"
                className="text-center text-xs text-ink-400"
              >
                Google sign-in isn&apos;t enabled on this deployment — use your
                email and password above. An administrator can enable it by
                setting GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.
              </p>
            ) : null}
          </div>
        </>
      ) : null}

      <p className="text-center text-sm text-ink-500">
        Don&apos;t have an account?{" "}
        <Link
          to="/signup"
          className={cn(
            "font-semibold text-brand-700 underline-offset-4 transition",
            "hover:text-brand-800 hover:underline",
            "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500",
          )}
        >
          Create account
        </Link>
      </p>
    </form>
  );
}
