import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowRight, CalendarDays, CheckCircle2, Wand2 } from "lucide-react";
import { Button } from "@/components/common/Button";
import { Card, CardBody } from "@/components/common/Card";
import { ProgressBar } from "@/components/common/ProgressBar";
import { PageHeader, StepGate } from "@/components/common/PageHeader";
import { EmptyState, ErrorState, LoadingState } from "@/components/common/States";
import { PersonalizationNotes, RoadmapWeekCard } from "@/components/roadmap/RoadmapWeekCard";
import { AdaptationBanner } from "@/components/roadmap/AdaptationBanner";
import { useLearner } from "@/hooks/useLearner";
import {
  completeWeek,
  generateRoadmap,
  getRoadmap,
} from "@/services/roadmapService";
import { toFriendlyError } from "@/services/api";
import type { Roadmap } from "@/types";

export default function RoadmapPage() {
  const navigate = useNavigate();
  const { learner } = useLearner();

  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [completing, setCompleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!learner) return;
    setLoading(true);
    setError(null);
    try {
      setRoadmap(await getRoadmap(learner.id));
    } catch (err) {
      // A missing roadmap is a normal first-run state, not an error.
      setRoadmap(null);
      setError(toFriendlyError(err));
    } finally {
      setLoading(false);
    }
  }, [learner]);

  useEffect(() => {
    void load();
  }, [load]);

  async function onGenerate(force = false) {
    if (!learner) return;
    setGenerating(true);
    setError(null);
    try {
      setRoadmap(await generateRoadmap(learner.id, force));
    } catch (err) {
      setError(toFriendlyError(err));
    } finally {
      setGenerating(false);
    }
  }

  async function onCompleteWeek() {
    if (!learner || !roadmap) return;
    setCompleting(true);
    setError(null);
    try {
      const result = await completeWeek(learner.id);
      setRoadmap({ ...roadmap, completed_weeks: result.completed_weeks });
    } catch (err) {
      setError(toFriendlyError(err));
    } finally {
      setCompleting(false);
    }
  }

  if (!learner) {
    return (
      <StepGate
        title="Create your learner profile first"
        description="Your roadmap is built from your profile and assessment results."
        cta="Create profile"
        to="/profile"
      />
    );
  }

  return (
    <div className="mx-auto max-w-4xl">
      <PageHeader
        variant="light"
        eyebrow="Step 3 of 5"
        title="Your personalised roadmap"
        description={`${roadmap?.duration ?? learner.target_duration} weeks, paced to ${learner.hours_per_week} hours per week, ordered around your weak topics.`}
        action={
          <Button
            variant={roadmap ? "secondary" : "primary"}
            size="md"
            onClick={() => onGenerate(true)}
            loading={generating}
            icon={<Wand2 className="h-4 w-4" />}
          >
            {roadmap ? "Rebuild from scratch" : "Generate roadmap"}
          </Button>
        }
      />

      {loading ? <LoadingState label="Loading your roadmap…" /> : null}
      {error ? <ErrorState message={error} onRetry={load} /> : null}

      {!loading && !roadmap && !error ? (
        <EmptyState
          title="No roadmap yet"
          description="Take the initial assessment first so we know which topics to prioritise, then generate your personalised plan."
          action={
            <div className="flex flex-col items-center gap-3">
              <Button
                onClick={() => void onGenerate(true)}
                loading={generating}
                icon={<Wand2 className="h-4 w-4" />}
              >
                Generate roadmap
              </Button>
              <button
                type="button"
                onClick={() => navigate("/assessment")}
                className="text-sm font-medium text-brand-700 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500"
              >
                or take the initial assessment first
              </button>
            </div>
          }
        />
      ) : null}

      {roadmap ? (
        <div className="space-y-5">
          <Card>
            <CardBody className="flex flex-wrap items-center justify-between gap-4">
              <div className="min-w-0">
                <h2 className="text-lg font-bold text-ink-900">{roadmap.title}</h2>
                <p className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-ink-500">
                  <span className="flex items-center gap-1.5">
                    <CalendarDays className="h-3.5 w-3.5" />
                    {roadmap.duration} weeks
                  </span>
                  <span>{learner.hours_per_week} hours per week</span>
                  <span>{roadmap.weeks.reduce((sum, w) => sum + w.topics.length, 0)} topics</span>
                </p>
              </div>
            </CardBody>
            <div className="border-t border-ink-100 px-5 py-4">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="min-w-0 flex-1">
                  <div className="mb-1.5 flex items-center justify-between text-sm">
                    <span className="font-medium text-ink-700">
                      {roadmap.completed_weeks} of {roadmap.duration} weeks complete
                    </span>
                    {roadmap.completed_weeks >= roadmap.duration ? (
                      <span className="flex items-center gap-1 font-semibold text-emerald-600">
                        <CheckCircle2 className="h-4 w-4" />
                        Plan finished
                      </span>
                    ) : null}
                  </div>
                  <ProgressBar
                    value={(roadmap.completed_weeks / roadmap.duration) * 100}
                    barClassName="bg-gradient-to-r from-brand-600 to-cyan-400"
                  />
                </div>
                <Button
                  variant="secondary"
                  size="sm"
                  loading={completing}
                  disabled={roadmap.completed_weeks >= roadmap.duration}
                  onClick={() => void onCompleteWeek()}
                  icon={<CheckCircle2 className="h-4 w-4" />}
                >
                  {roadmap.completed_weeks >= roadmap.duration
                    ? "All weeks complete"
                    : "Mark week complete"}
                </Button>
              </div>
            </div>
          </Card>

          {roadmap.adaptation ? (
            <AdaptationBanner
              adaptation={roadmap.adaptation}
              adapting={generating}
              onAdapt={() => onGenerate(false)}
            />
          ) : null}

          <PersonalizationNotes roadmap={roadmap} />

          <div className="space-y-3">
            {roadmap.weeks.map((week, index) => (
              <RoadmapWeekCard
                key={week.week}
                week={week}
                index={index}
                onPractice={(topic) => navigate(`/quiz?topic=${encodeURIComponent(topic)}`)}
              />
            ))}
          </div>

          <div className="flex justify-end pt-1">
            <Button
              size="lg"
              onClick={() => navigate("/tutor")}
              icon={<ArrowRight className="h-4 w-4" />}
            >
              Ask the AI Tutor
            </Button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
