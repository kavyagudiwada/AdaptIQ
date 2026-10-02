export type Level = "beginner" | "intermediate" | "advanced";

export type LearningGoal =
  | "academic"
  | "placement"
  | "interview"
  | "project"
  | "general";

export type Difficulty = "easy" | "medium" | "hard";

export type AiMode = "live" | "offline";

/* ---------------- Learner ---------------- */

export interface LearnerProfile {
  id: number;
  name: string;
  topic: string;
  /** Effective level, rewritten from real evidence. */
  current_level: Level;
  /** What the learner claimed at signup, kept so we can show the gap. */
  self_reported_level: Level;
  learning_goal: LearningGoal;
  hours_per_week: number;
  target_duration: number;
  estimated_level: Level | null;
  created_at: string;
}

export interface LearnerProfileInput {
  name: string;
  topic: string;
  current_level: Level;
  learning_goal: LearningGoal;
  hours_per_week: number;
  target_duration: number;
}

/* ---------------- Assessment ---------------- */

export interface AssessmentQuestion {
  id: string;
  question: string;
  options: string[];
  correct_index: number;
  subtopic: string;
  difficulty: Difficulty;
}

export interface AssessmentPaper {
  assessment_id: number | null;
  learner_id: number;
  questions: AssessmentQuestion[];
  total_questions: number;
  ai_mode: AiMode;
}

export interface AssessmentAnswerInput {
  question_id: string;
  selected_index: number;
}

export interface TopicBreakdown {
  subtopic: string;
  correct: number;
  total: number;
  percentage: number;
}

export interface AssessmentResult {
  assessment_id: number;
  learner_id: number;
  score: number;
  total_questions: number;
  percentage: number;
  strong_topics: string[];
  weak_topics: string[];
  estimated_level: Level;
  topic_breakdown: TopicBreakdown[];
  feedback: string;
  ai_mode: AiMode;
}

/* ---------------- Roadmap ---------------- */

export interface RoadmapWeek {
  week: number;
  title: string;
  focus: string;
  topics: RoadmapTopic[];
  practice_target: number;
  milestone: string;
}

export interface RoadmapTopic {
  name: string;
  subtopic: string;
  difficulty: Difficulty;
  estimated_hours: number;
  why_this_matters: string;
  resources: string[];
}

export type LevelSource = "assessment" | "practice" | "self_reported";

/** How the active plan compares to the learner's latest evidence. */
export interface Adaptation {
  is_stale: boolean;
  revision: number;
  effective_level: Level;
  self_reported_level: Level;
  level_source: LevelSource;
  level_changed_from_start: boolean;
  average_mastery: number;
  total_attempts: number;
  weak_topics: string[];
  strong_topics: string[];
  reasons: string[];
  basis_signature: string | null;
  current_signature: string | null;
}

export interface Roadmap {
  id: number;
  learner_id: number;
  title: string;
  duration: number;
  weeks: RoadmapWeek[];
  personalization_notes: string[];
  focus_areas: string[];
  ai_mode: AiMode;
  created_at: string;
  revision: number;
  superseded: boolean;
  completed_weeks: number;
  adaptation_reason: string | null;
  adaptation: Adaptation | null;
}

/** Result of checking off a roadmap week. */
export interface RoadmapCompletion {
  completed_weeks: number;
  duration: number;
  completed: boolean;
}

/* ---------------- Tutor ---------------- */

export interface TutorSection {
  heading: string;
  body: string;
}

export interface TutorResponse {
  topic: string;
  explanation: string;
  example: string;
  key_points: string[];
  common_mistakes: string[];
  follow_up_question: string;
  difficulty: Difficulty;
  personalized_note: string;
  ai_mode: AiMode;
}

export interface TutorMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface TutorExplainInput {
  learner_id: number;
  topic: string;
  question?: string;
  difficulty?: Difficulty;
}

export interface TutorHistoryItem {
  id: number;
  topic: string;
  subtopic: string;
  difficulty: Difficulty;
  explanation: string;
  example: string;
  key_points: string[];
  common_mistakes: string[];
  ai_mode: AiMode;
  created_at: string;
}

/* ---------------- Quiz ---------------- */

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correct_index: number;
  subtopic: string;
  difficulty: Difficulty;
  explanation: string;
}

export interface Quiz {
  quiz_id: number | null;
  learner_id: number;
  topic: string;
  difficulty: Difficulty;
  questions: QuizQuestion[];
  total_questions: number;
  adaptation_note: string;
  previous_percentage: number | null;
  ai_mode: AiMode;
}

export interface QuizAnswerInput {
  question_id: string;
  selected_index: number;
  /** 1 (guessing) to 5 (very sure), used for confidence calibration. */
  confidence?: number;
}

export interface QuizReviewItem {
  question_id: string;
  question: string;
  subtopic: string;
  your_answer: string;
  correct_answer: string;
  was_correct: boolean;
  explanation: string;
  misconception: string | null;
  misconception_fix: string | null;
}

export interface Misconception {
  question_id: string;
  misconception: string;
  fix: string;
}

export interface QuizResult {
  attempt_id: number;
  learner_id: number;
  topic: string;
  difficulty: Difficulty;
  score: number;
  total_questions: number;
  percentage: number;
  next_difficulty: Difficulty;
  difficulty_changed: boolean;
  system_message: string;
  weak_topics: string[];
  strong_topics: string[];
  recommended_action: string;
  ai_mode: AiMode;
  /** The learner's effective level after this attempt. */
  current_level: Level | null;
  level_changed: boolean;
  level_source: LevelSource | null;
  /** True when the active plan no longer reflects these results. */
  roadmap_stale: boolean;
  /** Question-by-question review with misconception diagnosis. */
  review: QuizReviewItem[];
  misconceptions: Misconception[];
  /** 0-100 average of how sure the learner felt (null = not rated). */
  confidence_avg: number | null;
  /** confidence_avg - percentage; positive = overconfident. */
  calibration_gap: number | null;
  calibration_feedback: string | null;
}

/* ---------------- Progress ---------------- */

export interface TopicProgress {
  topic: string;
  progress_percentage: number;
  mastery_level: Level;
  last_score: number;
  updated_at: string;
}

export interface ActivityItem {
  label: string;
  detail: string;
  kind: "profile" | "assessment" | "roadmap" | "tutor" | "quiz";
  created_at: string;
}

export interface ProgressSummary {
  learner_id: number;
  learner_name: string;
  topic: string;
  overall_progress: number;
  assessment_percentage: number | null;
  estimated_level: Level;
  current_topic: string;
  recommended_next_topic: string;
  recommendation_reason: string;
  topics: TopicProgress[];
  strong_topics: string[];
  weak_topics: string[];
  quiz_history: QuizHistoryPoint[];
  calibration_avg_gap: number | null;
  learning_streak: number;
  total_quizzes: number;
  total_tutor_sessions: number;
  roadmap_weeks_completed: number;
  recent_activity: ActivityItem[];
  ai_mode: AiMode;
}

export interface QuizHistoryPoint {
  attempt_id: number;
  topic: string;
  difficulty: Difficulty;
  percentage: number;
  confidence_avg?: number | null;
  calibration_gap?: number | null;
  created_at: string;
}

/* ---------------- Health / meta ---------------- */

export interface HealthResponse {
  status: string;
  database: string;
  ai_provider: string;
  ai_mode: AiMode;
  version: string;
}

export interface TopicSuggestion {
  topic: string;
}
