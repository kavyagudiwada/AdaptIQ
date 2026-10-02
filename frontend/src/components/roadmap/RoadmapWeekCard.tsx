import { useState } from "react";
import { Clock, Flame, Target, Wand2 } from "lucide-react";
import { Badge } from "@/components/common/Badge";
import { Card, CardBody, CardHeader } from "@/components/common/Card";
import { DifficultyBadge } from "@/components/assessment/DifficultyBadge";
import type { Roadmap, RoadmapWeek } from "@/types";
import { cn } from "@/utils/cn";

const WEEK_TONES = [
  "border-brand-200 bg-brand-50/40",
  "border-violet-200 bg-violet-50/40",
  "border-emerald-200 bg-emerald-50/40",
  "border-amber-200 bg-amber-50/40",
  "border-rose-200 bg-rose-50/40",
  "border-sky-200 bg-sky-50/40",
];

export function RoadmapWeekCard({
  week,
  index,
  onPractice,
}: {
  week: RoadmapWeek;
  index: number;
  onPractice?: (topic: string) => void;
}) {
  const [open, setOpen] = useState(index === 0);
  const tone = WEEK_TONES[index % WEEK_TONES.length];

  return (
    <Card className={cn("overflow-hidden border", tone)}>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center gap-4 px-5 py-4 text-left transition hover:bg-white/60"
      >
        <span
          className={cn(
            "flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-white text-lg font-bold text-ink-900 ring-1 ring-ink-200",
          )}
        >
          {week.week}
        </span>
        <div className="min-w-0 flex-1">
          <h3 className="text-base font-semibold text-ink-900">{week.title}</h3>
          <p className="mt-0.5 truncate text-sm text-ink-500">{week.focus}</p>
        </div>
        <div className="hidden shrink-0 items-center gap-1.5 sm:flex">
          <Badge tone="neutral">
            <Target className="h-3 w-3" />
            {week.practice_target} questions
          </Badge>
        </div>
        <span
          className={cn(
            "shrink-0 text-ink-400 transition-transform",
            open && "rotate-180",
          )}
          aria-hidden
        >
          ▾
        </span>
      </button>

      {open ? (
        <div className="border-t border-ink-200/70 bg-white/70 px-5 py-4">
          <ul className="space-y-3">
            {week.topics.map((topic) => (
              <li
                key={topic.name}
                className="rounded-xl border border-ink-200 bg-white px-4 py-3.5"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex flex-wrap items-center gap-2">
                    <p className="font-semibold text-ink-900">{topic.name}</p>
                    <DifficultyBadge difficulty={topic.difficulty} />
                  </div>
                  <span className="flex items-center gap-1 text-xs text-ink-500">
                    <Clock className="h-3 w-3" />
                    {topic.estimated_hours}h
                  </span>
                </div>
                <p className="mt-1.5 text-sm text-ink-600">{topic.why_this_matters}</p>
                {topic.resources.length ? (
                  <ul className="mt-2 flex flex-wrap gap-1.5">
                    {topic.resources.map((r) => (
                      <li
                        key={r}
                        className="rounded-md bg-ink-50 px-2 py-0.5 text-[11px] text-ink-600"
                      >
                        {r}
                      </li>
                    ))}
                  </ul>
                ) : null}
                {onPractice ? (
                  <button
                    type="button"
                    onClick={() => onPractice(topic.name)}
                    className="mt-2.5 text-xs font-semibold text-brand-600 transition hover:text-brand-700"
                  >
                    Practice this →
                  </button>
                ) : null}
              </li>
            ))}
          </ul>

          <div className="mt-4 flex items-start gap-2 rounded-xl border border-dashed border-ink-300 bg-white px-4 py-3">
            <Flame className="mt-0.5 h-4 w-4 shrink-0 text-amber-500" />
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">
                Week milestone
              </p>
              <p className="mt-0.5 text-sm text-ink-700">{week.milestone}</p>
            </div>
          </div>
        </div>
      ) : null}
    </Card>
  );
}

export function PersonalizationNotes({ roadmap }: { roadmap: Roadmap }) {
  return (
    <Card>
      <CardHeader
        title={
          <span className="flex items-center gap-2">
            <Wand2 className="h-4 w-4 text-brand-600" />
            Why this plan is personalised for you
          </span>
        }
        description="Generated from your assessment score, weak topics, goal and weekly hours."
      />
      <CardBody>
        <ul className="space-y-2.5">
          {roadmap.personalization_notes.map((note, i) => (
            <li key={i} className="flex items-start gap-2.5 text-sm text-ink-700">
              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-brand-500" />
              {note}
            </li>
          ))}
        </ul>

        {roadmap.focus_areas.length ? (
          <div className="mt-4 border-t border-ink-100 pt-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">
              Focus areas
            </p>
            <div className="mt-2 flex flex-wrap gap-1.5">
              {roadmap.focus_areas.map((area) => (
                <Badge key={area} tone="brand">
                  {area}
                </Badge>
              ))}
            </div>
          </div>
        ) : null}
      </CardBody>
    </Card>
  );
}
