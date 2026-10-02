import { useEffect, useState } from "react";
import { cn } from "@/utils/cn";

export function ProgressBar({
  value,
  className,
  showLabel = false,
  barClassName,
}: {
  value: number;
  className?: string;
  showLabel?: boolean;
  barClassName?: string;
}) {
  const pct = Math.max(0, Math.min(100, value));
  return (
    <div className={cn("w-full", className)}>
      {showLabel ? (
        <div className="mb-1.5 flex items-center justify-between text-xs">
          <span className="text-ink-500">Progress</span>
          <span className="font-semibold text-ink-800">{Math.round(pct)}%</span>
        </div>
      ) : null}
      <div
        className="h-2 w-full overflow-hidden rounded-full bg-ink-100"
        role="progressbar"
        aria-valuenow={Math.round(pct)}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className={cn(
            "h-full rounded-full bg-brand-500 transition-[width] duration-700 ease-out",
            barClassName,
          )}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

const TONE_FILL: Record<BarTone, string> = {
  brand: "bg-brand-500",
  success: "bg-emerald-500",
  warning: "bg-amber-500",
  danger: "bg-rose-500",
};

const TONE_GRADIENT: Record<BarTone, string> = {
  brand: "bg-gradient-to-r from-brand-600 via-brand-500 to-cyan-400",
  success: "bg-gradient-to-r from-emerald-600 via-emerald-500 to-teal-300",
  warning: "bg-gradient-to-r from-amber-500 via-amber-400 to-yellow-300",
  danger: "bg-gradient-to-r from-rose-600 via-rose-500 to-orange-400",
};

const TONE_GLOW: Record<BarTone, string> = {
  brand: "shadow-[0_0_14px_rgba(51,102,255,0.55)]",
  success: "shadow-[0_0_14px_rgba(16,185,129,0.55)]",
  warning: "shadow-[0_0_14px_rgba(245,158,11,0.5)]",
  danger: "shadow-[0_0_14px_rgba(244,63,94,0.55)]",
};

const TONE_SEGMENT_GLOW: Record<BarTone, string> = {
  brand: "shadow-[0_0_8px_rgba(51,102,255,0.45)]",
  success: "shadow-[0_0_8px_rgba(16,185,129,0.45)]",
  warning: "shadow-[0_0_8px_rgba(245,158,11,0.4)]",
  danger: "shadow-[0_0_8px_rgba(244,63,94,0.45)]",
};

type BarTone = "brand" | "success" | "warning" | "danger";

/**
 * Animated score bar: grows to `value` on mount with a flowing sheen, a glossy
 * inner highlight and an optional leading-edge cap. Passing `ticks` overlays
 * evenly spaced separators so the bar can read "N of M" milestones (for
 * example one tick per roadmap week).
 */
export function AnimatedBar({
  value,
  tone = "brand",
  delay = 0,
  height = "h-3",
  trackClassName,
  className,
  ticks,
  cap = true,
  tickClassName = "border-white/25",
}: {
  value: number;
  tone?: BarTone;
  delay?: number;
  height?: string;
  trackClassName?: string;
  className?: string;
  /** Draw this many evenly spaced separators across the track. */
  ticks?: number;
  /** Render a glossy knob at the leading edge of the fill. */
  cap?: boolean;
  /** Border color of the tick separators (pale track needs a dark one). */
  tickClassName?: string;
}) {
  const pct = Math.max(0, Math.min(100, value));
  const [width, setWidth] = useState(0);
  useEffect(() => {
    let timer: number | undefined;
    const raf = requestAnimationFrame(() => {
      timer = window.setTimeout(() => setWidth(pct), delay);
    });
    return () => {
      cancelAnimationFrame(raf);
      if (timer) window.clearTimeout(timer);
    };
  }, [pct, delay]);

  const separators =
    typeof ticks === "number" && ticks > 1
      ? Array.from({ length: ticks }).map((_, i) => (
          <span
            key={i}
            className={cn(
              "h-full flex-1",
              i < ticks - 1 && `border-r ${tickClassName}`,
            )}
          />
        ))
      : null;

  return (
    <div
      className={cn(
        "relative w-full overflow-hidden rounded-full",
        height,
        trackClassName ?? "bg-white/15",
        className,
      )}
      role="progressbar"
      aria-valuenow={Math.round(pct)}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      {separators ? (
        <div className="pointer-events-none absolute inset-0 flex" aria-hidden>
          {separators}
        </div>
      ) : null}
      <div
        className={cn(
          "relative h-full overflow-hidden rounded-full transition-[width] duration-1000 ease-out",
          TONE_GRADIENT[tone],
          TONE_GLOW[tone],
        )}
        style={{ width: `${width}%` }}
      >
        <span
          aria-hidden
          className="pointer-events-none absolute inset-x-0 top-0 h-1/2 rounded-t-full bg-white/20"
        />
        <span
          aria-hidden
          className="pointer-events-none absolute inset-y-0 -left-1/3 w-1/3 animate-progress-sheen bg-gradient-to-r from-transparent via-white/50 to-transparent"
        />
        {cap && width > 2 ? (
          <span
            aria-hidden
            className="pointer-events-none absolute right-0 top-1/2 h-[190%] w-1.5 -translate-y-1/2 rounded-full bg-white/90 shadow-[0_0_8px_rgba(255,255,255,0.9)]"
          />
        ) : null}
      </div>
    </div>
  );
}

/** Ten-segment score bar that lights up left-to-right with a stagger. */
export function SegmentBar({
  value,
  tone = "brand",
  animate = true,
  index = 0,
}: {
  value: number;
  tone?: BarTone;
  animate?: boolean;
  index?: number;
}) {
  const pct = Math.max(0, Math.min(100, value));
  const filled = Math.round(pct / 10);
  const [shown, setShown] = useState(animate ? 0 : filled);
  useEffect(() => {
    if (!animate) return;
    let timer: number | undefined;
    const raf = requestAnimationFrame(() => {
      timer = window.setTimeout(() => setShown(filled), 120 + index * 90);
    });
    return () => {
      cancelAnimationFrame(raf);
      if (timer) window.clearTimeout(timer);
    };
  }, [animate, filled, index]);

  return (
    <div className="flex gap-0.5" aria-label={`${Math.round(pct)} percent`}>
      {Array.from({ length: 10 }).map((_, i) => (
        <span
          key={`${i}`}
          className={cn(
            "h-2.5 flex-1 rounded-[3px] transition-all duration-500 ease-out",
            i < shown
              ? cn(
                  TONE_FILL[tone],
                  TONE_SEGMENT_GLOW[tone],
                  "shadow-[inset_0_1px_1px_rgba(255,255,255,0.45)]",
                )
              : "bg-ink-200",
          )}
          style={{ transitionDelay: `${i * 60}ms` }}
        />
      ))}
    </div>
  );
}