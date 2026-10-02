import { Link } from "react-router-dom";
import { cn } from "@/utils/cn";

/**
 * The single AdaptIQ brand mark. Pass `to` to render it as a link, otherwise it
 * renders as a plain lockup.
 *
 * The mark artwork is a wide (1.43:1) transparent PNG trimmed from
 * `public/adaptiq-mark.png`, so it is sized by height and allowed to keep its
 * own width. The wordmark stays as real text next to it, which keeps it crisp
 * and selectable rather than shrinking baked-in lettering into the header.
 */
export function Logo({
  to,
  className,
  iconClassName,
  light,
}: {
  to?: string;
  className?: string;
  iconClassName?: string;
  light?: boolean;
}) {
  const mark = (
    <>
      <img
        src="/adaptiq-mark.png"
        alt=""
        width={51}
        height={36}
        decoding="async"
        className={cn(
          "block h-9 w-auto shrink-0 object-contain",
          iconClassName,
        )}
      />
      <span
        className={cn(
          "text-lg font-bold tracking-tight",
          light ? "text-white" : "text-ink-900",
        )}
      >
        Adapt
        <span className={light ? "text-cyan-400" : "text-brand-600"}>IQ</span>
      </span>
    </>
  );

  const classes = cn("flex items-center gap-2.5", className);

  if (to) {
    return (
      <Link to={to} className={cn(classes, "transition-opacity hover:opacity-90")}>
        {mark}
      </Link>
    );
  }

  return <span className={classes}>{mark}</span>;
}
