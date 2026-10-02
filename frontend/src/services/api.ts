import axios, { AxiosError } from "axios";

export const API_URL: string =
  import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: { "Content-Type": "application/json" },
  timeout: 60_000,
});

/**
 * Normalises every failure (network, HTTP, validation) into a plain Error
 * with a message that is safe to render directly in the UI.
 */
export function toFriendlyError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const err = error as AxiosError<{ detail?: string | unknown }>;

    if (err.code === "ECONNABORTED") {
      return "The request took too long. Please try again.";
    }
    if (!err.response) {
      return `Cannot reach the backend at ${API_URL}. Is it running?`;
    }

    const detail = err.response.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail.length > 0) {
      const first = detail[0] as { msg?: string };
      if (first?.msg) return first.msg.replace(/^Value error,\s*/, "");
    }
    return `Request failed (${err.response.status}). Please try again.`;
  }

  if (error instanceof Error) return error.message;
  return "Something went wrong. Please try again.";
}

export { AxiosError };
