import { AlertTriangle, KeyRound, Lightbulb, ListChecks, Sparkles } from "lucide-react";
import { Badge } from "@/components/common/Badge";
import { Card, CardBody } from "@/components/common/Card";
import { DifficultyBadge } from "@/components/assessment/DifficultyBadge";
import { Markdown } from "@/utils/Markdown";
import type { TutorResponse } from "@/types";

export function TutorMessageCard({ response }: { response: TutorResponse }) {
  return (
    <div className="space-y-3">
      {/* Personalisation banner */}
      <div className="flex flex-wrap items-center gap-2 rounded-xl border border-brand-200 bg-brand-50/70 px-4 py-2.5">
        <Sparkles className="h-3.5 w-3.5 shrink-0 text-brand-600" />
        <p className="flex-1 text-xs text-brand-800">{response.personalized_note}</p>
      </div>

      <Card>
        <CardBody>
          <div className="mb-4 flex flex-wrap items-center justify-between gap-2 border-b border-ink-100 pb-3">
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="text-base font-bold text-ink-900">{response.topic}</h3>
              <DifficultyBadge difficulty={response.difficulty} />
            </div>
            <Badge tone="info">Personalised explanation</Badge>
          </div>

          <section>
            <h4 className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-ink-500">
              Explanation
            </h4>
            <Markdown text={response.explanation} className="text-[15px] text-ink-700" />
          </section>

          <section className="mt-5 rounded-xl border border-ink-200 bg-ink-50/70 p-4">
            <h4 className="mb-1.5 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-ink-500">
              <Lightbulb className="h-3.5 w-3.5 text-amber-500" />
              Example
            </h4>
            <Markdown text={response.example} className="text-sm text-ink-700" />
          </section>

          <div className="mt-5 grid gap-5 md:grid-cols-2">
            <section>
              <h4 className="mb-2 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-ink-500">
                <ListChecks className="h-3.5 w-3.5 text-emerald-600" />
                Key points
              </h4>
              <ul className="space-y-1.5">
                {response.key_points.map((point, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-ink-700">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-500" />
                    {point}
                  </li>
                ))}
              </ul>
            </section>

            <section>
              <h4 className="mb-2 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-ink-500">
                <AlertTriangle className="h-3.5 w-3.5 text-rose-600" />
                Common mistakes
              </h4>
              <ul className="space-y-1.5">
                {response.common_mistakes.map((mistake, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-ink-700">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-rose-500" />
                    {mistake}
                  </li>
                ))}
              </ul>
            </section>
          </div>

          <section className="mt-5 flex items-start gap-2.5 rounded-xl border border-dashed border-brand-300 bg-brand-50/50 px-4 py-3">
            <KeyRound className="mt-0.5 h-4 w-4 shrink-0 text-brand-600" />
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-brand-700">
                Follow-up question
              </p>
              <p className="mt-0.5 text-sm text-ink-800">{response.follow_up_question}</p>
            </div>
          </section>
        </CardBody>
      </Card>
    </div>
  );
}
