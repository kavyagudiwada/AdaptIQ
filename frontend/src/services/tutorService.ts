import { api } from "./api";
import type { TutorExplainInput, TutorHistoryItem, TutorResponse } from "@/types";

export async function askTutor(
  input: TutorExplainInput,
): Promise<TutorResponse> {
  const { data } = await api.post<TutorResponse>("/tutor/explain", input);
  return data;
}

export async function getTutorHistory(
  learnerId: number,
): Promise<TutorHistoryItem[]> {
  const { data } = await api.get<{ sessions: TutorHistoryItem[] }>(
    `/tutor/${learnerId}/history`,
  );
  return data.sessions;
}
