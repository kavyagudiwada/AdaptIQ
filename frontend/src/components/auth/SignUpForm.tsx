import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import { Mail, UserPlus, UserRound } from "lucide-react";
import { Button } from "@/components/common/Button";
import { FieldError, Input, Label } from "@/components/common/Form";
import { PasswordInput } from "@/components/auth/PasswordInput";
import { useAuth } from "@/hooks/useAuth";
import { toFriendlyError } from "@/services/api";
import { AuthError } from "@/types/auth";
import type { AuthFieldErrors, AuthSession } from "@/types/auth";
import { cn } from "@/utils/cn";

/** Mirrors the backend rule: at least 8 characters. */
const MIN_PASSWORD_LENGTH = 8;
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

/** Rough strength read-out, used only to guide the user. */
function passwordStrength(password: string): { label: string; className: string } {
  let score = 0;
  if (password.length >= MIN_PASSWORD_LENGTH) score += 1;
  if (password.length >= 12) score += 1;
  if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score += 1;
  if (/\d/.test(password)) score += 1;
  if (/[^A-Za-z0-9]/.test(password)) score += 1;

  if (score <= 2) return { label: "Weak", className: "bg-rose-500" };
  if (score <= 3) return { label: "Fair", className: "bg-amber-500" };
  return { label: "Strong", className: "bg-emerald-500" };
}

export function SignUpForm({
  onRegistered,
}: {
  onRegistered: (session: AuthSession) => void;
}) {
  const { signUp } = useAuth();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errors, setErrors] = useState<AuthFieldErrors>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const nameRef = useRef<HTMLInputElement>(null);
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const confirmRef = useRef<HTMLInputElement>(null);

  function validate(): AuthFieldErrors | null {
    const next: AuthFieldErrors = {};

    if (!name.trim()) {
      next.name = "Please enter your name.";
    }

    const trimmedEmail = email.trim();
    if (!trimmedEmail) {
      next.email = "Please enter your email.";
    } else if (!EMAIL_PATTERN.test(trimmedEmail)) {
      next.email = "Enter a valid email address.";
    }

    if (!password) {
      next.password = "Please choose a password.";
    } else if (password.length < MIN_PASSWORD_LENGTH) {
      next.password = `Use at least ${MIN_PASSWORD_LENGTH} characters.`;
    }

    if (!confirmPassword) {
      next.confirmPassword = "Please confirm your password.";
    } else if (confirmPassword !== password) {
      next.confirmPassword = "Passwords do not match.";
    }

    setErrors(next);
    return Object.keys(next).length === 0 ? null : next;
  }

  function focusFirstError(invalid: AuthFieldErrors) {
    if (invalid.name) nameRef.current?.focus();
    else if (invalid.email) emailRef.current?.focus();
    else if (invalid.password) passwordRef.current?.focus();
    else if (invalid.confirmPassword) confirmRef.current?.focus();
  }

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setSubmitError(null);

    const invalid = validate();
    if (invalid) {
      focusFirstError(invalid);
      return;
    }

    setSubmitting(true);
    try {
      const session = await signUp({
        name: name.trim(),
        email: email.trim(),
        password,
      });
      onRegistered(session);
    } catch (error) {
      setSubmitError(
        error instanceof AuthError ? error.message : toFriendlyError(error),
      );
    } finally {
      setSubmitting(false);
    }
  }

  const strength = password ? passwordStrength(password) : null;

  return (
    <form onSubmit={onSubmit} className="space-y-5" noValidate>
      <div>
        <Label htmlFor="signup-name">Full name</Label>
        <div className="relative">
          <UserRound
            className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-400"
            aria-hidden
          />
          <Input
            ref={nameRef}
            id="signup-name"
            type="text"
            value={name}
            onChange={(event) => {
              setName(event.target.value);
              setErrors((previous) => ({ ...previous, name: undefined }));
            }}
            placeholder="Kavya Rao"
            autoComplete="name"
            aria-invalid={Boolean(errors.name)}
            className="pl-10"
          />
        </div>
        {errors.name ? <FieldError>{errors.name}</FieldError> : null}
      </div>

      <div>
        <Label htmlFor="signup-email">Email</Label>
        <div className="relative">
          <Mail
            className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-400"
            aria-hidden
          />
          <Input
            ref={emailRef}
            id="signup-email"
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
        <div className="mb-1.5 flex items-baseline justify-between gap-3">
          <Label htmlFor="signup-password" className="mb-0">
            Password
          </Label>
          {strength ? (
            <span className="flex items-center gap-2 text-xs text-ink-500">
              <span className="h-1.5 w-16 overflow-hidden rounded-full bg-ink-200">
                <span
                  className={cn("block h-full rounded-full", strength.className)}
                  style={{ width: strength.label === "Weak" ? "33%" : strength.label === "Fair" ? "66%" : "100%" }}
                />
              </span>
              {strength.label}
            </span>
          ) : null}
        </div>
        <PasswordInput
          id="signup-password"
          inputRef={passwordRef}
          value={password}
          onChange={(value) => {
            setPassword(value);
            setErrors((previous) => ({ ...previous, password: undefined }));
          }}
          error={errors.password}
          placeholder="At least 8 characters"
          autoComplete="new-password"
        />
        {!errors.password ? (
          <p className="mt-1.5 text-xs text-ink-500">
            Use 8 or more characters. A mix of letters, numbers and symbols works
            best.
          </p>
        ) : null}
      </div>

      <div>
        <Label htmlFor="signup-confirm">Confirm password</Label>
        <PasswordInput
          id="signup-confirm"
          inputRef={confirmRef}
          value={confirmPassword}
          onChange={(value) => {
            setConfirmPassword(value);
            setErrors((previous) => ({
              ...previous,
              confirmPassword: undefined,
            }));
          }}
          error={errors.confirmPassword}
          placeholder="Re-enter your password"
          autoComplete="new-password"
          srLabel="Confirm password"
        />
      </div>

      <Button
        type="submit"
        size="lg"
        block
        loading={submitting}
        icon={submitting ? undefined : <UserPlus className="h-4 w-4" />}
      >
        {submitting ? "Creating account…" : "Create Account"}
      </Button>

      {submitError ? (
        <p
          role="alert"
          className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700"
        >
          {submitError}
        </p>
      ) : null}

      <p className="text-center text-sm text-ink-500">
        Already have an account?{" "}
        <Link
          to="/login"
          className={cn(
            "font-semibold text-brand-700 underline-offset-4 transition",
            "hover:text-brand-800 hover:underline",
            "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500",
          )}
        >
          Sign in
        </Link>
      </p>
    </form>
  );
}
