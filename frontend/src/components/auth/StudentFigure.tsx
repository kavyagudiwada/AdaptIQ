import { cn } from "@/utils/cn";

/**
 * Original AdaptIQ mascot: a student with a backpack.
 *
 * Drawn as flat vector shapes with a single soft highlight per form so it reads
 * as a soft 3D cartoon without borrowing any licensed character art. Every
 * colour is passed in so the same figure can appear in different outfits.
 */
export function StudentFigure({
  className,
  skin = "#f0c8a4",
  hair = "#3a2a20",
  shirt = "#3366ff",
  trousers = "#1f2937",
  backpack = "#fbbf24",
  shoe = "#171a21",
  /** Raises one arm, as if pointing something out. */
  wave = false,
}: {
  className?: string;
  skin?: string;
  hair?: string;
  shirt?: string;
  trousers?: string;
  backpack?: string;
  shoe?: string;
  wave?: boolean;
}) {
  return (
    <svg
      viewBox="0 0 120 200"
      className={cn("h-full w-auto", className)}
      role="img"
      aria-label="Friendly student wearing a backpack"
    >
      {/* Soft ground shadow so the figure sits in the scene */}
      <ellipse cx="60" cy="188" rx="34" ry="6" fill="#0f172a" opacity="0.08" />

      {/* Backpack behind the body */}
      <rect x="34" y="78" width="52" height="58" rx="16" fill={backpack} />
      <rect x="34" y="78" width="52" height="20" rx="10" fill="#000000" opacity="0.08" />
      <rect x="46" y="112" width="28" height="16" rx="6" fill="#000000" opacity="0.1" />

      {/* Legs */}
      <rect x="45" y="132" width="13" height="46" rx="6.5" fill={trousers} />
      <rect x="62" y="132" width="13" height="46" rx="6.5" fill={trousers} />
      <rect x="45" y="132" width="13" height="10" rx="5" fill="#ffffff" opacity="0.08" />
      <rect x="62" y="132" width="13" height="10" rx="5" fill="#ffffff" opacity="0.08" />

      {/* Shoes */}
      <rect x="41" y="174" width="21" height="12" rx="6" fill={shoe} />
      <rect x="58" y="174" width="21" height="12" rx="6" fill={shoe} />

      {/* Torso */}
      <rect x="38" y="82" width="44" height="54" rx="18" fill={shirt} />
      <rect x="38" y="82" width="44" height="16" rx="8" fill="#ffffff" opacity="0.12" />
      {/* Collar */}
      <path d="M52 82h16l-8 9z" fill="#ffffff" opacity="0.35" />

      {/* Left arm (hanging) */}
      <rect x="28" y="88" width="12" height="44" rx="6" fill={shirt} />
      <circle cx="34" cy="136" r="7" fill={skin} />

      {/* Right arm (raised when waving) */}
      {wave ? (
        <>
          <rect
            x="80"
            y="52"
            width="12"
            height="44"
            rx="6"
            fill={shirt}
            transform="rotate(28 86 96)"
          />
          <circle cx="92" cy="54" r="7.5" fill={skin} />
        </>
      ) : (
        <>
          <rect x="80" y="88" width="12" height="44" rx="6" fill={shirt} />
          <circle cx="86" cy="136" r="7" fill={skin} />
        </>
      )}

      {/* Neck + head */}
      <rect x="53" y="70" width="14" height="16" rx="6" fill={skin} />
      <circle cx="60" cy="52" r="24" fill={skin} />
      {/* Hair */}
      <path
        d="M36 50a24 24 0 0 1 48 0c0-3-6-8-24-8s-24 5-24 8z"
        fill={hair}
      />
      <path d="M36 50c-2-14 8-24 24-24s26 10 24 24c-2-6-8-9-24-9s-22 3-24 9z" fill={hair} />

      {/* Face */}
      <circle cx="52" cy="53" r="2.6" fill="#171a21" />
      <circle cx="68" cy="53" r="2.6" fill="#171a21" />
      <path
        d="M54 61q6 5 12 0"
        stroke="#171a21"
        strokeWidth="2.2"
        strokeLinecap="round"
        fill="none"
      />
      <circle cx="44" cy="58" r="4" fill="#f472b6" opacity="0.28" />
      <circle cx="76" cy="58" r="4" fill="#f472b6" opacity="0.28" />
    </svg>
  );
}
