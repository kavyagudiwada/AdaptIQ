import { Link } from "react-router-dom";
import { cn } from "@/utils/cn";

export function PageHeader({
  eyebrow,
  title,
  description,
  action,
  className,
  variant = "default",
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
  variant?: "default" | "light";
}) {
  return (
    <div
      className={cn(
        "mb-6 flex flex-wrap items-end justify-between gap-4",
        className,
      )}
    >
      <div className="min-w-0">
        {eyebrow ? (
          <p
            className={cn(
              "mb-1 text-xs font-semibold uppercase tracking-wider",
              variant === "light" ? "text-cyan-300" : "text-brand-600",
            )}
          >
            {eyebrow}
          </p>
        ) : null}
        <h1
          className={cn(
            "text-2xl font-bold tracking-tight sm:text-3xl",
            variant === "light" ? "text-white" : "text-ink-900",
          )}
        >
          {title}
        </h1>
        {description ? (
          <p
            className={cn(
              "mt-2 max-w-2xl text-sm",
              variant === "light" ? "text-ink-300" : "text-ink-500",
            )}
          >
            {description}
          </p>
        ) : null}
      </div>
      {action ? <div className="shrink-0">{action}</div> : null}
    </div>
  );
}

/** Inline panel that asks the learner to finish an earlier step first. */
export function StepGate({
  title,
  description,
  cta,
  to,
}: {
  title: string;
  description: string;
  cta: string;
  to: string;
}) {
  return (
    <div className="rounded-2xl border border-ink-200 bg-white px-6 py-12 text-center shadow-sm">
      <h2 className="text-lg font-semibold text-ink-900">{title}</h2>
      <p className="mx-auto mt-2 max-w-md text-sm text-ink-500">{description}</p>
      <Link
        to={to}
        className="mt-5 inline-flex h-10 items-center rounded-xl bg-brand-600 px-4 text-sm font-medium text-white shadow-sm transition hover:bg-brand-700"
      >
        {cta}
      </Link>
    </div>
  );
}
