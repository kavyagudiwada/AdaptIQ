import { api } from "./api";
import type { HealthResponse, ProgressSummary } from "@/types";

export async function getProgress(learnerId: number): Promise<ProgressSummary> {
  const { data } = await api.get<ProgressSummary>(`/progress/${learnerId}`);
  return data;
}

export async function getHealth(): Promise<HealthResponse> {
  const { data } = await api.get<HealthResponse>("/health");
  return data;
}
