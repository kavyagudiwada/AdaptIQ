import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { LoginForm } from "@/components/auth/LoginForm";
import { useAuth } from "@/hooks/useAuth";

/**
 * Sign-in page.
 *
 * Desktop is a 58/42 split: a light sky-blue hero on the left holding the
 * headline and the illustration, and a white panel on the right holding only
 * the sign-in card.
 *
 * Below `lg` both sections switch to `display: contents`, which lets their
 * children participate in the parent flex column. That is what makes the
 * mobile order (form, headline, description, illustration) possible without
 * duplicating markup.
 */
export default function LoginPage() {
  const navigate = useNavigate();
  const { isAuthenticated, session } = useAuth();

  // Already signed in with a learner? Skip the form. An account without a
  // linked learner still needs the profile step, so leave the form up.
  useEffect(() => {
    if (isAuthenticated && session?.learner) {
      navigate("/dashboard", { replace: true });
    }
  }, [isAuthenticated, session, navigate]);

  return (
    <div className="flex min-h-screen flex-col lg:grid lg:h-screen lg:grid-cols-[58fr_42fr] lg:overflow-hidden">
      {/* ---------------- Hero section ---------------- */}
      <div className="contents lg:flex lg:min-h-0 lg:flex-col lg:overflow-hidden lg:px-10 lg:py-5 xl:px-14">
        <div className="order-3 flex shrink-0 flex-col items-center px-5 pt-8 text-center lg:px-0 lg:pt-2">
          <h1 className="max-w-2xl text-3xl font-bold leading-[1.1] tracking-tight text-white sm:text-4xl xl:text-[2.6rem]">
            Platform that helps{" "}
            <span className="relative inline-block">
              <span
                aria-hidden
                className="absolute inset-x-0 bottom-1 z-0 h-3 rounded-sm bg-cyan-400/30"
              />
              <span className="relative z-10">curious minds</span>
            </span>{" "}
            learn faster, build skills and succeed anywhere{" "}
            <span aria-hidden>✨</span>
          </h1>

          <p className="mt-3 max-w-lg text-sm leading-relaxed text-ink-200 sm:text-base">
            Adaptive lessons that notice where you stall, then change the
            explanation, the examples and the practice until it clicks.{" "}
            <span aria-hidden>🚀</span>
          </p>
        </div>

        {/* Takes whatever height is left, so the illustration scales down
            instead of pushing the page past the fold. */}
        <div className="order-4 flex min-h-0 flex-1 items-start justify-center px-5 pb-8 pt-4 lg:px-0 lg:pb-2 lg:pt-2">
          <img
            src="/studify.png"
            alt="Students learning together with AdaptIQ"
            width={1511}
            height={1041}
            decoding="async"
            fetchPriority="high"
            className="mx-auto block h-auto max-h-full w-full max-w-2xl animate-fade-in select-none object-contain
            [mask-image:linear-gradient(to_bottom,black_70%,transparent_100%),linear-gradient(to_right,black_70%,transparent_100%),linear-gradient(to_top,black_70%,transparent_100%),linear-gradient(to_left,black_70%,transparent_100%)]
            [mask-composite:intersect]
            [-webkit-mask-image:linear-gradient(to_bottom,black_70%,transparent_100%),linear-gradient(to_right,black_70%,transparent_100%),linear-gradient(to_top,black_70%,transparent_100%),linear-gradient(to_left,black_70%,transparent_100%)]
            [-webkit-mask-composite:source-in]"
          />
        </div>
      </div>

      {/* ---------------- Landing panel + sign-in card ---------------- */}
      <div className="contents lg:flex lg:flex-col lg:overflow-y-auto lg:border-l lg:border-white/10">
        {/* Sign-in card: on mobile it is order 2, directly under the logo */}
        <div className="order-2 px-5 pt-6 lg:px-10 lg:pt-12">
          <div
            className={[
              "mx-auto w-full max-w-[420px] rounded-[24px] bg-white p-6 sm:p-7",
              "ring-1 ring-ink-200/70",
              "shadow-[0_28px_70px_-24px_rgba(16,42,67,0.28)]",
              "animate-slide-up",
              // Stays fully inside the viewport: it used to be pulled up with a
              // negative top margin, which put the card's heading above y=0 on
              // every desktop size and clipped it.
              "lg:relative lg:z-10 lg:mb-2",
            ].join(" ")}
          >
            <img
              src="/adaptiq-mark.png"
              alt=""
              width={192}
              height={135}
              decoding="async"
              className="mx-auto mb-5 block h-14 w-auto select-none"
            />
            <h2 className="text-2xl font-bold tracking-tight text-ink-900 sm:text-[1.7rem]">
              Welcome Back
            </h2>
            <p className="mt-1.5 text-sm text-ink-500">
              Continue your personalized learning journey.
            </p>

            <div className="mt-6">
              <LoginForm
                onAuthenticated={(result) =>
                  // No linked learner yet? The profile step comes first.
                  navigate(result.learner ? "/dashboard" : "/profile", {
                    replace: true,
                  })
                }
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
