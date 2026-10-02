import { AlertCircle, Inbox, RefreshCw } from "lucide-react";
import { Button } from "./Button";
import { cn } from "@/utils/cn";

export function LoadingState({
  label = "Loading…",
  className,
}: {
  label?: string;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center gap-3 py-14 text-center",
        className,
      )}
      role="status"
      aria-live="polite"
    >
      <span className="h-8 w-8 animate-spin rounded-full border-[3px] border-brand-200 border-t-brand-600" />
      <p className="text-sm text-ink-500">{label}</p>
    </div>
  );
}

export function ErrorState({
  message,
  onRetry,
  className,
}: {
  message: string;
  onRetry?: () => void;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "flex flex-col items-center gap-3 rounded-2xl border border-rose-200 bg-rose-50/70 px-6 py-10 text-center",
        className,
      )}
      role="alert"
    >
      <AlertCircle className="h-7 w-7 text-rose-600" />
      <div>
        <p className="font-medium text-rose-900">Something went wrong</p>
        <p className="mt-1 max-w-md text-sm text-rose-700">{message}</p>
      </div>
      {onRetry ? (
        <Button variant="secondary" size="sm" icon={<RefreshCw className="h-3.5 w-3.5" />} onClick={onRetry}>
          Try again
        </Button>
      ) : null}
    </div>
  );
}

export function EmptyState({
  title,
  description,
  action,
  className,
}: {
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "flex flex-col items-center gap-3 rounded-2xl border border-dashed border-ink-300 bg-ink-50/60 px-6 py-12 text-center",
        className,
      )}
    >
      <Inbox className="h-7 w-7 text-ink-400" />
      <div>
        <p className="font-medium text-ink-800">{title}</p>
        {description ? (
          <p className="mt-1 max-w-md text-sm text-ink-500">{description}</p>
        ) : null}
      </div>
      {action}
    </div>
  );
}
