import { Link } from "react-router-dom";
import {
  ArrowRight,
  BarChart3,
  Brain,
  Compass,
  Gauge,
  Lightbulb,
  MessageSquareText,
  Sparkles,
  Target,
} from "lucide-react";
import { Button } from "@/components/common/Button";
import { Card } from "@/components/common/Card";
import { Logo } from "@/components/common/Logo";
import { FlashCard } from "@/components/landing/FlashCard";
import { ADAPTIVE_RULES } from "@/data/options";
import { useLearner } from "@/hooks/useLearner";

/** Front and back share the same copy so the flip stays coherent. */
const FLASH_CARDS = [
  {
    icon: Compass,
    title: "Personalised Path",
    kicker: "Roadmap",
    body: "Your roadmap is rebuilt from your assessment score, weak topics, goal and weekly hours — never a generic syllabus.",
    accent: "border-brand-200 bg-brand-50",
    iconAccent: "bg-brand-50 text-brand-600",
  },
  {
    icon: Target,
    title: "Adaptive Practice",
    kicker: "Difficulty",
    body: "Question difficulty moves with you: easy while you are shaky, hard once you are ready to be challenged.",
    accent: "border-emerald-200 bg-emerald-50",
    iconAccent: "bg-emerald-50 text-emerald-600",
  },
  {
    icon: Brain,
    title: "Misconception Diagnosis",
    kicker: "Diagnosis",
    body: "A wrong answer is traced to the specific misconception behind it, so the fix targets the cause and not the symptom.",
    accent: "border-violet-200 bg-violet-50",
    iconAccent: "bg-violet-50 text-violet-600",
  },
  {
    icon: Gauge,
    title: "Confidence Calibration",
    kicker: "Self-check",
    body: "Rate how sure you feel, then see the gap between confidence and correctness — the gap is where real learning hides.",
    accent: "border-amber-200 bg-amber-50",
    iconAccent: "bg-amber-50 text-amber-600",
  },
  {
    icon: BarChart3,
    title: "Progress You Can See",
    kicker: "Tracking",
    body: "Mastery per topic, streak, and time invested, so progress is evidence rather than a feeling.",
    accent: "border-sky-200 bg-sky-50",
    iconAccent: "bg-sky-50 text-sky-600",
  },
  {
    icon: MessageSquareText,
    title: "AI Tutor Chat",
    kicker: "Help",
    body: "Ask anything mid-lesson and get an explanation pitched at your current level, in plain language.",
    accent: "border-rose-200 bg-rose-50",
    iconAccent: "bg-rose-50 text-rose-600",
  },
];

const FEATURES = [
  {
    icon: Compass,
    title: "Personalised Learning Paths",
    body: "A roadmap built from your assessment score, weak topics, goal and weekly hours — not a generic syllabus.",
    accent: "bg-brand-50 text-brand-600",
  },
  {
    icon: Target,
    title: "Adaptive Practice",
    body: "Quiz difficulty moves with you: easy when you struggle, hard when you are ready to be challenged.",
    accent: "bg-emerald-50 text-emerald-600",
  },
  {
    icon: MessageSquareText,
    title: "AI Explanations",
    body: "Explanations written at your level — analogies for beginners, mathematics and trade-offs for advanced.",
    accent: "bg-violet-50 text-violet-600",
  },
  {
    icon: BarChart3,
    title: "Progress Intelligence",
    body: "Topic-level mastery, weak-area detection and a clear, justified recommendation for what to do next.",
    accent: "bg-amber-50 text-amber-600",
  },
];

const FLOW = [
  "Learner Profile",
  "Initial Assessment",
  "AI Knowledge Analysis",
  "Personalised Roadmap",
  "AI Tutor",
  "Adaptive Quiz",
  "Progress Dashboard",
];

