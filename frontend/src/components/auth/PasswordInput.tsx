import { useId, useState } from "react";
import type { Ref } from "react";
import { Eye, EyeOff } from "lucide-react";
import { FieldError, Input, Label } from "@/components/common/Form";
import { cn } from "@/utils/cn";

interface PasswordInputProps {
  /** Optional: omit when the surrounding layout renders its own label. */
  label?: string;
  /** Pass this when an external <label htmlFor> points at the field. */
  id?: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  placeholder?: string;
  autoComplete?: string;
  required?: boolean;
  inputRef?: Ref<HTMLInputElement>;
  /** Accessible name when an external <label> is used instead of `label`. */
  srLabel?: string;
}

/** Password field with a show/hide toggle, wired for screen readers. */
export function PasswordInput({
  label,
  id,
  value,
  onChange,
  error,
  placeholder,
  autoComplete = "current-password",
  required,
  inputRef,
  srLabel = "password",
}: PasswordInputProps) {
  const [visible, setVisible] = useState(false);
  const generatedId = useId();
  const inputId = id ?? `password-${generatedId}`;
  const errorId = `${inputId}-error`;
  const fieldName = (label ?? srLabel).toLowerCase();

  return (
    <div>
      {label ? <Label htmlFor={inputId}>{label}</Label> : null}
      <div className="relative">
        <Input
          ref={inputRef}
          id={inputId}
          type={visible ? "text" : "password"}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder={placeholder}
          autoComplete={autoComplete}
          required={required}
          aria-invalid={Boolean(error)}
          aria-describedby={error ? errorId : undefined}
          aria-label={label ? undefined : srLabel}
          className="pr-11"
        />
        <button
          type="button"
          onClick={() => setVisible((previous) => !previous)}
          aria-label={visible ? `Hide ${fieldName}` : `Show ${fieldName}`}
          aria-pressed={visible}
          className={cn(
            "absolute right-1.5 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center",
            "rounded-lg text-ink-400 transition hover:bg-ink-100 hover:text-ink-700",
            "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500",
          )}
        >
          {visible ? (
            <EyeOff className="h-4 w-4" aria-hidden />
          ) : (
            <Eye className="h-4 w-4" aria-hidden />
          )}
        </button>
      </div>
      {error ? (
        <div id={errorId}>
          <FieldError>{error}</FieldError>
        </div>
      ) : null}
    </div>
  );
}
