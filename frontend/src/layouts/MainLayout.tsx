import { useEffect, useRef, useState } from "react";
import { Link, NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import {
  ClipboardCheck,
  LayoutDashboard,
  LogOut,
  Map,
  Menu,
  Sparkles,
  Target,
  TrendingUp,
  UserRound,
  X,
} from "lucide-react";
import { cn } from "@/utils/cn";
import { NAV_ITEMS } from "@/data/options";
import { useLearner } from "@/hooks/useLearner";
import { useAuth } from "@/hooks/useAuth";
import { Badge } from "@/components/common/Badge";
import { Logo } from "@/components/common/Logo";

const ICONS = {
  LayoutDashboard,
  ClipboardCheck,
  Map,
  Sparkles,
  Target,
  TrendingUp,
} as const;

const MOBILE_NAV = [
  { to: "/dashboard", label: "Home", icon: LayoutDashboard },
  { to: "/assessment", label: "Assess", icon: ClipboardCheck },
  { to: "/roadmap", label: "Roadmap", icon: Map },
  { to: "/tutor", label: "Tutor", icon: Sparkles },
  { to: "/quiz", label: "Practice", icon: Target },
  { to: "/progress", label: "Progress", icon: TrendingUp },
];

export default function MainLayout() {
  const { learner, healthError } = useLearner();
  const { session, signOut } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [accountOpen, setAccountOpen] = useState(false);
  const accountRef = useRef<HTMLDivElement>(null);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    setAccountOpen(false);
  }, [location.pathname]);

  // Close the account menu on an outside click or Escape.
  useEffect(() => {
    if (!accountOpen) return;

    function onPointerDown(event: MouseEvent) {
      if (!accountRef.current?.contains(event.target as Node)) setAccountOpen(false);
    }
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") setAccountOpen(false);
    }

    document.addEventListener("mousedown", onPointerDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("mousedown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [accountOpen]);

  function handleSignOut() {
    signOut();
    setAccountOpen(false);
    navigate("/", { replace: true });
  }

  return (
    <div className="relative flex min-h-screen flex-col overflow-hidden bg-transparent">
      {/* Top bar */}
      <header className="sticky top-0 z-30 border-b border-white/10 bg-[#04060f]/55 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-7xl items-center gap-4 px-4 sm:px-6">
          <Logo to="/" light iconClassName="shadow-sm" />

          {/* Desktop nav */}
          <nav className="ml-4 hidden flex-1 items-center gap-1 lg:flex">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-white/10 text-cyan-200"
                      : "text-ink-400 hover:bg-white/10 hover:text-white",
                  )
                }
              >
                {({ isActive }) => (
                  <>
                    {(() => {
                      const Icon = ICONS[item.icon as keyof typeof ICONS];
                      return <Icon className={cn("h-4 w-4", isActive && "text-cyan-300")} />;
                    })()}
                    {item.label}
                  </>
                )}
              </NavLink>
            ))}
          </nav>

          <div className="ml-auto flex items-center gap-3">
            {healthError ? (
              <Badge tone="danger" className="hidden sm:inline-flex">
                API offline
              </Badge>
            ) : null}

            {learner ? (
              <div className="hidden items-center gap-2.5 rounded-xl bg-white/10 py-1.5 pl-2.5 pr-3 ring-1 ring-white/15 sm:flex">
                <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-cyan-400/25 text-xs font-bold text-cyan-100">
                  {learner.name.charAt(0).toUpperCase()}
                </span>
                <div className="leading-tight">
                  <p className="text-xs font-semibold text-white">{learner.name}</p>
                  <p className="text-[10px] text-cyan-100/70">{learner.topic}</p>
                </div>
              </div>
            ) : (
              <Link
                to="/profile"
                className="hidden h-9 items-center rounded-xl bg-cyan-400/15 px-4 text-sm font-medium text-cyan-100 ring-1 ring-inset ring-cyan-300/25 transition hover:bg-cyan-400/25 sm:inline-flex"
              >
                Start learning
              </Link>
            )}

            {session ? (
              /* Account menu: only shown once someone is actually signed in. */
              <div className="relative" ref={accountRef}>
                <button
                  type="button"
                  onClick={() => setAccountOpen((v) => !v)}
                  aria-expanded={accountOpen}
                  aria-haspopup="menu"
                  className="inline-flex h-9 items-center gap-1.5 rounded-xl bg-white/10 px-2.5 text-sm font-medium text-ink-200 ring-1 ring-white/15 transition hover:bg-white/15 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400"
                >
                  <span className="flex h-6 w-6 items-center justify-center rounded-lg bg-cyan-400/25 text-[11px] font-bold text-cyan-100">
                    {session.user.name.charAt(0).toUpperCase()}
                  </span>
                  <span className="hidden max-w-[9rem] truncate sm:inline">
                    {session.user.name}
                  </span>
                </button>

                {accountOpen ? (
                  <div
                    role="menu"
                    className="absolute right-0 top-11 z-40 w-60 animate-slide-up overflow-hidden rounded-2xl border border-ink-200 bg-white shadow-lg"
                  >
                    <div className="border-b border-ink-100 px-4 py-3">
                      <p className="truncate text-sm font-semibold text-ink-900">
                        {session.user.name}
                      </p>
                      <p className="truncate text-xs text-ink-500">
                        {session.user.email}
                      </p>
                      {session.learner ? (
                        <p className="mt-1.5 text-[11px] text-ink-400">
                          Linked to learner #{session.learner.id}
                        </p>
                      ) : (
                        <p className="mt-1.5 text-[11px] text-amber-600">
                          No learner profile linked yet
                        </p>
                      )}
                    </div>
                    <Link
                      to="/profile"
                      role="menuitem"
                      className="flex items-center gap-2.5 px-4 py-2.5 text-sm text-ink-700 transition hover:bg-ink-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-brand-500"
                    >
                      <UserRound className="h-4 w-4 text-ink-400" aria-hidden />
                      {session.learner ? "Edit learner profile" : "Create learner profile"}
                    </Link>
                    <button
                      type="button"
                      role="menuitem"
                      onClick={handleSignOut}
                      className="flex w-full items-center gap-2.5 border-t border-ink-100 px-4 py-2.5 text-left text-sm font-medium text-rose-600 transition hover:bg-rose-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-brand-500"
                    >
                      <LogOut className="h-4 w-4" aria-hidden />
                      Sign out
                    </button>
                  </div>
                ) : null}
              </div>
            ) : null}

            <button
              type="button"
              onClick={() => setMenuOpen((v) => !v)}
              className="inline-flex h-9 w-9 items-center justify-center rounded-lg text-ink-200 ring-1 ring-white/15 transition hover:bg-white/10 lg:hidden"
              aria-label={menuOpen ? "Close menu" : "Open menu"}
            >
              {menuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>

        {/* Mobile dropdown */}
        {menuOpen ? (
          <nav className="border-t border-white/10 bg-[#0a1026]/95 px-4 py-2 backdrop-blur lg:hidden">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-white/10 text-cyan-200"
                      : "text-ink-400 hover:bg-white/10 hover:text-white",
                  )
                }
              >
                {(() => {
                  const Icon = ICONS[item.icon as keyof typeof ICONS];
                  return <Icon className="h-4 w-4" />;
                })()}
                {item.label}
              </NavLink>
            ))}
          </nav>
        ) : null}
      </header>

      <main className="relative z-10 mx-auto w-full max-w-7xl flex-1 px-4 py-6 sm:px-6 sm:py-8">
        <Outlet />
      </main>

      {/* Mobile bottom tab bar */}
      <nav className="sticky bottom-0 z-20 border-t border-white/10 bg-[#060a1c]/90 backdrop-blur lg:hidden">
        <div className="grid grid-cols-6">
          {MOBILE_NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                cn(
                  "flex flex-col items-center gap-0.5 py-2.5 text-[10px] font-medium transition-colors",
                  isActive ? "text-cyan-300" : "text-ink-300",
                )
              }
            >
              <item.icon className="h-5 w-5" />
              {item.label}
            </NavLink>
          ))}
        </div>
      </nav>
    </div>
  );
}
