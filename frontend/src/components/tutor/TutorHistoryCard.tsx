import { useEffect, useState } from "react";
import { ChevronDown, History } from "lucide-react";
import { Badge } from "@/components/common/Badge";
import { Card, CardBody, CardHeader } from "@/components/common/Card";
import { getTutorHistory } from "@/services/tutorService";
import { toFriendlyError } from "@/services/api";
import type { TutorHistoryItem } from "@/types";
import { cn } from "@/utils/cn";

function dateLabel(iso: string) {
  const d = new Date(iso);
  return isNaN(d.getTime())
    ? ""
    : d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

function difficultyTone(diff: string) {
  if (diff === "easy") return "success" as const;
  if (diff === "hard") return "danger" as const;
  return "warning" as const;
}

export function TutorHistory({
  learnerId,
  refreshKey,
}: {
  learnerId: number;
  refreshKey: number;
}) {
  const [sessions, setSessions] = useState<TutorHistoryItem[]>([]);
  const [open, setOpen] = useState<number | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoaded(false);
    setError(null);
    (async () => {
      try {
        const items = await getTutorHistory(learnerId);
        if (!cancelled) setSessions(items);
      } catch (err) {
        if (!cancelled) setError(toFriendlyError(err));
      } finally {
        if (!cancelled) setLoaded(true);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [learnerId, refreshKey]);

  return (
    <Card>
      <CardHeader
        title={`Past explanations (${sessions.length})`}
        description="Every answer is saved here so you can revisit what the tutor taught you."
      />
      <CardBody>
        {!loaded ? (
          <div className="space-y-2">
            <div className="h-10 animate-pulse rounded-xl bg-ink-100" />
            <div className="h-10 animate-pulse rounded-xl bg-ink-100" />
          </div>
        ) : error ? (
          <p className="text-sm text-ink-500">{error}</p>
        ) : sessions.length === 0 ? (
          <div className="flex flex-col items-center gap-2 py-6 text-center">
            <History className="h-6 w-6 text-ink-300" />
            <p className="text-sm text-ink-500">
              No explanations saved yet. Ask the tutor a question and it will
              appear here.
            </p>
          </div>
        ) : (
          <ul className="divide-y divide-ink-100">
            {sessions.map((item) => {
              const expanded = open === item.id;
              return (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => setOpen(expanded ? null : item.id)}
                    className="flex w-full items-center justify-between gap-3 py-3 text-left"
                  >
                    <span className="flex min-w-0 flex-wrap items-center gap-x-2.5 gap-y-1">
                      <span className="font-medium text-ink-900">{item.subtopic}</span>
                      <Badge tone={difficultyTone(item.difficulty)}>
                        {item.difficulty}
                      </Badge>
                      {item.ai_mode === "live" ? (
                        <Badge tone="info">AI</Badge>
                      ) : null}
                      <span className="text-xs text-ink-400">{dateLabel(item.created_at)}</span>
                    </span>
                    <ChevronDown
                      className={cn(
                        "h-4 w-4 shrink-0 text-ink-400 transition-transform",
                        expanded && "rotate-180",
                      )}
                    />
                  </button>
                  {expanded ? (
                    <div className="pb-4">
                      <p className="whitespace-pre-wrap rounded-xl bg-ink-50 px-4 py-3 text-sm leading-relaxed text-ink-700">
                        {item.explanation}
                      </p>
                      {item.key_points.length ? (
                        <ul className="mt-2 space-y-1">
                          {item.key_points.map((point, i) => (
                            <li key={`${item.id}-kp-${i}`} className="flex items-start gap-2 text-sm text-ink-600">
                              <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-brand-500" />
                              {point}
                            </li>
                          ))}
                        </ul>
                      ) : null}
                    </div>
                  ) : null}
                </li>
              );
            })}
          </ul>
        )}
      </CardBody>
    </Card>
  );
}