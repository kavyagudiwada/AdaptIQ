import { CheckCircle2, TrendingUp, XCircle } from "lucide-react";
import { Badge } from "@/components/common/Badge";
import { Card, CardBody, CardHeader } from "@/components/common/Card";
import { ProgressBar } from "@/components/common/ProgressBar";
import { LEVEL_META } from "@/data/options";
import type { AssessmentResult } from "@/types";
import { cn } from "@/utils/cn";

function topicTone(pct: number) {
  if (pct >= 75) return { bar: "bg-emerald-500", text: "text-emerald-700", ring: "ring-emerald-600/20", bg: "bg-emerald-50" };
  if (pct >= 50) return { bar: "bg-amber-500", text: "text-amber-700", ring: "ring-amber-600/20", bg: "bg-amber-50" };
  return { bar: "bg-rose-500", text: "text-rose-700", ring: "ring-rose-600/20", bg: "bg-rose-50" };
}

export function AssessmentResultView({ result }: { result: AssessmentResult }) {
  const level = LEVEL_META[result.estimated_level] ?? LEVEL_META.beginner;

  return (
    <div className="space-y-5">
      {/* Score hero */}
      <Card className="overflow-hidden">
        <div className="flex flex-wrap items-center gap-6 border-b border-ink-100 bg-gradient-to-br from-brand-50 to-white px-6 py-6">
          <div className="relative flex h-28 w-28 shrink-0 items-center justify-center">
            <svg className="h-28 w-28 -rotate-90" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="42" fill="none" stroke="#eceef2" strokeWidth="10" />
              <circle
                cx="50"
                cy="50"
                r="42"
                fill="none"
                stroke="#3366ff"
                strokeWidth="10"
                strokeLinecap="round"
                strokeDasharray={`${(result.percentage / 100) * 264} 264`}
                className="transition-[stroke-dasharray] duration-1000"
              />
            </svg>
            <div className="absolute text-center">
              <p className="text-2xl font-bold text-ink-900">{Math.round(result.percentage)}%</p>
              <p className="text-[10px] font-medium text-ink-500">
                {result.score}/{result.total_questions} correct
              </p>
            </div>
          </div>

          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <Badge className={level.className}>{level.label}</Badge>
            </div>
            <h2 className="mt-2 text-xl font-bold text-ink-900">Knowledge analysis</h2>
            <p className="mt-1.5 text-sm leading-relaxed text-ink-600">{result.feedback}</p>
            <p className="mt-2.5 flex items-center gap-1.5 text-sm text-brand-700">
              <TrendingUp className="h-3.5 w-3.5 shrink-0 text-brand-600" />
              We have set your working level to{" "}
              <span className="font-semibold">{level.label}</span> from this result. Your
              practice sets, tutor and roadmap now use it.
            </p>
          </div>
        </div>

        <div className="grid divide-y divide-ink-100 sm:grid-cols-2 sm:divide-x sm:divide-y-0">
          <div className="px-6 py-5">
            <p className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-emerald-600">
              <CheckCircle2 className="h-3.5 w-3.5" />
              Strong topics
            </p>
            {result.strong_topics.length ? (
              <div className="mt-2.5 flex flex-wrap gap-1.5">
                {result.strong_topics.map((t) => (
                  <Badge key={t} tone="success">
                    {t}
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="mt-2 text-sm text-ink-500">None yet — keep practising.</p>
            )}
          </div>
          <div className="px-6 py-5">
            <p className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-rose-600">
              <XCircle className="h-3.5 w-3.5" />
              Weak topics
            </p>
            {result.weak_topics.length ? (
              <div className="mt-2.5 flex flex-wrap gap-1.5">
                {result.weak_topics.map((t) => (
                  <Badge key={t} tone="danger">
                    {t}
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="mt-2 text-sm text-ink-500">
                Nothing missed — we will push you harder.
              </p>
            )}
          </div>
        </div>
      </Card>

      {/* Per-subtopic breakdown */}
      <Card>
        <CardHeader
          title="Topic-by-topic breakdown"
          description="Each topic feeds the roadmap generator and the tutor."
        />
        <CardBody className="space-y-3.5">
          {result.topic_breakdown.map((row) => {
            const tone = topicTone(row.percentage);
            return (
              <div key={row.subtopic}>
                <div className="mb-1.5 flex items-center justify-between text-sm">
                  <span className="font-medium text-ink-800">{row.subtopic}</span>
                  <span className={cn("font-semibold", tone.text)}>
                    {row.correct}/{row.total} · {Math.round(row.percentage)}%
                  </span>
                </div>
                <ProgressBar value={row.percentage} barClassName={tone.bar} />
              </div>
            );
          })}
        </CardBody>
      </Card>
    </div>
  );
}
