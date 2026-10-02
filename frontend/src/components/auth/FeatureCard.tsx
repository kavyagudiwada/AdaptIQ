import type { LucideIcon } from "lucide-react";
import { cn } from "@/utils/cn";

/**
 * Compact white card used in the four-across feature row. Each card pairs a
 * coloured icon tile with a title and one short line, so the row stays visually
 * consistent whatever icon it is given.
 */
export function FeatureCard({
  icon: Icon,
  title,
  description,
  tone = "brand",
}: {
  icon: LucideIcon;
  title: string;
  description: string;
  tone?: "brand" | "violet" | "emerald" | "amber";
}) {
  const tones = {
    brand: "bg-brand-50 text-brand-600",
    violet: "bg-violet-50 text-violet-600",
    emerald: "bg-emerald-50 text-emerald-600",
    amber: "bg-amber-50 text-amber-600",
  } as const;

  return (
    <div
      className={cn(
        "group rounded-2xl border border-ink-200/60 bg-white p-4",
        "shadow-[0_10px_30px_-22px_rgba(16,42,67,0.5)]",
        "transition-transform duration-200 hover:-translate-y-1",
      )}
    >
      <span
        className={cn(
          "inline-flex h-9 w-9 items-center justify-center rounded-xl",
          tones[tone],
        )}
      >
        <Icon className="h-4.5 w-4.5" aria-hidden />
      </span>
      <p className="mt-3 text-sm font-bold tracking-tight text-ink-900">{title}</p>
      <p className="mt-1 text-xs leading-relaxed text-ink-500">{description}</p>
    </div>
  );
}
