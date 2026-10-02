import type {
  ComponentProps,
  LabelHTMLAttributes,
} from "react";
import { cn } from "@/utils/cn";

export function Label({ className, ...props }: LabelHTMLAttributes<HTMLLabelElement>) {
  return (
    <label
      className={cn(
        "mb-2 block text-sm font-semibold text-ink-800",
        className,
      )}
      {...props}
    />
  );
}

const fieldBase =
  "w-full rounded-xl border border-ink-200 bg-white px-3.5 py-2.5 text-sm text-ink-900 " +
  "shadow-[0_1px_2px_rgba(16,24,40,0.04)] transition-all duration-200 " +
  "placeholder:text-ink-400 hover:border-ink-300 " +
  "focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/25 " +
  "focus:shadow-[0_0_0_4px_rgba(51,102,255,0.06),0_8px_20px_-8px_rgba(51,102,255,0.35)] " +
  "aria-invalid:border-rose-400 aria-invalid:focus:border-rose-500 aria-invalid:focus:ring-rose-500/25 " +
  "disabled:cursor-not-allowed disabled:bg-ink-50 disabled:text-ink-400";

/** `ComponentProps<"input">` keeps React 19 ref forwarding available. */
export function Input({ className, ...props }: ComponentProps<"input">) {
  return <input className={cn(fieldBase, className)} {...props} />;
}

export function Textarea({
  className,
  ...props
}: ComponentProps<"textarea">) {
  return <textarea className={cn(fieldBase, "resize-y", className)} {...props} />;
}

export function Select({
  className,
  ...props
}: ComponentProps<"select">) {
  return (
    <select
      className={cn(fieldBase, "cursor-pointer appearance-none bg-no-repeat pr-9", className)}
      style={{
        backgroundImage:
          "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%2366738d'><path d='M5.5 7.5l4.5 4.5 4.5-4.5' stroke='%2366738d' stroke-width='1.6' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>\")",
        backgroundPosition: "right 0.6rem center",
        backgroundSize: "1.15rem",
      }}
      {...props}
    />
  );
}

export function FieldHint({ children }: { children: React.ReactNode }) {
  return (
    <p className="mt-1.5 flex items-center gap-1.5 text-xs text-ink-500">
      <span aria-hidden className="h-1 w-1 shrink-0 rounded-full bg-ink-300" />
      {children}
    </p>
  );
}

export function FieldError({ children }: { children?: React.ReactNode }) {
  if (!children) return null;
  return (
    <p className="mt-2 flex items-center gap-1.5 text-xs font-medium text-rose-600">
      <span aria-hidden className="h-1.5 w-1.5 shrink-0 rounded-full bg-rose-500" />
      {children}
    </p>
  );
}
