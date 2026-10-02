import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowRight, GraduationCap, Send, Sparkles, Wand2 } from "lucide-react";
import { Button } from "@/components/common/Button";
import { Card, CardBody, CardHeader } from "@/components/common/Card";
import { PageHeader, StepGate } from "@/components/common/PageHeader";
import { ErrorState } from "@/components/common/States";
import { TutorMessageCard } from "@/components/tutor/TutorMessageCard";
import { TutorHistory } from "@/components/tutor/TutorHistoryCard";
import { useLearner } from "@/hooks/useLearner";
import { toFriendlyError } from "@/services/api";
import { getRoadmap } from "@/services/roadmapService";
import { askTutor } from "@/services/tutorService";
import type { TutorResponse } from "@/types";

const STARTER_QUESTIONS = [
  "Explain this in simple terms",
  "Why does this matter in practice?",
  "Walk me through a worked example",
  "What are the common mistakes here?",
];

interface Turn {
  key: string;
  question: string;
  response: TutorResponse;
}

export default function TutorPage() {
  const navigate = useNavigate();
  const { learner } = useLearner();

  const [topic, setTopic] = useState("");
  const [question, setQuestion] = useState("");
  const [turns, setTurns] = useState<Turn[]>([]);
  const [asking, setAsking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [topicOptions, setTopicOptions] = useState<string[]>([]);
  const threadEnd = useRef<HTMLDivElement | null>(null);

  // Topic suggestions come from the learner's own roadmap, so the tutor chat
  // starts inside their plan instead of a generic list.
  useEffect(() => {
    if (!learner) return;
    let cancelled = false;
    (async () => {
      try {
        const roadmap = await getRoadmap(learner.id);
        if (cancelled) return;
        const names = roadmap
          ? Array.from(
              new Set(roadmap.weeks.flatMap((week) => week.topics.map((t) => t.name))),
            )
          : [];
        setTopicOptions(names);
        if (names.length) setTopic(names[0]);
      } catch {
        if (!cancelled) setTopic(learner.topic);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [learner]);

  useEffect(() => {
    threadEnd.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [turns, asking]);

  const canAsk = useMemo(() => Boolean(learner) && topic.trim().length > 0, [learner, topic]);

  async function send(text: string) {
    const asked = text.trim();
    if (!learner || !asked || !canAsk) return;
    setAsking(true);
    setError(null);
    try {
      const response = await askTutor({
        learner_id: learner.id,
        topic: topic.trim(),
        question: asked,
      });
      setTurns((prev) => [
        ...prev,
        { key: `${Date.now()}`, question: asked, response },
      ]);
      setQuestion("");
    } catch (err) {
      setError(toFriendlyError(err));
    } finally {
      setAsking(false);
    }
  }

  if (!learner) {
    return (
      <StepGate
        title="Create your learner profile first"
        description="The tutor needs your level, goal and weak topics before it can personalise an explanation."
        cta="Create profile"
        to="/profile"
      />
    );
  }

  return (
    <div className="mx-auto max-w-3xl">
      <PageHeader
        variant="light"
        eyebrow="Step 4 of 5"
        title="AI tutor"
        description="Explanations are written for your level, framed around your goal, and weighted toward your weak topics."
        action={
          <Button
            variant="secondary"
            size="sm"
            onClick={() => navigate("/quiz")}
            icon={<ArrowRight className="h-3.5 w-3.5" />}
          >
            Skip to practice
          </Button>
        }
      />

      <Card>
        <CardHeader
          title="Ask about a topic"
          description="Pick a topic from your roadmap, then ask anything in your own words."
        />
        <CardBody>
          <label
            htmlFor="tutor-topic"
            className="mb-1.5 block text-sm font-medium text-ink-800"
          >
            Topic
          </label>
          {topicOptions.length ? (
            <select
              id="tutor-topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="h-11 w-full rounded-xl border border-ink-200 bg-white px-3.5 text-sm text-ink-900 shadow-sm transition focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
            >
              {topicOptions.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
          ) : (
            <input
              id="tutor-topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder={learner.topic}
              className="h-11 w-full rounded-xl border border-ink-200 bg-white px-3.5 text-sm text-ink-900 shadow-sm transition focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
            />
          )}

          <div className="mt-3 flex flex-wrap gap-1.5">
            {STARTER_QUESTIONS.map((starter) => (
              <button
                key={starter}
                type="button"
                onClick={() => setQuestion(starter)}
                className="rounded-full bg-ink-50 px-3 py-1.5 text-xs font-medium text-ink-600 ring-1 ring-inset ring-ink-200 transition hover:bg-ink-100"
              >
                {starter}
              </button>
            ))}
          </div>

          <form
            className="mt-4 flex flex-col gap-2 sm:flex-row"
            onSubmit={(e) => {
              e.preventDefault();
              void send(question);
            }}
          >
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder={`Ask a question about ${topic || "your topic"}…`}
              className="h-11 flex-1 rounded-xl border border-ink-200 bg-white px-3.5 text-sm text-ink-900 shadow-sm transition placeholder:text-ink-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
              aria-label="Your question"
            />
            <Button
              type="submit"
              size="lg"
              loading={asking}
              disabled={!canAsk || !question.trim()}
              icon={<Send className="h-4 w-4" />}
            >
              Ask
            </Button>
          </form>
        </CardBody>
      </Card>

      {error ? (
        <div className="mt-4">
          <ErrorState message={error} onRetry={() => void send(question)} />
        </div>
      ) : null}

      <div className="mt-5 space-y-5">
        {turns.map((turn) => (
          <div key={turn.key} className="space-y-2.5">
            <div className="flex items-start justify-end gap-2.5">
              <div className="max-w-[80%] rounded-2xl rounded-br-sm bg-brand-600 px-4 py-2.5 text-sm text-white shadow-sm">
                {turn.question}
              </div>
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-ink-900 text-white">
                {learner.name.charAt(0).toUpperCase()}
              </span>
            </div>
            <TutorMessageCard response={turn.response} />
          </div>
        ))}

        {asking ? (
          <div className="flex items-center gap-2.5 rounded-2xl border border-ink-200 bg-white px-4 py-3.5 shadow-sm">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-50 text-brand-600">
              <Sparkles className="h-4 w-4 animate-pulse" />
            </span>
            <p className="text-sm text-ink-500">
              Personalising an explanation for your level…
            </p>
          </div>
        ) : null}

        {!turns.length && !asking ? (
          <Card>
            <CardBody className="flex flex-col items-center gap-3 py-10 text-center">
              <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-50 text-brand-600">
                <GraduationCap className="h-6 w-6" />
              </span>
              <div>
                <p className="font-medium text-ink-900">
                  Your personalised tutor session starts here
                </p>
                <p className="mx-auto mt-1 max-w-md text-sm text-ink-500">
                  Pick a topic above. The tutor uses your assessment score, weak
                  topics, roadmap position and recent quiz results to shape the
                  answer.
                </p>
              </div>
            </CardBody>
          </Card>
        ) : null}

        <div ref={threadEnd} />
      </div>

      {turns.length ? (
        <div className="mt-6 flex flex-col items-center gap-2 rounded-2xl border border-dashed border-ink-300 bg-white px-6 py-6 text-center">
          <Wand2 className="h-5 w-5 text-brand-600" />
          <p className="text-sm font-medium text-ink-900">
            Ready to lock it in with practice questions?
          </p>
          <p className="mx-auto max-w-sm text-xs text-ink-500">
            The quiz difficulty adapts to your answers, so it will start at
            exactly the right level.
          </p>
          <Button
            className="mt-1"
            onClick={() => navigate("/quiz")}
            icon={<ArrowRight className="h-4 w-4" />}
          >
            Start adaptive quiz
          </Button>
        </div>
      ) : null}

      <div className="mt-6">
        <TutorHistory learnerId={learner.id} refreshKey={turns.length} />
      </div>
    </div>
  );
}
