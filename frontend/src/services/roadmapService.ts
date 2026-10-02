import { api } from "./api";
import type { Adaptation, Roadmap, RoadmapCompletion } from "@/types";

export async function generateRoadmap(
  learnerId: number,
  force = false,
): Promise<Roadmap> {
  const { data } = await api.post<Roadmap>("/roadmap/generate", {
    learner_id: learnerId,
    force,
  });
  return data;
}

export async function getRoadmap(learnerId: number): Promise<Roadmap | null> {
  const { data } = await api.get<Roadmap | null>(`/roadmap/${learnerId}`);
  return data;
}

/**
 * Ask whether the active plan still matches the learner's latest results, so
 * the UI can offer to adapt it instead of silently leaving a stale plan.
 */
export async function getAdaptation(learnerId: number): Promise<Adaptation> {
  const { data } = await api.get<Adaptation>(`/roadmap/${learnerId}/adaptation`);
  return data;
}

export async function completeWeek(learnerId: number): Promise<RoadmapCompletion> {
  const { data } = await api.post<RoadmapCompletion>(
    `/roadmap/${learnerId}/week/complete`,
  );
  return data;
}
