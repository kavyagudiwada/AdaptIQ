import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceLine,
} from "recharts";
import {
  Award,
  BarChart3,
  BookOpen,
  CalendarCheck,
  ClipboardCheck,
  Flame,
  MessageSquareText,
  Sparkles,
  Target,
  User,
} from "lucide-react";
import { Badge } from "@/components/common/Badge";
import { Card, CardBody, CardHeader } from "@/components/common/Card";
import { PageHeader, StepGate } from "@/components/common/PageHeader";
import { ErrorState, LoadingState } from "@/components/common/States";
import { SegmentBar, AnimatedBar } from "@/components/common/ProgressBar";
import { LEVEL_META } from "@/data/options";
import { useAsync } from "@/hooks/useAsync";
import { useCountUp } from "@/hooks/useCountUp";
import { useLearner } from "@/hooks/useLearner";
import { getProgress } from "@/services/progressService";
import type { ActivityItem, QuizHistoryPoint, TopicProgress } from "@/types";
import { cn } from "@/utils/cn";

const ACTIVITY_ICONS = {
  profile: User,
  assessment: ClipboardCheck,
  roadmap: BookOpen,
  tutor: MessageSquareText,
  quiz: Target,
} as const;

function toneFor(pct: number) {
  if (pct >= 75) return "success" as const;
  if (pct >= 50) return "warning" as const;
  return "danger" as const;
}

function StatCard({
  icon: Icon,
  label,
  value,
  hint,
  tone,
}: {
  icon: typeof Award;
  label: string;
  value: string | number;
  hint?: string;
  tone: string;
}) {
  return (
    <Card className="group p-4 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_10px_24px_-10px_rgba(16,24,40,0.25)]">
      <div className="flex items-start gap-3">
        <span
          className={cn(
            "flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ring-1 ring-inset ring-white/50 transition-transform duration-200 group-hover:scale-110",
            tone,
          )}
        >
          <Icon className="h-5 w-5" />
        </span>
        <div className="min-w-0">
          <p className="text-xs font-medium uppercase tracking-wide text-ink-500">{label}</p>
          <p className="mt-0.5 text-2xl font-bold leading-tight text-ink-900">{value}</p>
          {hint ? <p className="mt-0.5 truncate text-xs text-ink-500">{hint}</p> : null}
        </div>
      </div>
    </Card>
  );
}

