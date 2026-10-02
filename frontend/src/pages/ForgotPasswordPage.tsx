import { Link } from "react-router-dom";
import { ArrowLeft, KeyRound } from "lucide-react";
import { Button } from "@/components/common/Button";
import { Card, CardBody } from "@/components/common/Card";
import { Logo } from "@/components/common/Logo";

/**
 * Placeholder for password recovery. Resetting a password needs a real
 * accounts table plus an email provider, neither of which this build has.
 */
export default function ForgotPasswordPage() {
  return (
    <div className="flex min-h-screen flex-col px-5 py-8 sm:px-10">
      <Logo to="/" light />

      <div className="flex flex-1 items-center py-10">
        <Card className="mx-auto w-full max-w-md animate-slide-up">
          <CardBody className="px-6 py-10 text-center">
            <span className="mx-auto flex h-11 w-11 items-center justify-center rounded-2xl bg-amber-50 text-amber-600">
              <KeyRound className="h-5 w-5" aria-hidden />
            </span>
            <h1 className="mt-4 text-xl font-bold tracking-tight text-ink-900">
              Reset your password
            </h1>
            <p className="mt-2 text-sm leading-relaxed text-ink-500">
              Password recovery is not available in this build. If you already
              have a learner profile saved in this browser, you can pick up
              exactly where you left off.
            </p>
            <div className="mt-6 flex flex-col gap-2.5">
              <Link to="/dashboard">
                <Button size="lg" block>
                  Go to my progress
                </Button>
              </Link>
              <Link to="/login">
                <Button variant="ghost" size="md" block icon={<ArrowLeft className="h-4 w-4" />}>
                  Back to sign in
                </Button>
              </Link>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
