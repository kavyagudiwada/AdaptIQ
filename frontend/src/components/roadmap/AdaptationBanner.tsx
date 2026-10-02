import { ArrowUpRight, RefreshCw, TrendingUp } from "lucide-react";
import { Badge } from "@/components/common/Badge";
import { Button } from "@/components/common/Button";
import { Card, CardBody } from "@/components/common/Card";
import type { Adaptation } from "@/types";

const LEVEL_LABELS: Record<string, string> = {
  beginner: "Beginner",
  intermediate: "Intermediate",
  advanced: "Advanced",
};

const SOURCE_LABELS: Record<string, string> = {
  assessment: "from your assessment",
  practice: "from your quiz results",
  self_reported: "from what you told us",
};

function capitalise(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

/**
 * Surfaces the adaptation loop: shows the measured level, where it came from,
 * and offers to rebuild the plan when the learner's results have moved on.
 */
export function AdaptationBanner({
  adaptation,
  adapting,
  onAdapt,
}: {
  adaptation: Adaptation;
  adapting: boolean;
  onAdapt: () => void;
}) {
  const stale = adaptation.is_stale;
  const moved = adaptation.level_changed_from_start;
  const source = SOURCE_LABELS[adaptation.level_source] ?? "from your results";

  return (
    <Card
      className={stale ? "border-amber-300 bg-amber-50/60" : "border-emerald-200 bg-emerald-50/40"}
    >
      <CardBody className="space-y-4">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="min-w-0">
            <h2 className="flex items-center gap-2 text-base font-bold text-ink-900">
              <TrendingUp className="h-4 w-4 text-brand-600" />
              {stale ? "Your plan needs updating" : "How this plan was tailored"}
            </h2>
            <p className="mt-1 text-sm text-ink-600">
              {stale
                ? `Your results have moved since this plan was built, so it no longer matches where you are.`
                : `Built around ${LEVEL_LABELS[adaptation.effective_level].toLowerCase()}-level work ${source}.`}
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <Badge tone={moved ? "success" : "neutral"}>
              {LEVEL_LABELS[adaptation.effective_level]}
            </Badge>
            {moved ? (
              <Badge tone="info">
                You said {LEVEL_LABELS[adaptation.self_reported_level]}
              </Badge>
            ) : null}
            <Badge tone={stale ? "warning" : "success"}>
              Revision {adaptation.revision}
            </Badge>
          </div>
        </div>

        {adaptation.total_attempts > 0 ? (
          <p className="text-xs text-ink-500">
            Based on {adaptation.total_attempts} practice{" "}
            {adaptation.total_attempts === 1 ? "set" : "sets"} ·{" "}
            {adaptation.average_mastery}% average mastery
          </p>
        ) : null}

        {adaptation.reasons.length > 0 ? (
          <ul className="space-y-1.5">
            {adaptation.reasons.map((reason) => (
              <li key={reason} className="flex items-start gap-2.5 text-sm text-ink-700">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-brand-500" />
                {reason}
              </li>
            ))}
          </ul>
        ) : null}

        {stale ? (
          <Button
            variant="primary"
            size="md"
            onClick={onAdapt}
            loading={adapting}
            icon={<RefreshCw className="h-4 w-4" />}
          >
            Adapt my plan
          </Button>
        ) : (
          <p className="flex items-center gap-1.5 text-xs text-ink-500">
            <ArrowUpRight className="h-3.5 w-3.5" />
            This plan is up to date with your latest results
            {adaptation.weak_topics.length > 0
              ? `, with extra focus on ${adaptation.weak_topics.slice(0, 3).map(capitalise).join(", ")}`
              : ""}
            .
          </p>
        )}
      </CardBody>
    </Card>
  );
}
