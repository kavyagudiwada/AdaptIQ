import { lazy, Suspense } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "@/hooks/useAuth";
import { LearnerProvider } from "@/hooks/useLearner";
import MainLayout from "@/layouts/MainLayout";
import LandingPage from "@/pages/LandingPage";
import BackgroundEcosystem from "@/components/common/BackgroundEcosystem";

// Split per route so the chart library and page code load on demand.
const LoginPage = lazy(() => import("@/pages/LoginPage"));
const SignUpPage = lazy(() => import("@/pages/SignUpPage"));
const ForgotPasswordPage = lazy(() => import("@/pages/ForgotPasswordPage"));
const GoogleCallbackPage = lazy(() => import("@/pages/GoogleCallbackPage"));
const ProfilePage = lazy(() => import("@/pages/ProfilePage"));
const AssessmentPage = lazy(() => import("@/pages/AssessmentPage"));
const RoadmapPage = lazy(() => import("@/pages/RoadmapPage"));
const TutorPage = lazy(() => import("@/pages/TutorPage"));
const QuizPage = lazy(() => import("@/pages/QuizPage"));
const DashboardPage = lazy(() => import("@/pages/DashboardPage"));

function RouteFallback() {
  return (
    <div className="flex items-center justify-center py-24" role="status" aria-live="polite">
      <span className="h-8 w-8 animate-spin rounded-full border-[3px] border-brand-200 border-t-brand-600" />
    </div>
  );
}

export default function App() {
  return (
    <LearnerProvider>
      <AuthProvider>
        <BrowserRouter>
          <BackgroundEcosystem />
          <Suspense fallback={<RouteFallback />}>
            <Routes>
              <Route path="/" element={<LandingPage />} />

              {/* Auth screens sit outside the app shell */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignUpPage />} />
              <Route path="/forgot-password" element={<ForgotPasswordPage />} />
              {/* OAuth landing: must sit outside the app shell */}
              <Route path="/auth/google/callback" element={<GoogleCallbackPage />} />

              <Route element={<MainLayout />}>
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/assessment" element={<AssessmentPage />} />
                <Route path="/roadmap" element={<RoadmapPage />} />
                <Route path="/tutor" element={<TutorPage />} />
                <Route path="/quiz" element={<QuizPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                {/* /progress is the same personalised view as the dashboard */}
                <Route path="/progress" element={<Navigate to="/dashboard" replace />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Route>
            </Routes>
          </Suspense>
        </BrowserRouter>
      </AuthProvider>
    </LearnerProvider>
  );
}
