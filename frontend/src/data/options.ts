import type { LearningGoal, Level } from "@/types";

export const LEVEL_OPTIONS: { value: Level; label: string; blurb: string }[] = [
  {
    value: "beginner",
    label: "Beginner",
    blurb: "New to the topic. Prefer analogies and simple language.",
  },
  {
    value: "intermediate",
    label: "Intermediate",
    blurb: "Comfortable with basics. Want practical detail and formulas.",
  },
  {
    value: "advanced",
    label: "Advanced",
    blurb: "Deep knowledge. Want mathematics, trade-offs and limitations.",
  },
];

export const GOAL_OPTIONS: { value: LearningGoal; label: string; blurb: string }[] = [
  { value: "placement", label: "Placement Preparation", blurb: "Interview-style questions and company patterns." },
  { value: "interview", label: "Interview", blurb: "Rapid-fire concepts and whiteboard reasoning." },
  { value: "academic", label: "Academic", blurb: "Syllabus coverage and exam-style questions." },
  { value: "project", label: "Project", blurb: "Implementation steps you can actually build from." },
  { value: "general", label: "General Learning", blurb: "Balanced reading, practice and small projects." },
];

export const TOPIC_SUGGESTIONS = [
  "Machine Learning",
  "Data Science",
  "Python",
  "Deep Learning",
  "Data Structures & Algorithms",
  "Data Structures",
];

export const DIFFICULTY_META: Record<
  string,
  { label: string; className: string; dot: string }
> = {
  easy: {
    label: "Easy",
    className: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
    dot: "bg-emerald-500",
  },
  medium: {
    label: "Medium",
    className: "bg-amber-50 text-amber-700 ring-amber-600/20",
    dot: "bg-amber-500",
  },
  hard: {
    label: "Hard",
    className: "bg-rose-50 text-rose-700 ring-rose-600/20",
    dot: "bg-rose-500",
  },
};

export const LEVEL_META: Record<string, { label: string; className: string }> = {
  beginner: { label: "Beginner", className: "bg-sky-50 text-sky-700 ring-sky-600/20" },
  intermediate: {
    label: "Intermediate",
    className: "bg-violet-50 text-violet-700 ring-violet-600/20",
  },
  advanced: {
    label: "Advanced",
    className: "bg-brand-50 text-brand-700 ring-brand-600/20",
  },
};

export const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: "LayoutDashboard" },
  { to: "/assessment", label: "Assessment", icon: "ClipboardCheck" },
  { to: "/roadmap", label: "Learning Roadmap", icon: "Map" },
  { to: "/tutor", label: "AI Tutor", icon: "Sparkles" },
  { to: "/quiz", label: "Practice", icon: "Target" },
  { to: "/progress", label: "Progress", icon: "TrendingUp" },
] as const;

/** Mirrors the backend adaptive thresholds so the UI can explain the logic. */
export const ADAPTIVE_RULES = [
  { range: "score < 50%", result: "Easy", tone: "emerald" },
  { range: "50% – 74%", result: "Medium", tone: "amber" },
  { range: "score ≥ 75%", result: "Hard", tone: "rose" },
] as const;
