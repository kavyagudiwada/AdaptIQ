import { api } from "./api";
import type {
  Quiz,
  QuizAnswerInput,
  QuizResult,
  Difficulty,
  QuizQuestion,
} from "@/types";

export async function generateQuiz(
  learnerId: number,
  topic?: string,
  seed?: string,
): Promise<Quiz> {
  const { data } = await api.post<Quiz>("/quiz/generate", {
    learner_id: learnerId,
    topic: topic ?? null,
    seed: seed ?? null,
  });
  return data;
}

export async function submitQuiz(
  learnerId: number,
  topic: string,
  difficulty: Difficulty,
  answers: QuizAnswerInput[],
  paper: QuizQuestion[],
  aiMode: "live" | "offline",
): Promise<QuizResult> {
  const { data } = await api.post<QuizResult>("/quiz/submit", {
    learner_id: learnerId,
    topic,
    difficulty,
    answers,
    paper,
    ai_mode: aiMode,
  });
  return data;
}
