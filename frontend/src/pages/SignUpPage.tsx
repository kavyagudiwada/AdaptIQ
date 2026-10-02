import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthVisual } from "@/components/auth/AuthVisual";
import { SignUpForm } from "@/components/auth/SignUpForm";
import { Logo } from "@/components/common/Logo";
import { useAuth } from "@/hooks/useAuth";

export default function SignUpPage() {
  const navigate = useNavigate();
  const { isAuthenticated, session } = useAuth();

  // Already signed in *and* linked to a learner? Skip the form. A brand-new
  // account has no learner yet, so it must still go through the profile step.
  useEffect(() => {
    if (isAuthenticated && session?.learner) {
      navigate("/dashboard", { replace: true });
    }
  }, [isAuthenticated, session, navigate]);

  return (
    <div className="min-h-screen md:grid md:grid-cols-[52fr_48fr] lg:grid-cols-[45fr_55fr]">
      {/* Form column */}
      <main className="flex min-h-screen flex-col px-5 py-8 sm:px-10 lg:px-14">
        <Logo to="/" light />

        <div className="flex flex-1 items-center py-10">
          <div className="mx-auto w-full max-w-[400px] animate-slide-up">
            <h1 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Create your account
            </h1>
            <p className="mt-2 text-sm text-ink-200 sm:text-base">
              Start your personalized learning journey in under a minute.
            </p>

            <div className="mt-8">
              {/* New accounts have no learner record yet, so the next stop is
                  the profile form, which is then linked to the account. */}
              <SignUpForm
                onRegistered={() => navigate("/profile", { replace: true })}
              />
            </div>
          </div>
        </div>

        {/* Compact brand panel for small screens */}
        <div className="border-t border-white/10 pt-8 md:hidden">
          <AuthVisual compact />
        </div>

        <p className="mt-8 text-center text-xs text-ink-300">
          AdaptIQ · Adaptive learning, not a generic chatbot.
        </p>
      </main>

      {/* Visual column */}
      <aside className="hidden border-l border-ink-100 bg-gradient-to-br from-sky-50 via-brand-50 to-white md:block">
        <AuthVisual />
      </aside>
    </div>
  );
}
