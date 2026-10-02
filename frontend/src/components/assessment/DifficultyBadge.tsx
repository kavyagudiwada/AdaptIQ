import { DIFFICULTY_META } from "@/data/options";
import { Badge } from "@/components/common/Badge";
import { cn } from "@/utils/cn";

export function DifficultyBadge({ difficulty }: { difficulty: string }) {
  const meta = DIFFICULTY_META[difficulty] ?? DIFFICULTY_META.medium;
  return (
    <Badge className={meta.className}>
      <span className={cn("h-1.5 w-1.5 rounded-full", meta.dot)} />
      {meta.label}
    </Badge>
  );
}

/** Shows the adaptive thresholds so the logic is visible, not magic. */
export function AdaptiveLogicHint({ compact = false }: { compact?: boolean }) {
  if (compact) {
    return (
      <p className="text-xs text-ink-500">
        Adaptive rule: <span className="font-mono">score &lt; 50%</span> → Easy ·{" "}
        <span className="font-mono">50–74%</span> → Medium ·{" "}
        <span className="font-mono">≥ 75%</span> → Hard
      </p>
    );
  }

  return (
    <div className="rounded-xl border border-ink-200 bg-ink-50 px-4 py-3">
      <p className="text-xs font-semibold text-ink-700">How difficulty is chosen</p>
      <div className="mt-2 grid gap-2 sm:grid-cols-3">
        {[
          { range: "score < 50%", result: "Easy", tone: "text-emerald-700 bg-emerald-50" },
          { range: "50% – 74%", result: "Medium", tone: "text-amber-700 bg-amber-50" },
          { range: "score ≥ 75%", result: "Hard", tone: "text-rose-700 bg-rose-50" },
        ].map((rule) => (
          <div
            key={rule.range}
            className={cn("rounded-lg px-3 py-2 text-center", rule.tone)}
          >
            <p className="font-mono text-[11px] font-medium opacity-80">{rule.range}</p>
            <p className="text-sm font-bold">{rule.result}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
