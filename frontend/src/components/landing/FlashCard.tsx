import { useEffect, useState } from "react";
import type { LucideIcon } from "lucide-react";
import { cn } from "@/utils/cn";

type FlashCardProps = {
  icon: LucideIcon;
  title: string;
  kicker: string;
  body: string;
  accent: string;
  iconAccent: string;
};

/**
 * A single flip card.
 *
 * Front shows the capability name, back shows the detail. It flips on hover for
 * pointers and on click/tap for touch, so it is never a hover-only affordance.
 * The whole card is one real <button>, so it is reachable and operable from the
 * keyboard for free, and it reports its state with aria-pressed.
 */
export function FlashCard({
  icon: Icon,
  title,
  kicker,
  body,
  accent,
  iconAccent,
}: FlashCardProps) {
  const [flipped, setFlipped] = useState(false);
  const [canHover, setCanHover] = useState(false);

  // Only drive the flip on hover for devices that actually have a pointer,
  // otherwise a tap would leave the card stuck in a hover-flipped state.
  useEffect(() => {
    const mq = window.matchMedia("(hover: hover) and (pointer: fine)");
    const sync = () => setCanHover(mq.matches);
    sync();
    mq.addEventListener("change", sync);
    return () => mq.removeEventListener("change", sync);
  }, []);

  const showBack = flipped;

  return (
    <button
      type="button"
      aria-pressed={showBack}
      onClick={() => setFlipped((f) => !f)}
      onMouseEnter={() => canHover && setFlipped(true)}
      onMouseLeave={() => canHover && setFlipped(false)}
      className={cn(
        "group relative h-56 w-full text-left [perspective:1200px]",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500",
        "focus-visible:ring-offset-2 rounded-2xl",
      )}
    >
      <span
        className={cn(
          "relative block h-full w-full rounded-2xl transition-transform duration-500",
          "motion-reduce:transition-none [transform-style:preserve-3d]",
          showBack ? "rotate-y-180" : "",
        )}
      >
        {/* Front */}
        <span
          className={cn(
            "absolute inset-0 flex flex-col rounded-2xl border border-ink-100 bg-white p-6",
            "shadow-[0_18px_40px_-28px_rgba(16,42,67,0.5)] [backface-visibility:hidden]",
          )}
        >
          <span
            className={cn(
              "inline-flex h-11 w-11 items-center justify-center rounded-xl",
              iconAccent,
            )}
          >
            <Icon className="h-5 w-5" aria-hidden />
          </span>
          <span className="mt-4 text-lg font-bold text-ink-900">{title}</span>
          <span className="mt-1 text-xs font-semibold uppercase tracking-wide text-ink-400">
            {kicker}
          </span>
          <span className="mt-3 text-sm leading-relaxed text-ink-600">{body}</span>
          <span className="mt-auto pt-4 text-xs font-semibold text-brand-600">
            Tap to flip
          </span>
        </span>

        {/* Back */}
        <span
          className={cn(
            "absolute inset-0 flex flex-col justify-center rounded-2xl border p-6",
            "shadow-[0_18px_40px_-28px_rgba(16,42,67,0.5)]",
            "[backface-visibility:hidden] [transform:rotateY(180deg)]",
            accent,
          )}
        >
          <span className="text-xs font-semibold uppercase tracking-wide text-ink-500">
            {kicker}
          </span>
          <span className="mt-2 text-xl font-bold text-ink-900">{title}</span>
          <span className="mt-3 text-sm leading-relaxed text-ink-700">{body}</span>
        </span>
      </span>
    </button>
  );
}
