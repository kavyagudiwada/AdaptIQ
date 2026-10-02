import { Link } from "react-router-dom";
import {
  Award,
  BookOpen,
  Blocks,
  Sparkles,
  TrendingUp,
} from "lucide-react";
import { StudentFigure } from "@/components/auth/StudentFigure";
import { FeatureCard } from "@/components/auth/FeatureCard";
import { cn } from "@/utils/cn";

const FEATURES = [
  {
    icon: BookOpen,
    title: "Courses",
    description: "Structured AI tracks, sequenced for real skill growth.",
    tone: "brand" as const,
  },
  {
    icon: Blocks,
    title: "Projects",
    description: "Build real artefacts instead of only watching videos.",
    tone: "violet" as const,
  },
  {
    icon: TrendingUp,
    title: "Progress",
    description: "See your level move as your evidence builds up.",
    tone: "emerald" as const,
  },
  {
    icon: Award,
    title: "Outcomes",
    description: "Finish job-ready, with proof of what you can do.",
    tone: "amber" as const,
  },
];

const STATS = [
  { value: "2x", label: "Faster Skills" },
  { value: "30%", label: "Course Completion" },
];

/** Small dark pill CTA used twice in the panel. */
function DarkPill({
  to,
  children,
  className,
}: {
  to: string;
  children: string;
  className?: string;
}) {
  return (
    <Link
      to={to}
      className={cn(
        "inline-flex h-9 items-center rounded-full bg-ink-900 px-4 text-sm",
        "font-semibold text-white transition-transform hover:scale-[1.04]",
        "active:scale-100 focus-visible:outline-none focus-visible:ring-2",
        "focus-visible:ring-brand-500 focus-visible:ring-offset-2",
        className,
      )}
    >
      {children}
    </Link>
  );
}

/**
 * The right-hand panel of the login page.
 *
 * It reads as a second, informational landing panel rather than a plain form
 * column: a headline, the "why it matters" block, a mascot CTA and a bottom
 * CTA. The sign-in card itself is layered over it by `LoginPage`.
 *
 * `compact` trims the panel down for the sign-up page, which shows it beneath
 * the form on small screens.
 */
export function AuthVisual({ compact = false }: { compact?: boolean }) {
  if (compact) {
    return (
      <div className="flex h-full flex-col justify-center px-6 py-10 sm:px-10">
        <div className="mx-auto w-full max-w-lg text-center">
          <h2 className="text-2xl font-bold tracking-tight text-ink-900">
            Learn Smarter. Grow Faster.
          </h2>
          <p className="mx-auto mt-3 max-w-md text-sm leading-relaxed text-ink-600">
            Your personalised AI tutor adapts to your skills, pace and progress.
          </p>

          <dl className="mt-8 grid grid-cols-2 gap-3">
            {STATS.map((stat) => (
              <div
                key={stat.label}
                className="rounded-2xl border border-ink-200/60 bg-white px-4 py-4 text-left shadow-sm"
              >
                <dt className="sr-only">{stat.label}</dt>
                <dd>
                  <span className="block text-2xl font-bold tracking-tight text-ink-900">
                    {stat.value}
                  </span>
                  <span className="mt-0.5 block text-xs font-medium text-ink-500">
                    {stat.label}
                  </span>
                </dd>
              </div>
            ))}
          </dl>

          <ul className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
            {FEATURES.map(({ icon: Icon, title, tone }) => (
              <li
                key={title}
                className="flex flex-col items-center gap-1.5 rounded-2xl border border-ink-200/60 bg-white px-2 py-3 shadow-sm"
              >
                <Icon className="h-4 w-4 text-brand-600" aria-hidden />
                <span className="text-[11px] font-medium leading-tight text-ink-600">
                  {title}
                </span>
                <span className="sr-only">{tone}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }

  const mascot = (
    <div className="flex w-24 shrink-0 flex-col items-center gap-2">
      <StudentFigure
        className="h-28"
        skin="#f3d0b0"
        hair="#3a2a20"
        shirt="#8b5cf6"
        trousers="#1f2937"
        backpack="#f59e0b"
      />
      <DarkPill to="/signup">Join Now</DarkPill>
    </div>
  );

  return (
    <div className="flex flex-col px-6 py-10 sm:px-10">
      {/* Headline */}
      <div>
        <h2 className="text-3xl font-bold leading-[1.15] tracking-tight text-ink-900 sm:text-[2.1rem]">
          Platform that helps{" "}
          <span className="relative inline-block">
            <span
              aria-hidden
              className="absolute inset-x-0 bottom-1 z-0 h-3 rounded-sm bg-sky-200/70"
            />
            <span className="relative z-10">curious minds</span>
          </span>{" "}
          learn faster, build skills and succeed anywhere{" "}
          <span aria-hidden>✨</span>
        </h2>
        <p className="mt-4 max-w-md text-sm leading-relaxed text-ink-600 sm:text-base">
          Adaptive lessons that notice where you stall, then change the
          explanation, the examples and the practice until it clicks.{" "}
          <span aria-hidden>🚀</span>
        </p>
      </div>

      {/* Stats + mascot */}
      <div className="mt-8 flex items-end justify-between gap-6">
        <dl className="grid flex-1 grid-cols-2 gap-3">
          {STATS.map((stat) => (
            <div
              key={stat.label}
              className="rounded-2xl border border-ink-200/60 bg-white/70 px-4 py-3.5"
            >
              <dt className="sr-only">{stat.label}</dt>
              <dd>
                <span className="block text-2xl font-bold tracking-tight text-ink-900 sm:text-3xl">
                  {stat.value}
                </span>
                <span className="mt-0.5 block text-xs font-medium text-ink-500">
                  {stat.label}
                </span>
              </dd>
            </div>
          ))}
        </dl>
        {mascot}
      </div>

      {/* Why it matters */}
      <div className="mt-10 text-center">
        <p className="text-xs font-semibold uppercase tracking-wider text-ink-400">
          Why does it matter?
        </p>
        <h3 className="mt-2.5 text-2xl font-bold leading-tight tracking-tight text-ink-900">
          Education Built for{" "}
          <span className="rounded-lg bg-sky-100 px-2 py-0.5">
            Real Growth
          </span>
        </h3>
        <p className="mx-auto mt-3 max-w-sm text-sm leading-relaxed text-ink-600">
          Build skills, track progress, and keep growing through personalized
          learning experiences.{" "}
          <span aria-hidden>👍</span>
        </p>
      </div>

      {/* Feature row */}
      <ul className="mt-7 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {FEATURES.map((feature) => (
          <li key={feature.title}>
            <FeatureCard {...feature} />
          </li>
        ))}
      </ul>

      {/* Bottom CTA */}
      <div className="mt-8 flex items-center justify-between gap-4 rounded-2xl border border-ink-200/60 bg-sky-50/60 px-4 py-3">
        <div className="flex items-center gap-3">
          <Sparkles className="h-4 w-4 shrink-0 text-brand-600" aria-hidden />
          <p className="text-xs font-medium leading-snug text-ink-600">
            Pick up exactly where you left off.
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-3">
          <StudentFigure
            className="h-14"
            skin="#8d5a3b"
            hair="#241a14"
            shirt="#10b981"
            trousers="#0f172a"
            backpack="#0ea5e9"
            wave
          />
          <DarkPill to="/signup">Start Learning</DarkPill>
        </div>
      </div>
    </div>
  );
}
