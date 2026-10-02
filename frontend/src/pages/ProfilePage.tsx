import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowRight, Save } from "lucide-react";
import { Button } from "@/components/common/Button";
import { Card, CardBody, CardHeader } from "@/components/common/Card";
import { FieldError, FieldHint, Input, Label, Select } from "@/components/common/Form";
import { PageHeader } from "@/components/common/PageHeader";
import { ErrorState } from "@/components/common/States";
import { GOAL_OPTIONS, LEVEL_OPTIONS, TOPIC_SUGGESTIONS } from "@/data/options";
import { useLearner } from "@/hooks/useLearner";
import { useAuth } from "@/hooks/useAuth";
import { saveProfile } from "@/services/learnerService";
import { toFriendlyError } from "@/services/api";
import type { LearningGoal, Level } from "@/types";
import { cn } from "@/utils/cn";

interface FormState {
  name: string;
  topic: string;
  current_level: Level;
  learning_goal: LearningGoal;
  hours_per_week: string;
  target_duration: string;
}

const INITIAL: FormState = {
  name: "",
  topic: "Machine Learning",
  current_level: "beginner",
  learning_goal: "placement",
  hours_per_week: "5",
  target_duration: "4",
};

export default function ProfilePage() {
  const navigate = useNavigate();
  const { setLearner, healthError } = useLearner();
  const { isAuthenticated, linkLearner, session } = useAuth();

  const [form, setForm] = useState<FormState>(INITIAL);
  const [errors, setErrors] = useState<Partial<Record<keyof FormState, string>>>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  function update<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
    setErrors((prev) => ({ ...prev, [key]: undefined }));
  }

  function validate(): boolean {
    const next: Partial<Record<keyof FormState, string>> = {};
    if (!form.name.trim()) next.name = "Please enter your name.";
    if (!form.topic.trim()) next.topic = "Please enter a topic to learn.";

    const hours = Number(form.hours_per_week);
    if (!Number.isFinite(hours) || hours <= 0 || hours > 80) {
      next.hours_per_week = "Enter hours between 1 and 80.";
    }

    const duration = Number(form.target_duration);
    if (!Number.isInteger(duration) || duration < 1 || duration > 52) {
      next.target_duration = "Enter a whole number of weeks between 1 and 52.";
    }

    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setSubmitError(null);
    if (!validate()) return;

    setSaving(true);
    try {
      const learner = await saveProfile({
        name: form.name.trim(),
        topic: form.topic.trim(),
        current_level: form.current_level,
        learning_goal: form.learning_goal,
        hours_per_week: Number(form.hours_per_week),
        target_duration: Number(form.target_duration),
      });
      setLearner(learner);

      // Link this profile to the signed-in account so the next sign-in on any
      // device restores the same progress. Best effort: the profile itself is
      // already saved even if the link fails.
      if (isAuthenticated && !session?.learner) {
        try {
          await linkLearner(learner.id);
        } catch {
          // Ignore: they can re-link from this page later.
        }
      }

      navigate("/assessment");
    } catch (error) {
      setSubmitError(toFriendlyError(error));
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="relative mx-auto w-full max-w-7xl">
      <div className="mx-auto w-full max-w-3xl">
        <PageHeader
          variant="light"
          eyebrow="Step 1 of 5"
        title="Create your learner profile"
        description="This is the context every AI module uses. The clearer this is, the better your roadmap, explanations and practice questions will be."
      />

      {healthError ? (
        <div className="mb-5">
          <ErrorState message={healthError} />
        </div>
      ) : null}

      <Card>
        <CardHeader
          title="About you"
          description="We use this to calibrate difficulty, pace and framing."
        />
        <CardBody>
          <form onSubmit={onSubmit} className="space-y-5" noValidate>
            <div className="grid gap-5 sm:grid-cols-2">
              <div>
                <Label htmlFor="name">Name</Label>
                <Input
                  id="name"
                  value={form.name}
                  onChange={(e) => update("name", e.target.value)}
                  placeholder="e.g. Kavya"
                  autoComplete="name"
                  aria-invalid={Boolean(errors.name)}
                />
                <FieldError>{errors.name}</FieldError>
              </div>

              <div>
                <Label htmlFor="hours">Hours per week</Label>
                <Input
                  id="hours"
                  type="number"
                  min={1}
                  max={80}
                  value={form.hours_per_week}
                  onChange={(e) => update("hours_per_week", e.target.value)}
                  aria-invalid={Boolean(errors.hours_per_week)}
                />
                <FieldError>{errors.hours_per_week}</FieldError>
                {!errors.hours_per_week ? (
                  <FieldHint>Used to size the weekly plan realistically.</FieldHint>
                ) : null}
              </div>
            </div>

            <div>
              <Label htmlFor="topic">Learning topic</Label>
              <Input
                id="topic"
                value={form.topic}
                onChange={(e) => update("topic", e.target.value)}
                placeholder="e.g. Machine Learning"
                aria-invalid={Boolean(errors.topic)}
              />
              <FieldError>{errors.topic}</FieldError>
              {!errors.topic ? (
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {TOPIC_SUGGESTIONS.map((suggestion) => (
                    <button
                      key={suggestion}
                      type="button"
                      onClick={() => update("topic", suggestion)}
                      className={cn(
                        "rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset transition",
                        form.topic === suggestion
                          ? "bg-brand-50 text-brand-700 ring-brand-600/25"
                          : "bg-white text-ink-600 ring-ink-200 hover:bg-ink-50",
                      )}
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              ) : null}
            </div>

            <div>
              <Label>Current level</Label>
              <div className="grid gap-2.5 sm:grid-cols-3">
                {LEVEL_OPTIONS.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => update("current_level", option.value)}
                    className={cn(
                      "rounded-xl border px-4 py-3 text-left transition",
                      form.current_level === option.value
                        ? "border-brand-500 bg-brand-50/70 ring-1 ring-brand-500"
                        : "border-ink-200 bg-white hover:border-ink-300 hover:bg-ink-50",
                    )}
                  >
                    <p className="text-sm font-semibold text-ink-900">{option.label}</p>
                    <p className="mt-0.5 text-xs leading-snug text-ink-500">
                      {option.blurb}
                    </p>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <Label htmlFor="goal">Learning goal</Label>
              <Select
                id="goal"
                value={form.learning_goal}
                onChange={(e) => update("learning_goal", e.target.value as LearningGoal)}
              >
                {GOAL_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </Select>
              <FieldHint>
                {GOAL_OPTIONS.find((g) => g.value === form.learning_goal)?.blurb}
              </FieldHint>
            </div>

            <div>
              <Label htmlFor="duration">Target duration (weeks)</Label>
              <Input
                id="duration"
                type="number"
                min={1}
                max={52}
                value={form.target_duration}
                onChange={(e) => update("target_duration", e.target.value)}
                aria-invalid={Boolean(errors.target_duration)}
              />
              <FieldError>{errors.target_duration}</FieldError>
              {!errors.target_duration ? (
                <FieldHint>
                  Your roadmap will contain exactly this many weeks.
                </FieldHint>
              ) : null}
            </div>

            {submitError ? (
              <div
                role="alert"
                className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700"
              >
                {submitError}
              </div>
            ) : null}

            <div className="flex flex-col gap-3 border-t border-ink-100 pt-5 sm:flex-row sm:items-center sm:justify-between">
              <p className="text-xs text-ink-400">
                Saving creates a new learner record and starts your progress tracking.
              </p>
              <Button
                type="submit"
                size="lg"
                loading={saving}
                icon={<Save className="h-4 w-4" />}
              >
                Save &amp; take assessment
              </Button>
            </div>
          </form>
        </CardBody>
      </Card>

      <div className="mt-4 flex items-center justify-center gap-2 text-xs text-ink-400">
          Next: AI knowledge analysis
          <ArrowRight className="h-3.5 w-3.5" />
        </div>
      </div>

      <aside
        className="pointer-events-none fixed bottom-6 z-0 hidden w-28 select-none lg:block xl:w-56 2xl:w-80"
        style={{ left: "calc(50% + (100vw + 48rem) / 4)", transform: "translateX(-50%)" }}
        aria-hidden="true"
      >
        <img
          src="/bg.png"
          alt=""
          draggable={false}
          className="h-auto w-full"
        />
      </aside>
    </div>
  );
}