function QuizHistoryChart({
  points,
}: {
  points: QuizHistoryPoint[];
}) {
  if (points.length === 0) {
    return (
      <div className="flex h-52 flex-col items-center justify-center gap-2 text-center">
        <BarChart3 className="h-7 w-7 text-ink-300" />
        <p className="text-sm text-ink-500">
          No quiz attempts yet. Your score trend will appear here after your first set.
        </p>
      </div>
    );
  }

  const data = points.map((p) => ({
    attempt_id: p.attempt_id,
    percentage: p.percentage,
    confidence_avg: p.confidence_avg ?? null,
  }));

  const hasConfidence = points.some((p) => p.confidence_avg != null);

  return (
    <div>
      <div className="mb-1.5 flex items-center gap-4 text-xs text-ink-500">
        <span className="flex items-center gap-1.5">
          <span className="h-1.5 w-4 rounded-full bg-[#3366ff]" />
          Actual score
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-1.5 w-4 rounded-full bg-[#8b5cf6]" />
          Self-rated confidence
        </span>
      </div>
      <div className="h-48 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#eceef2" vertical={false} />
            <XAxis
              dataKey="attempt_id"
              tickLine={false}
              axisLine={false}
              tick={{ fontSize: 11, fill: "#7b8496" }}
            />
            <YAxis
              domain={[0, 100]}
              ticks={[0, 25, 50, 75, 100]}
              tickLine={false}
              axisLine={false}
              tick={{ fontSize: 11, fill: "#7b8496" }}
            />
            <Tooltip
              contentStyle={{
                borderRadius: 12,
                border: "1px solid #e4e7ec",
                fontSize: 12,
                boxShadow: "0 8px 20px rgba(16,24,40,0.08)",
              }}
              formatter={(value, name) => [
                `${value}%`,
                name === "confidence_avg" ? "confidence" : "score",
              ]}
            />
            <ReferenceLine
              y={75}
              stroke="#10b981"
              strokeDasharray="4 4"
              label={{ value: "hard", position: "right", fontSize: 10, fill: "#10b981" }}
            />
            <ReferenceLine
              y={50}
              stroke="#f59e0b"
              strokeDasharray="4 4"
              label={{ value: "medium", position: "right", fontSize: 10, fill: "#f59e0b" }}
            />
            <Line
              type="monotone"
              dataKey="percentage"
              stroke="#3366ff"
              strokeWidth={2.5}
              dot={{ r: 3.5, strokeWidth: 2, fill: "#fff", stroke: "#3366ff" }}
              activeDot={{ r: 5 }}
            />
            {hasConfidence ? (
              <Line
                type="monotone"
                dataKey="confidence_avg"
                stroke="#8b5cf6"
                strokeWidth={2}
                strokeDasharray="5 4"
                dot={{ r: 3, strokeWidth: 1.5, fill: "#fff", stroke: "#8b5cf6" }}
                activeDot={{ r: 4 }}
              />
            ) : null}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function TopicRow({ row, index = 0 }: { row: TopicProgress; index?: number }) {
  const level = LEVEL_META[row.mastery_level] ?? LEVEL_META.beginner;
  return (
    <div className="rounded-xl border border-ink-200 bg-white px-4 py-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-medium text-ink-900">{row.topic}</span>
          <Badge className={level.className}>{level.label}</Badge>
        </div>
        <span
          className={cn(
            "text-sm font-semibold",
            row.progress_percentage >= 75
              ? "text-emerald-600"
              : row.progress_percentage >= 50
                ? "text-amber-600"
                : "text-rose-600",
          )}
        >
          {Math.round(row.progress_percentage)}%
        </span>
      </div>
      <div className="mt-2">
        <SegmentBar value={row.progress_percentage} tone={toneFor(row.progress_percentage)} index={index} />
      </div>
    </div>
  );
}

function ActivityRow({ item }: { item: ActivityItem }) {
  const Icon = ACTIVITY_ICONS[item.kind] ?? BookOpen;
  return (
    <li className="flex items-start gap-3">
      <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-ink-50 text-ink-500">
        <Icon className="h-4 w-4" />
      </span>
      <div className="min-w-0">
        <p className="text-sm font-medium text-ink-800">{item.label}</p>
        <p className="truncate text-xs text-ink-500">{item.detail}</p>
      </div>
    </li>
  );
}

export default function DashboardPage() {
  const { learner } = useLearner();
  const { data, loading, error, reload } = useAsync(
    () => (learner ? getProgress(learner.id) : Promise.reject(new Error("No learner"))),
    [learner?.id],
  );
  const overallCount = useCountUp(data?.overall_progress ?? 0, 1100, 150);

  if (!learner) {
    return (
      <StepGate
        title="Create your learner profile first"
        description="Your progress dashboard fills up as you take the assessment, generate a roadmap, use the tutor and practise."
        cta="Create profile"
        to="/profile"
      />
    );
  }

  if (loading) return <LoadingState label="Loading your progress…" />;
  if (error) return <ErrorState message={error} onRetry={reload} />;
  if (!data) return null;

  const level = LEVEL_META[data.estimated_level] ?? LEVEL_META.beginner;

  return (
    <div className="space-y-5">
      <PageHeader
        variant="light"
        eyebrow="Your progress"
        title={`Welcome back, ${data.learner_name}`}
        description={`Here is where you stand on ${data.topic} and what we recommend you tackle next.`}
      />

      {/* Overall score hero */}
      <Card className="relative overflow-hidden border-white/10 bg-gradient-to-br from-[#0c1526] via-[#111c33] to-[#0a1020] shadow-[0_10px_40px_rgba(10,16,32,0.6)]">
        <div className="pointer-events-none absolute -right-16 -top-16 h-64 w-64 rounded-full bg-brand-600/20 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-20 -left-10 h-56 w-56 rounded-full bg-cyan-500/10 blur-3xl" />
        <CardBody className="relative">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-cyan-300">
                Overall score
              </p>
              <p className="mt-1 text-5xl font-bold tracking-tight text-white">
                {Math.round(overallCount)}
                <span className="text-2xl text-white/60">%</span>
              </p>
              <p className="mt-1 text-sm text-white/50">{data.topics.length} topics tracked</p>
            </div>
            <div className="hidden w-48 sm:block">
              <p className="mb-1.5 text-xs font-medium text-white/60">Mastery level</p>
              <Badge className={cn("rounded-lg px-3 py-1 text-sm", level.className)}>
                {level.label}
              </Badge>
            </div>
          </div>
          <div className="mt-5">
            <AnimatedBar value={data.overall_progress} tone="brand" height="h-3.5" ticks={10} />
          </div>
        </CardBody>
      </Card>

      {/* Stats */}
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <StatCard
          icon={ClipboardCheck}
          label="Assessment score"
          value={
            data.assessment_percentage !== null
              ? `${Math.round(data.assessment_percentage)}%`
              : "Not taken"
          }
          hint={level.label}
          tone="bg-violet-50 text-violet-600"
        />
        <StatCard
          icon={Target}
          label="Quizzes taken"
          value={data.total_quizzes}
          hint={`${data.learning_streak}-day streak`}
          tone="bg-emerald-50 text-emerald-600"
        />
        <StatCard
          icon={Flame}
          label="Current focus"
          value={data.current_topic}
          hint={`Next: ${data.recommended_next_topic}`}
          tone="bg-amber-50 text-amber-600"
        />
      </div>

      {/* Recommendation */}
      <Card className="overflow-hidden border-brand-200 bg-gradient-to-br from-brand-50/70 to-white">
        <CardBody className="flex flex-wrap items-start gap-4">
          <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-brand-600 text-white shadow-sm">
            <Sparkles className="h-5 w-5" />
          </span>
          <div className="min-w-0 flex-1">
            <p className="text-xs font-semibold uppercase tracking-wide text-brand-700">
              Recommended next
            </p>
            <p className="mt-0.5 text-lg font-bold text-ink-900">
              {data.recommended_next_topic}
            </p>
            <p className="mt-1 text-sm leading-relaxed text-ink-600">
              {data.recommendation_reason}
            </p>
          </div>
        </CardBody>
      </Card>

      <div className="grid gap-5 lg:grid-cols-3">
        {/* Trend */}
        <Card className="lg:col-span-2">
          <CardHeader
            title="Quiz score trend"
            description="Each point is one attempt. Dashed lines mark the adaptive thresholds."
            action={
              data.calibration_avg_gap != null ? (
                <Badge
                  tone={
                    data.calibration_avg_gap <= 12
                      ? "success"
                      : data.calibration_avg_gap <= 20
                        ? "warning"
                        : "danger"
                  }
                >
                  Calibration ± {data.calibration_avg_gap} pts
                </Badge>
              ) : undefined
            }
          />
          <CardBody>
            <QuizHistoryChart points={data.quiz_history} />
          </CardBody>
        </Card>

        {/* Activity */}
        <Card>
          <CardHeader title="Recent activity" />
          <CardBody>
            {data.recent_activity.length ? (
              <ul className="space-y-4">
                {data.recent_activity.map((item, i) => (
                  <ActivityRow key={`${item.kind}-${item.created_at}-${i}`} item={item} />
                ))}
              </ul>
            ) : (
              <p className="py-6 text-center text-sm text-ink-500">
                Nothing yet — start with the assessment.
              </p>
            )}
          </CardBody>
        </Card>
      </div>

      {/* Topics */}
      <Card>
        <CardHeader
          title="Topic mastery"
          description="Mastery is updated from your latest score on each topic."
        />
        <CardBody className="space-y-2.5">
          {data.topics.length ? (
            data.topics.map((row, i) => <TopicRow key={row.topic} row={row} index={i} />)
          ) : (
            <p className="py-6 text-center text-sm text-ink-500">
              No topic data yet. Take the assessment or a quiz to populate this.
            </p>
          )}
        </CardBody>
      </Card>

      {/* Strengths + roadmap progress */}
      <div className="grid gap-5 sm:grid-cols-2">
        <Card>
          <CardHeader title="Strengths" />
          <CardBody>
            {data.strong_topics.length ? (
              <div className="flex flex-wrap gap-1.5">
                {data.strong_topics.map((t) => (
                  <Badge key={t} tone="success">
                    {t}
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="text-sm text-ink-500">No strong topics yet.</p>
            )}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Roadmap progress" />
          <CardBody>
            <p className="flex items-center gap-2 text-sm text-ink-600">
              <CalendarCheck className="h-4 w-4 text-brand-600" />
              {data.roadmap_weeks_completed} of {learner.target_duration} weeks completed
            </p>
            <div className="mt-2">
              <AnimatedBar
                value={(data.roadmap_weeks_completed / learner.target_duration) * 100}
                tone="warning"
                height="h-2.5"
                ticks={learner.target_duration}
                tickClassName="border-ink-900/15"
                trackClassName="bg-ink-100"
              />
            </div>
            <p className="mt-1.5 flex items-center gap-2 text-sm text-ink-600">
              <MessageSquareText className="h-4 w-4 text-violet-600" />
              {data.total_tutor_sessions} tutor session
              {data.total_tutor_sessions === 1 ? "" : "s"}
            </p>
            <p className="mt-1.5 flex items-center gap-2 text-sm text-ink-600">
              <Award className="h-4 w-4 text-amber-600" />
              Level: {level.label}
            </p>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
