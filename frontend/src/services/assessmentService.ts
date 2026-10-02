import { api } from "./api";
import type {
  AssessmentAnswerInput,
  AssessmentPaper,
  AssessmentResult,
} from "@/types";

export async function generateAssessment(
  learnerId: number,
): Promise<AssessmentPaper> {
  const { data } = await api.post<AssessmentPaper>("/assessment/generate", {
    learner_id: learnerId,
  });
  return data;
}

export async function submitAssessment(
  learnerId: number,
  answers: AssessmentAnswerInput[],
): Promise<AssessmentResult> {
  const { data } = await api.post<AssessmentResult>("/assessment/submit", {
    learner_id: learnerId,
    answers,
  });
  return data;
}
