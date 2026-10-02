import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { ArrowRight, RefreshCw, Target, Wand2 } from "lucide-react";
import { Button } from "@/components/common/Button";
import { Card, CardBody, CardHeader } from "@/components/common/Card";
import { PageHeader, StepGate } from "@/components/common/PageHeader";
import { EmptyState, ErrorState, LoadingState } from "@/components/common/States";
import { AdaptiveLogicHint, DifficultyBadge } from "@/components/assessment/DifficultyBadge";
import { QuizResultView } from "@/components/quiz/QuizResultView";
import { useLearner } from "@/hooks/useLearner";
import { toFriendlyError } from "@/services/api";
import { generateQuiz, submitQuiz } from "@/services/quizService";
import { generateRoadmap, getRoadmap } from "@/services/roadmapService";
import type { Quiz, QuizAnswerInput, QuizResult } from "@/types";
import { cn } from "@/utils/cn";

export default function QuizPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const { learner } = useLearner();

  const [topic, setTopic] = useState<string>("");
  const [topicOptions, setTopicOptions] = useState<string[]>([]);
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [confidence, setConfidence] = useState<Record<string, number>>({});
  const [result, setResult] = useState<QuizResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [roadmapping, setRoadmapping] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const freshSeedRef = useRef(0);

  const requestedTopic = searchParams.get("topic");

  useEffect(() => {
    if (!learner) return;
    let cancelled = false;
    (async () => {
      try {
        const roadmap = await getRoadmap(learner.id);
        if (cancelled) return;
        const names = roadmap
          ? Array.from(
              new Set(roadmap.weeks.flatMap((w) => w.topics.map((t) => t.name))),
            )
          : [];
        setTopicOptions(names);
        setTopic((prev) => prev || requestedTopic || names[0] || learner.topic);
      } catch {
        if (!cancelled) setTopic((prev) => prev || requestedTopic || learner.topic);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [learner, requestedTopic]);

  const load = useCallback(
    async (targetTopic?: string, fresh = false) => {
      if (!learner) return;
      if (fresh) freshSeedRef.current += 1;
      setLoading(true);
      setError(null);
      setResult(null);
      setAnswers({});
      setConfidence({});
      try {
        setQuiz(
          await generateQuiz(
            learner.id,
            targetTopic ?? topic ?? undefined,
            fresh ? String(freshSeedRef.current) : undefined,
          ),
        );
      } catch (err) {
        setError(toFriendlyError(err));
      } finally {
        setLoading(false);
      }
    },
    [learner, topic],
  );

  const answered = Object.keys(answers).length;
  const total = quiz?.questions.length ?? 0;

  const progressPct = useMemo(
    () => (total ? Math.round((answered / total) * 100) : 0),
    [answered, total],
  );

  if (!learner) {
    return (
      <StepGate
        title="Create your learner profile first"
        description="The quiz picks its starting difficulty from your level and your latest scores, so we need a profile first."
        cta="Create profile"
        to="/profile"
      />
    );
  }

  async function onSubmit() {
    if (!quiz || !learner) return;
    setSubmitting(true);
    setError(null);
    try {
      const payload: QuizAnswerInput[] = Object.entries(answers).map(
        ([question_id, selected_index]) => ({
          question_id,
          selected_index,
          confidence: confidence[question_id],
        }),
      );
      setResult(
        await submitQuiz(
          learner.id,
          quiz.topic,
          quiz.difficulty,
          payload,
          quiz.questions,
          quiz.ai_mode,
        ),
      );
    } catch (err) {
      setError(toFriendlyError(err));
    } finally {
      setSubmitting(false);
    }
  }

  function onChangeTopic(next: string) {
    setTopic(next);
    setSearchParams({ topic: next });
  }

  async function onGenerateRoadmap() {
    if (!learner) return;
    setRoadmapping(true);
    setError(null);
    try {
      await generateRoadmap(learner.id);
      navigate("/roadmap");
    } catch (err) {
      setError(toFriendlyError(err));
    } finally {
      setRoadmapping(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl">
      <PageHeader
        variant="light"
        eyebrow="Step 5 of 5"
        title="Adaptive practice"
        description="We choose the starting difficulty from your level and history, then move it up or down based on what you score."
        action={
          quiz && !result ? (
            <Button
              variant="secondary"
              size="sm"
              onClick={() => void load(undefined, true)}
              disabled={loading || submitting}
              icon={<RefreshCw className="h-3.5 w-3.5" />}
            >
              New set
            </Button>
          ) : null
        }
      />

      <div className="mb-5 space-y-3">
        {topicOptions.length > 1 ? (
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="mr-1 text-xs font-semibold uppercase tracking-wide text-ink-500">
              Topic
            </span>
            {topicOptions.map((name) => (
              <button
                key={name}
                type="button"
                onClick={() => onChangeTopic(name)}
                disabled={loading || submitting}
                className={cn(
                  "rounded-full px-3 py-1.5 text-xs font-medium ring-1 ring-inset transition disabled:opacity-60",
                  topic === name
                    ? "bg-brand-50 text-brand-700 ring-brand-600/25"
                    : "bg-white text-ink-600 ring-ink-200 hover:bg-ink-50",
                )}
              >
                {name}
              </button>
            ))}
          </div>
        ) : null}
        <AdaptiveLogicHint />
      </div>

      {error ? <ErrorState message={error} onRetry={() => void load()} /> : null}
      {loading ? <LoadingState label="Picking questions for your level…" /> : null}

      {result ? (
        <QuizResultView
          result={result}
          nextLoading={loading}
          onNext={() => void load(undefined, true)}
          roadmapLoading={roadmapping}
          onGenerateRoadmap={() => void onGenerateRoadmap()}
        />
      ) : quiz && !loading ? (
        <Card>
          <CardHeader
            title={quiz.topic}
            description={quiz.adaptation_note}
            action={<DifficultyBadge difficulty={quiz.difficulty} />}
          />
          <CardBody className="space-y-6">
            {quiz.previous_percentage !== null ? (
              <p className="rounded-xl border border-ink-200 bg-ink-50 px-4 py-2.5 text-xs text-ink-600">
                Previous score on this topic:{" "}
                <span className="font-semibold text-ink-900">
                  {Math.round(quiz.previous_percentage)}%
                </span>{" "}
                → {quiz.adaptation_note}
              </p>
            ) : null}

            {quiz.questions.map((question, index) => {
              const selected = answers[question.id];
              return (
                <fieldset key={question.id} className="space-y-2.5">
                  <legend className="flex w-full items-start gap-2 text-sm font-medium text-ink-900">
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-brand-50 text-xs font-bold text-brand-700">
                      {index + 1}
                    </span>
                    <span className="flex-1">{question.question}</span>
                  </legend>
                  <div className="ml-8 flex flex-wrap items-center gap-2">
                    <DifficultyBadge difficulty={question.difficulty} />
                    <span className="text-xs text-ink-400">{question.subtopic}</span>
                  </div>
                  <div className="ml-8 space-y-2 pt-0.5">
                    {question.options.map((option, optionIndex) => {
                      const isSelected = selected === optionIndex;
                      return (
                        <label
                          key={optionIndex}
                          className={cn(
                            "flex cursor-pointer items-start gap-3 rounded-xl border px-3.5 py-2.5 text-sm transition",
                            isSelected
                              ? "border-brand-500 bg-brand-50/70 ring-1 ring-brand-500"
                              : "border-ink-200 bg-white hover:border-ink-300 hover:bg-ink-50",
                          )}
                        >
                          <input
                            type="radio"
                            name={question.id}
                            checked={isSelected}
                            onChange={() =>
                              setAnswers((prev) => ({
                                ...prev,
                                [question.id]: optionIndex,
                              }))
                            }
                            className="mt-0.5 h-4 w-4 accent-brand-600"
                          />
                          <span className={cn(isSelected ? "font-medium text-ink-900" : "text-ink-700")}>
                            {option}
                          </span>
                        </label>
                      );
                    })}
                  </div>
                  <div className="ml-8 pt-1">
                    <div className="flex items-center gap-2">
                      <span className="text-[11px] font-medium text-ink-400">
                        How sure are you?
                      </span>
                      <div className="flex items-center gap-1">
                        {[1, 2, 3, 4, 5].map((level) => (
                          <button
                            key={level}
                            type="button"
                            onClick={() =>
                              setConfidence((prev) => ({
                                ...prev,
                                [question.id]: level,
                              }))
                            }
                            aria-pressed={confidence[question.id] === level}
                            className={cn(
                              "flex h-7 w-7 items-center justify-center rounded-md text-xs font-bold ring-1 ring-inset transition disabled:opacity-60",
                              confidence[question.id] === level
                                ? "bg-brand-600 text-white ring-brand-600"
                                : "bg-white text-ink-500 ring-ink-200 hover:bg-brand-50",
                            )}
                          >
                            {level}
                          </button>
                        ))}
                      </div>
                      <span className="text-[11px] text-ink-400">
                        {confidence[question.id]
                          ? ["Guessing", "Unsure", "Fairly sure", "Confident", "Very sure"][
                              confidence[question.id] - 1
                            ]
                          : "optional · enables calibration"}
                      </span>
                    </div>
                  </div>
                </fieldset>
              );
            })}

            <div className="flex flex-wrap items-center justify-between gap-3 border-t border-ink-100 pt-5">
              <p className="text-sm text-ink-500">
                {answered} of {total} answered · {progressPct}% complete
                {Object.keys(confidence).length > 0 ? (
                  <span className="ml-2 inline-flex items-center gap-1 text-brand-600">
                    <Target className="h-3.5 w-3.5" />
                    {Object.keys(confidence).length} rated for calibration
                  </span>
                ) : null}
              </p>
              <Button
                size="lg"
                loading={submitting}
                disabled={answered < total}
                onClick={onSubmit}
                icon={<Target className="h-4 w-4" />}
              >
                {answered < total ? `Answer all ${total}` : "Submit & adapt"}
              </Button>
            </div>
          </CardBody>
        </Card>
      ) : !loading && !quiz && !error ? (
        <EmptyState
          title="Ready to practise?"
          description="Generate a set and we'll start you at the difficulty that matches your current level."
          action={
            <Button
              onClick={() => void load()}
              icon={<Wand2 className="h-4 w-4" />}
            >
              Generate quiz
            </Button>
          }
        />
      ) : null}

      <div className="mt-6 flex flex-col items-center gap-2 rounded-2xl border border-dashed border-ink-300 bg-white px-6 py-6 text-center">
        <p className="text-sm font-medium text-ink-900">
          Want to see how your mastery is trending?
        </p>
        <Button
          variant="secondary"
          onClick={() => navigate("/progress")}
          icon={<ArrowRight className="h-4 w-4" />}
        >
          View progress
        </Button>
      </div>
    </div>
  );
}
