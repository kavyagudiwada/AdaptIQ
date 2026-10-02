import { cn } from "@/utils/cn";

/**
 * Overlapping avatar placeholders for the social-proof line. Original
 * gradient discs with initials rather than stock photos, so nothing is
 * licensed and it still reads as "real people".
 */
export function AvatarCluster({ className }: { className?: string }) {
  const people = [
    { initials: "A", from: "#8b5cf6", to: "#6366f1" },
    { initials: "M", from: "#f59e0b", to: "#ef4444" },
    { initials: "S", from: "#10b981", to: "#0ea5e9" },
  ];

  return (
    <span className={cn("inline-flex items-center", className)}>
      {people.map(({ initials, from, to }, index) => (
        <span
          key={initials}
          aria-hidden
          className="-ml-2 inline-flex h-8 w-8 items-center justify-center rounded-full text-[11px] font-bold text-white ring-2 ring-white first:ml-0"
          style={{
            backgroundImage: `linear-gradient(135deg, ${from}, ${to})`,
            zIndex: people.length - index,
          }}
        >
          {initials}
        </span>
      ))}
    </span>
  );
}