export default function LandingPage() {
  const { learner } = useLearner();

  return (
    <div className="min-h-screen">
      {/* Nav */}
      <header className="sticky top-0 z-30 border-b border-white/10 bg-[#04060f]/55 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-6xl items-center px-4 sm:px-6">
          <Logo light />
          <div className="ml-auto flex items-center gap-2">
            {learner ? (
              <Link
                to="/dashboard"
                className="hidden h-9 items-center rounded-xl bg-cyan-400/15 px-4 text-sm font-medium text-cyan-100 ring-1 ring-inset ring-cyan-300/25 transition hover:bg-cyan-400/25 sm:inline-flex"
              >
                Dashboard
              </Link>
            ) : (
              <Link
                to="/login"
                className="hidden h-9 items-center rounded-xl px-3 text-sm font-medium text-ink-200 transition hover:bg-white/10 hover:text-white sm:inline-flex"
              >
                Sign in
              </Link>
            )}
            <Link to={learner ? "/dashboard" : "/profile"}>
              <Button size="md">{learner ? "Continue learning" : "Start Learning"}</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero: the product image, whole and uncropped, scaled to fit the
          window, sitting inside the deep-ink human–AI ecosystem background. */}
      <section className="relative isolate overflow-hidden bg-transparent">
        {/* Environment: low-key cyan/indigo glows + a faint masked grid so the
            illustration reads as sitting in a space rather than floating on
            flat colour. */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 bg-[radial-gradient(55%_45%_at_50%_18%,rgba(34,211,238,0.09),transparent_70%)]"
        />
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 opacity-[0.35] [background-image:linear-gradient(to_right,rgba(140,190,255,0.06)_1px,transparent_1px),linear-gradient(to_bottom,rgba(140,190,255,0.06)_1px,transparent_1px)] [background-size:56px_56px] [mask-image:radial-gradient(70%_60%_at_50%_40%,black,transparent_75%)]"
        />
        <div
          aria-hidden
          className="pointer-events-none absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-[#05081a]/70 via-[#05081a]/20 to-transparent"
        />

        {/* Floating background decorations: soft icons and glows drifting in the
            space around the illustration. Purely decorative (aria-hidden, no
            pointer events) and motion-safe via .animate-float. */}
        <div aria-hidden className="pointer-events-none absolute inset-0">
          <div
            className="absolute left-[5%] top-[10%] animate-float text-cyan-300/30"
            style={{ animationDuration: "7.5s", animationDelay: "0.4s" }}
          >
            <Brain className="h-12 w-12" strokeWidth={1.4} />
          </div>
          <div
            className="absolute right-[6%] top-[13%] animate-float text-indigo-300/30"
            style={{ animationDuration: "8.5s", animationDelay: "1.1s" }}
          >
            <Target className="h-11 w-11" strokeWidth={1.4} />
          </div>
          <div
            className="absolute left-[8%] top-[46%] animate-float text-sky-300/30"
            style={{ animationDuration: "9s", animationDelay: "0.2s" }}
          >
            <Compass className="h-14 w-14" strokeWidth={1.2} />
          </div>
          <div
            className="absolute right-[8%] top-[42%] animate-float text-cyan-400/25"
            style={{ animationDuration: "7s", animationDelay: "1.6s" }}
          >
            <MessageSquareText className="h-12 w-12" strokeWidth={1.4} />
          </div>
          <div
            className="absolute left-[3.5%] top-[22%] animate-float text-amber-200/20"
            style={{ animationDuration: "8s", animationDelay: "2.1s" }}
          >
            <Lightbulb className="h-9 w-9" strokeWidth={1.6} />
          </div>
          <div
            className="absolute right-[3.5%] top-[26%] animate-float text-cyan-200/25"
            style={{ animationDuration: "7.5s", animationDelay: "0.8s" }}
          >
            <Sparkles className="h-8 w-8" strokeWidth={1.6} />
          </div>
          <div
            className="absolute left-[13%] top-[5%] h-24 w-24 animate-float rounded-full bg-cyan-400/15 blur-2xl"
            style={{ animationDuration: "10s", animationDelay: "0.6s" }}
          />
          <div
            className="absolute right-[13%] top-[64%] h-20 w-20 animate-float rounded-full bg-violet-500/15 blur-2xl"
            style={{ animationDuration: "11s", animationDelay: "1.4s" }}
          />
        </div>

        {/* Warm/cyan aura behind the artwork so its edge dissolve lands on a
            soft haze instead of the flat ecosystem surface. Decorative. */}
        <div
          aria-hidden
          className="pointer-events-none absolute left-1/2 top-[46%] h-[68%] w-[86%] -translate-x-1/2 -translate-y-1/2 rounded-full bg-[radial-gradient(50%_55%_at_50%_55%,rgba(244,214,196,0.10),rgba(34,211,238,0.05)_55%,transparent_76%)] blur-2xl"
        />

        <figure className="relative flex h-[calc(100dvh-4rem)] w-full items-center justify-center px-4 sm:px-6">
          <img
            src="/landingimage.png"
            alt="Students learning together with the AdaptIQ AI tutor"
            width={1521}
            height={1034}
            decoding="async"
            fetchPriority="high"
            className="block h-full w-full object-contain drop-shadow-[0_28px_60px_-30px_rgba(94,234,212,0.10)]
            [mask-image:linear-gradient(to_bottom,black_60%,transparent_100%),linear-gradient(to_right,black_60%,transparent_100%),linear-gradient(to_top,black_60%,transparent_100%),linear-gradient(to_left,black_60%,transparent_100%)]
            [mask-composite:intersect]
            [-webkit-mask-image:linear-gradient(to_bottom,black_60%,transparent_100%),linear-gradient(to_right,black_60%,transparent_100%),linear-gradient(to_top,black_60%,transparent_100%),linear-gradient(to_left,black_60%,transparent_100%)]
            [-webkit-mask-composite:source-in]"
          />
        </figure>
      </section>

      {/* Flash cards */}
      <section id="flashcards" className="bg-transparent py-16 sm:py-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <span className="inline-flex items-center gap-2 rounded-full bg-brand-50 px-3.5 py-1.5 text-xs font-semibold text-brand-700 ring-1 ring-inset ring-brand-600/20">
              Flip the cards
            </span>
            <h2 className="mt-4 text-3xl font-bold tracking-tight text-white">
              What AdaptIQ does for you
            </h2>
            <p className="mt-3 text-ink-400">
              Six things that change as you learn. Hover or tap any card to see it
              from the other side.
            </p>
          </div>

          <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {FLASH_CARDS.map((card) => (
              <FlashCard key={card.title} {...card} />
            ))}
          </div>
        </div>
      </section>

      {/* What is adaptive learning */}
      <section id="how-it-works" className="border-y border-white/10 py-16 sm:py-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-white">
              What "adaptive" actually means here
            </h2>
            <p className="mt-3 text-ink-400">
              Every stage feeds the next. The system measures you, then changes what it
              shows you, how deeply it explains it, and how hard it makes the practice.
            </p>
          </div>

          <div className="mt-10 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {FEATURES.map((feature) => (
              <Card key={feature.title} className="p-6 transition hover:shadow-md">
                <span
                  className={`inline-flex h-11 w-11 items-center justify-center rounded-xl ${feature.accent}`}
                >
                  <feature.icon className="h-5.5 w-5.5" />
                </span>
                <h3 className="mt-4 text-base font-semibold text-ink-900">
                  {feature.title}
                </h3>
                <p className="mt-1.5 text-sm leading-relaxed text-ink-500">
                  {feature.body}
                </p>
              </Card>
            ))}
          </div>

          {/* Difficulty rules */}
          <Card className="mx-auto mt-10 max-w-2xl overflow-hidden">
            <div className="border-b border-ink-100 bg-white px-6 py-4">
              <h3 className="flex items-center gap-2 text-base font-semibold text-ink-900">
                <Target className="h-4 w-4 text-brand-600" />
                Transparent difficulty rules
              </h3>
              <p className="mt-0.5 text-sm text-ink-500">
                No black box — the same thresholds decide your next question set.
              </p>
            </div>
            <ul className="divide-y divide-ink-100">
              {ADAPTIVE_RULES.map((rule) => (
                <li key={rule.range} className="flex items-center justify-between px-6 py-3.5">
                  <span className="font-mono text-sm text-ink-700">{rule.range}</span>
                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold ${
                      rule.tone === "emerald"
                        ? "bg-emerald-50 text-emerald-700"
                        : rule.tone === "amber"
                          ? "bg-amber-50 text-amber-700"
                          : "bg-rose-50 text-rose-700"
                    }`}
                  >
                    {rule.result}
                  </span>
                </li>
              ))}
            </ul>
          </Card>
        </div>
      </section>

      {/* Flow */}
      <section className="py-16 sm:py-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <h2 className="text-center text-3xl font-bold tracking-tight text-white">
            Your learning loop
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-center text-ink-400">
            A complete personalised path you can walk through in a few minutes.
          </p>

          <ol className="mt-10 grid gap-2.5 sm:grid-cols-2 lg:grid-cols-4">
            {FLOW.map((step, i) => (
              <li
                key={step}
                className="flex items-center gap-3 rounded-xl border border-ink-200 bg-white px-4 py-3.5"
              >
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-brand-50 text-xs font-bold text-brand-700">
                  {i + 1}
                </span>
                <span className="text-sm font-medium text-ink-800">{step}</span>
              </li>
            ))}
          </ol>

          <div className="mt-12 flex flex-col items-center">
            <Link to={learner ? "/dashboard" : "/profile"} className="w-full sm:w-auto">
              <Button size="lg" block icon={<ArrowRight className="h-4 w-4" />}>
                {learner ? "Go to my dashboard" : "Create my learning profile"}
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
