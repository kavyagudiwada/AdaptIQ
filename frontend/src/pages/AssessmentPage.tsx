import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowRight, RefreshCw, Sparkles } from "lucide-react";
import { Button } from "@/components/common/Button";
import { Card, CardBody, CardHeader } from "@/components/common/Card";
import { PageHeader, StepGate } from "@/components/common/PageHeader";
import { ErrorState, LoadingState } from "@/components/common/States";
import { AssessmentResultView } from "@/components/assessment/AssessmentResultView";
import { DifficultyBadge } from "@/components/assessment/DifficultyBadge";
import { useLearner } from "@/hooks/useLearner";
import { generateAssessment, submitAssessment } from "@/services/assessmentService";
import { toFriendlyError } from "@/services/api";
import type { AssessmentPaper, AssessmentResult } from "@/types";
import { cn } from "@/utils/cn";

export default function AssessmentPage() {
  const navigate = useNavigate();
  const { learner } = useLearner();

  const [paper, setPaper] = useState<AssessmentPaper | null>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!learner) return;
    setLoading(true);
    setError(null);
    setAnswers({});
    setResult(null);
    try {
      setPaper(await generateAssessment(learner.id));
    } catch (err) {
      setError(toFriendlyError(err));
    } finally {
      setLoading(false);
    }
  }, [learner]);

  useEffect(() => {
    if (learner && !paper && !loading && !error) void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [learner?.id]);

  async function onSubmit() {
    if (!paper || !learner) return;
    setSubmitting(true);
    setError(null);
    try {
      const payload = Object.entries(answers).map(([question_id, selected_index]) => ({
        question_id,
        selected_index,
      }));
      setResult(await submitAssessment(learner.id, payload));
    } catch (err) {
      setError(toFriendlyError(err));
    } finally {
      setSubmitting(false);
    }
  }

  if (!learner) {
    return (
      <StepGate
        title="Create your learner profile first"
        description="The assessment is generated from your level and topic, so we need those before we can start."
        cta="Create profile"
        to="/profile"
      />
    );
  }

  const answered = Object.keys(answers).length;
  const total = paper?.questions.length ?? 0;

  return (
    <div className="mx-auto max-w-3xl">
      <PageHeader
        variant="light"
        eyebrow="Step 2 of 5"
        title="Initial assessment"
        description={`Five questions across ${learner.topic}, spread over different subtopics so we can see exactly where your gaps are.`}
        action={
          paper ? (
            <Button
              variant="secondary"
              size="sm"
              icon={<RefreshCw className="h-3.5 w-3.5" />}
              onClick={load}
              disabled={loading}
            >
              New set
            </Button>
          ) : null
        }
      />

      {error ? <ErrorState message={error} onRetry={load} /> : null}
      {loading ? <LoadingState label="Generating your assessment…" /> : null}

      {result ? (
        <>
          <AssessmentResultView result={result} />
          <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:justify-end">
            <Button variant="secondary" onClick={load} icon={<RefreshCw className="h-4 w-4" />}>
              Retake assessment
            </Button>
            <Button
              size="lg"
              onClick={() => navigate("/roadmap")}
              icon={<ArrowRight className="h-4 w-4" />}
            >
              Generate my roadmap
            </Button>
          </div>
        </>
      ) : paper && !loading ? (
        <Card>
          <CardHeader
            title="Answer all five questions"
            description="Don't overthink it — we want your honest current level."
          />
          <CardBody className="space-y-6">
            {paper.questions.map((question, index) => (
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
                    const selected = answers[question.id] === optionIndex;
                    return (
                      <label
                        key={optionIndex}
                        className={cn(
                          "flex cursor-pointer items-start gap-3 rounded-xl border px-3.5 py-2.5 text-sm transition",
                          selected
                            ? "border-brand-500 bg-brand-50/70 ring-1 ring-brand-500"
                            : "border-ink-200 bg-white hover:border-ink-300 hover:bg-ink-50",
                        )}
                      >
                        <input
                          type="radio"
                          name={question.id}
                          value={optionIndex}
                          checked={selected}
                          onChange={() =>
                            setAnswers((prev) => ({ ...prev, [question.id]: optionIndex }))
                          }
                          className="mt-0.5 h-4 w-4 accent-brand-600"
                        />
                        <span className={cn(selected ? "font-medium text-ink-900" : "text-ink-700")}>
                          {option}
                        </span>
                      </label>
                    );
                  })}
                </div>
              </fieldset>
            ))}

            <div className="flex flex-wrap items-center justify-between gap-3 border-t border-ink-100 pt-5">
              <p className="text-sm text-ink-500">
                {answered} of {total} answered
              </p>
              <Button
                size="lg"
                onClick={onSubmit}
                loading={submitting}
                disabled={answered < total}
                icon={<Sparkles className="h-4 w-4" />}
              >
                {answered < total ? `Answer all ${total} questions` : "Submit & analyse"}
              </Button>
            </div>
          </CardBody>
        </Card>
      ) : null}
    </div>
  );
}
