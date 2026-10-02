import { Link } from "react-router-dom";
import { Logo } from "@/components/common/Logo";
import { cn } from "@/utils/cn";

/**
 * Floating white navigation pill for the top of the hero.
 *
 * Only destinations that actually exist in the app are links. The remaining
 * labels are rendered as inert text with the same hover treatment, so the page
 * never shows a link that goes nowhere.
 */
export function AuthNav({ className }: { className?: string }) {
  const links = [
    { label: "Home", to: "/" },
    { label: "Courses" },
    { label: "About" },
    { label: "Pricing" },
    { label: "Resources" },
  ];

  const itemClass =
    "rounded-lg px-3 py-1.5 text-sm font-medium text-ink-600 transition-colors " +
    "hover:bg-ink-50 hover:text-ink-900";

  return (
    <nav
      aria-label="Primary"
      className={cn(
        "flex w-full items-center justify-between gap-3 rounded-2xl bg-white/90",
        "px-3 py-2.5 shadow-[0_10px_30px_-18px_rgba(16,42,67,0.45)] ring-1 ring-ink-200/60",
        "backdrop-blur sm:px-4",
        className,
      )}
    >
      <Logo to="/" />

      {/* Centre links collapse away on small screens, where the pill would
          otherwise wrap awkwardly. */}
      <ul className="hidden items-center gap-0.5 md:flex">
        {links.map(({ label, to }) =>
          to ? (
            <li key={label}>
              <Link to={to} className={itemClass}>
                {label}
              </Link>
            </li>
          ) : (
            <li key={label}>
              <span className={itemClass} aria-disabled="true">
                {label}
              </span>
            </li>
          ),
        )}
      </ul>

      <div className="flex shrink-0 items-center gap-2 sm:gap-3">
        <span className="hidden text-sm font-semibold text-ink-900 sm:inline">
          Login
        </span>
        <Link
          to="/signup"
          className={cn(
            "inline-flex h-9 items-center rounded-full bg-ink-900 px-4 text-sm",
            "font-semibold text-white transition-transform hover:scale-[1.03]",
            "active:scale-100 focus-visible:outline-none focus-visible:ring-2",
            "focus-visible:ring-brand-500 focus-visible:ring-offset-2",
          )}
        >
          Get Started
        </Link>
      </div>
    </nav>
  );
}
