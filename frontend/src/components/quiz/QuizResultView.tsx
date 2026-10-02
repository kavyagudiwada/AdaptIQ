import {
  ArrowDown,
  ArrowRight,
  ArrowUp,
  CheckCircle2,
  Gauge,
  Lightbulb,
  RefreshCw,
  Target,
  TrendingUp,
  XCircle,
} from "lucide-react";
import { Badge } from "@/components/common/Badge";
import { Button } from "@/components/common/Button";
import { Card, CardBody, CardHeader } from "@/components/common/Card";
import { DifficultyBadge } from "@/components/assessment/DifficultyBadge";
import { DIFFICULTY_META } from "@/data/options";
import type { QuizResult } from "@/types";

const ORDER = { easy: 0, medium: 1, hard: 2 } as const;

export function QuizResultView({
  result,
  onNext,
  nextLoading,
}: {
  result: QuizResult;
  onNext: () => void;
  nextLoading: boolean;
}) {
  const moved =
    result.difficulty_changed &&
    ORDER[result.next_difficulty] !== ORDER[result.difficulty];
  const wentUp = ORDER[result.next_difficulty] > ORDER[result.difficulty];
  const from = DIFFICULTY_META[result.difficulty];
  const to = DIFFICULTY_META[result.next_difficulty];

  const gap = result.calibration_gap;
  const calibrated =
    gap === null || gap === undefined || Math.abs(gap) <= 5;
  const overconfident = gap !== null && gap !== undefined && gap > 5;
  const wrongCount = result.review.filter((r) => !r.was_correct).length;
  const discovered = result.misconceptions.length;

  return (
    <div className="space-y-5">
      {/* Adaptive decision */}
      <Card className="overflow-hidden">
        <div
          className={`flex flex-wrap items-center gap-5 border-b border-ink-100 px-6 py-6 ${
            wentUp
              ? "bg-gradient-to-br from-emerald-50 to-white"
              : "bg-gradient-to-br from-amber-50 to-white"
          }`}
        >
          <div className="flex h-24 w-24 shrink-0 flex-col items-center justify-center rounded-2xl bg-white shadow-sm ring-1 ring-ink-200">
            <p
              className={`text-2xl font-bold ${
                result.percentage >= 75
                  ? "text-emerald-600"
                  : result.percentage >= 50
                    ? "text-amber-600"
                    : "text-rose-600"
              }`}
            >
              {Math.round(result.percentage)}%
            </p>
            <p className="text-[10px] font-medium text-ink-500">
              {result.score}/{result.total_questions} correct
            </p>
          </div>

          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <DifficultyBadge difficulty={result.difficulty} />
              {moved ? (
                <span className="text-ink-400" aria-hidden>
                  <ArrowRight className="h-4 w-4" />
                </span>
              ) : null}
              <DifficultyBadge difficulty={result.next_difficulty} />
            </div>

            <p className="mt-2.5 text-lg font-bold text-ink-900">
              Next difficulty: {to.label}
              {moved ? (
                <span
                  className={`ml-2 inline-flex items-center gap-1 text-sm font-semibold ${
                    wentUp ? "text-emerald-600" : "text-amber-600"
                  }`}
                >
                  {wentUp ? (
                    <ArrowUp className="h-3.5 w-3.5" />
                  ) : (
                    <ArrowDown className="h-3.5 w-3.5" />
                  )}
                  {from.label} → {to.label}
                </span>
              ) : null}
            </p>
            <p className="mt-1.5 text-sm leading-relaxed text-ink-600">
              {result.system_message}
            </p>
          </div>
        </div>

        <div className="space-y-3 px-6 py-4">
          <p className="flex items-start gap-2 rounded-xl bg-ink-50 px-4 py-3 text-sm text-ink-700">
            <Target className="mt-0.5 h-4 w-4 shrink-0 text-brand-600" />
            {result.recommended_action}
          </p>

          {result.level_changed && result.current_level ? (
            <p className="flex items-start gap-2 rounded-xl bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
              <TrendingUp className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" />
              <span>
                Your measured level just changed to{" "}
                <span className="font-semibold capitalize">{result.current_level}</span>. Future
                practice sets, assessments and your plan now use this level.
              </span>
            </p>
          ) : null}

          {result.roadmap_stale ? (
            <p className="flex items-start gap-2 rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-800">
              <RefreshCw className="mt-0.5 h-4 w-4 shrink-0 text-amber-600" />
              <span>
                These results mean your roadmap is out of date. Head to the roadmap and choose{" "}
                <span className="font-semibold">Adapt my plan</span> to re-prioritise your topics.
              </span>
            </p>
          ) : null}
        </div>
      </Card>

      {/* Topic outcome */}
      <Card>
        <CardHeader title="Topic breakdown" description={`Practice set on ${result.topic}`} />
        <CardBody className="grid gap-5 sm:grid-cols-2">
          <div>
            <p className="mb-2 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-emerald-600">
              <CheckCircle2 className="h-3.5 w-3.5" />
              Strong
            </p>
            {result.strong_topics.length ? (
              <div className="flex flex-wrap gap-1.5">
                {result.strong_topics.map((t) => (
                  <Badge key={t} tone="success">
                    {t}
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="text-sm text-ink-500">Nothing scored ≥ 75% this time.</p>
            )}
          </div>
          <div>
            <p className="mb-2 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-rose-600">
              <XCircle className="h-3.5 w-3.5" />
              Needs work
            </p>
            {result.weak_topics.length ? (
              <div className="flex flex-wrap gap-1.5">
                {result.weak_topics.map((t) => (
                  <Badge key={t} tone="danger">
                    {t}
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="text-sm text-ink-500">No weak subtopics — push harder.</p>
            )}
          </div>
        </CardBody>
      </Card>

      {/* Confidence calibration */}
      {result.confidence_avg !== null && result.confidence_avg !== undefined ? (
        <Card>
          <CardHeader
            title="Confidence calibration"
            description="How sure you felt vs how well you actually did."
            action={
              <Badge tone={calibrated ? "success" : overconfident ? "danger" : "info"}>
                {calibrated
                  ? "Well calibrated"
                  : overconfident
                    ? "Overconfident"
                    : "Underconfident"}
              </Badge>
            }
          />
          <CardBody className="space-y-4">
            <div className="grid gap-3 sm:grid-cols-3">
              <div className="rounded-xl bg-ink-50 px-4 py-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">
                  Actual accuracy
                </p>
                <p className="mt-1 text-2xl font-bold text-ink-900">
                  {Math.round(result.percentage)}%
                </p>
              </div>
              <div className="rounded-xl bg-ink-50 px-4 py-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">
                  Your confidence
                </p>
                <p className="mt-1 text-2xl font-bold text-ink-900">
                  {Math.round(result.confidence_avg)}%
                </p>
              </div>
              <div className="rounded-xl bg-ink-50 px-4 py-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-ink-500">
                  Calibration gap
                </p>
                <p
                  className={`mt-1 text-2xl font-bold ${
                    calibrated
                      ? "text-emerald-600"
                      : overconfident
                        ? "text-rose-600"
                        : "text-sky-600"
                  }`}
                >
                  {gap! > 0 ? "+" : ""}
                  {Math.round(gap!)}
                  <span className="ml-1 text-sm font-medium text-ink-500">pts</span>
                </p>
              </div>
            </div>
            {result.calibration_feedback ? (
              <p className="flex items-start gap-2 rounded-xl bg-brand-50 px-4 py-3 text-sm leading-relaxed text-brand-800">
                <Gauge className="mt-0.5 h-4 w-4 shrink-0 text-brand-600" />
                {result.calibration_feedback}
              </p>
            ) : null}
          </CardBody>
        </Card>
      ) : null}

      {/* Question review + misconception clinic */}
      <Card>
        <CardHeader
          title={
            discovered > 0
              ? `Misconception clinic · ${discovered} diagnosed`
              : "Question review"
          }
          description={
            discovered > 0
              ? "Every wrong answer is traced to the specific misconception behind it, with a fix."
              : `How each answer matched up · ${wrongCount} to revisit`
          }
        />
        <CardBody className="space-y-3">
          {result.review.length === 0 ? (
            <p className="text-sm text-ink-500">No question review available.</p>
          ) : (
            result.review.map((item) => (
              <div
                key={item.question_id}
                className={`rounded-xl border px-4 py-3 ${
                  item.was_correct
                    ? "border-emerald-200 bg-emerald-50/40"
                    : "border-rose-200 bg-rose-50/40"
                }`}
              >
                <div className="flex items-start gap-2">
                  {item.was_correct ? (
                    <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" />
                  ) : (
                    <XCircle className="mt-0.5 h-4 w-4 shrink-0 text-rose-600" />
                  )}
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-ink-900">{item.question}</p>
                    <p className="mt-1 text-xs text-ink-500">
                      <span className="text-ink-400">{item.subtopic}</span>
                    </p>
                    <div className="mt-2 grid gap-1 text-xs sm:grid-cols-2">
                      <p className="text-ink-600">
                        <span className="font-semibold text-ink-900">You:</span>{" "}
                        {item.your_answer}
                      </p>
                      <p className="text-ink-600">
                        <span className="font-semibold text-ink-900">Correct:</span>{" "}
                        {item.correct_answer}
                      </p>
                    </div>
                    {!item.was_correct && item.misconception ? (
                      <div className="mt-2 space-y-1.5 rounded-lg bg-white px-3 py-2.5 ring-1 ring-rose-100">
                        <p className="flex items-start gap-1.5 text-xs font-semibold text-rose-700">
                          <Lightbulb className="mt-0.5 h-3.5 w-3.5 shrink-0" />
                          Misconception: {item.misconception}
                        </p>
                        {item.misconception_fix ? (
                          <p className="text-xs text-ink-600">
                            <span className="font-semibold text-ink-700">Fix:</span>{" "}
                            {item.misconception_fix}
                          </p>
                        ) : null}
                      </div>
                    ) : null}
                    {!item.was_correct && item.explanation ? (
                      <p className="mt-1.5 text-xs italic leading-relaxed text-ink-500">
                        {item.explanation}
                      </p>
                    ) : null}
                  </div>
                </div>
              </div>
            ))
          )}
        </CardBody>
      </Card>

      <div className="flex justify-end">
        <Button size="lg" loading={nextLoading} onClick={onNext} icon={<Target className="h-4 w-4" />}>
          Start {to.label} set
        </Button>
      </div>

      {/* keeps the threshold reference visible right under the decision */}
      <p className="text-right text-[11px] text-ink-400">
        Adaptive rule applied: score &lt; 50% → Easy · 50–74% → Medium · ≥ 75% → Hard
      </p>
    </div>
  );
}
