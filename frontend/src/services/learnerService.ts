import { api } from "./api";
import type { LearnerProfile, LearnerProfileInput } from "@/types";

export async function saveProfile(
  input: LearnerProfileInput,
): Promise<LearnerProfile> {
  const { data } = await api.post<LearnerProfile>("/learner/profile", input);
  return data;
}

export async function getLearner(learnerId: number): Promise<LearnerProfile> {
  const { data } = await api.get<LearnerProfile>(`/learner/${learnerId}`);
  return data;
}
