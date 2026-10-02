const PARTICLES = [
  { top: "12%", left: "5%", size: 3, delay: "0s", drift: -60, driftX: 14 },
  { top: "22%", left: "9%", size: 2, delay: "2.5s", drift: -90, driftX: -10 },
  { top: "40%", left: "3%", size: 4, delay: "5s", drift: -70, driftX: 6 },
  { top: "64%", left: "7%", size: 2, delay: "1.4s", drift: -110, driftX: -12 },
  { top: "80%", left: "11%", size: 3, delay: "6.5s", drift: -80, driftX: 20 },
  { top: "30%", left: "26%", size: 2, delay: "3.6s", drift: -130, driftX: -18 },
  { top: "70%", left: "23%", size: 3, delay: "8s", drift: -95, driftX: 10 },
  { top: "52%", left: "31%", size: 2, delay: "10s", drift: -60, driftX: 8 },
  { top: "18%", left: "40%", size: 3, delay: "7.2s", drift: -100, driftX: -6 },
  { top: "78%", left: "38%", size: 2, delay: "4s", drift: -120, driftX: 16 },
  { top: "26%", left: "55%", size: 2, delay: "9s", drift: -70, driftX: -14 },
  { top: "60%", left: "52%", size: 3, delay: "2s", drift: -140, driftX: 12 },
  { top: "14%", left: "63%", size: 2, delay: "5.6s", drift: -85, driftX: 6 },
  { top: "72%", left: "60%", size: 3, delay: "7.8s", drift: -110, driftX: -20 },
  { top: "22%", left: "73%", size: 2, delay: "0.8s", drift: -96, driftX: 10 },
  { top: "48%", left: "71%", size: 3, delay: "9.4s", drift: -70, driftX: -8 },
  { top: "84%", left: "68%", size: 2, delay: "3s", drift: -120, driftX: 18 },
  { top: "58%", left: "80%", size: 2, delay: "6.1s", drift: -100, driftX: -12 },
  { top: "30%", left: "86%", size: 3, delay: "11s", drift: -80, driftX: 8 },
  { top: "76%", left: "90%", size: 2, delay: "1.9s", drift: -90, driftX: -16 },
  { top: "44%", left: "94%", size: 3, delay: "8.6s", drift: -110, driftX: 10 },
  { top: "20%", left: "96%", size: 2, delay: "4.7s", drift: -70, driftX: -6 },
];

const STREAMS = [
  "M 300 -20 C 260 180, 360 320, 320 500 C 300 620, 360 760, 330 920",
  "M 60 -20 C 30 200, 140 380, 110 560 C 90 700, 150 820, 130 920",
];

export default function BackgroundEcosystem() {
  return (
    <div
      id="adaptive-ecosystem"
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 -z-10 overflow-hidden"
    >
      <div className="absolute inset-0 bg-[linear-gradient(180deg,#04060f_0%,#08102b_30%,#101a4d_58%,#0b1233_80%,#04060f_100%)]" />

      <div className="absolute -left-40 -top-48 h-[46rem] w-[46rem] rounded-full bg-cyan-400/[0.06] blur-[130px]" />
      <div className="absolute -right-52 -top-40 h-[44rem] w-[44rem] rounded-full bg-indigo-500/[0.14] blur-[140px]" />
      <div className="absolute bottom-[-20rem] left-[34%] h-[42rem] w-[42rem] rounded-full bg-violet-600/[0.10] blur-[150px]" />
      <div className="absolute left-[18%] top-[45%] h-[32rem] w-[32rem] rounded-full bg-blue-500/[0.10] blur-[130px]" />
      <div className="absolute right-[8%] top-[68%] h-[26rem] w-[26rem] rounded-full bg-cyan-300/[0.05] blur-[120px]" />

      <div className="absolute inset-0 opacity-30 [background-image:linear-gradient(to_right,rgba(140,190,255,0.05)_1px,transparent_1px),linear-gradient(to_bottom,rgba(140,190,255,0.05)_1px,transparent_1px)] [background-size:64px_64px] [mask-image:radial-gradient(65%_55%_at_50%_18%,black,transparent_82%)]" />

      <svg
        className="absolute inset-0 h-full w-full"
        viewBox="0 0 1440 900"
        fill="none"
        preserveAspectRatio="xMidYMid slice"
      >
        <defs>
          <linearGradient id="ecosystem-link" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#22d3ee" stopOpacity="0.5" />
            <stop offset="100%" stopColor="#818cf8" stopOpacity="0.4" />
          </linearGradient>
          <radialGradient id="ecosystem-node" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#bae6fd" />
            <stop offset="100%" stopColor="#22d3ee" stopOpacity="0.15" />
          </radialGradient>
          <radialGradient id="ecosystem-node-violet" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#e0e7ff" />
            <stop offset="100%" stopColor="#818cf8" stopOpacity="0.15" />
          </radialGradient>
          <linearGradient id="ecosystem-arc" x1="0" y1="1" x2="1" y2="0">
            <stop offset="0%" stopColor="#22d3ee" stopOpacity="0.35" />
            <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.12" />
          </linearGradient>
        </defs>

        <g stroke="url(#ecosystem-link)" strokeWidth="1">
          <path d="M90 220 170 140 250 230 330 180" strokeOpacity="0.5" />
          <path d="M90 220 120 360 220 320 250 230" strokeOpacity="0.4" />
          <path d="M250 230 300 300 330 180" strokeOpacity="0.35" />
          <path d="M120 360 300 300" strokeOpacity="0.22" />
          <path d="M170 140 300 300" strokeOpacity="0.18" />
        </g>
        <g stroke="url(#ecosystem-link)" strokeWidth="0.8">
          <path d="M1180 280 1240 210 1300 300 1360 250" strokeOpacity="0.4" />
          <path d="M1180 280 1200 400 1330 380 1300 300" strokeOpacity="0.32" />
          <path d="M1200 400 1180 560 1290 540" strokeOpacity="0.28" />
          <path d="M1330 380 1360 250" strokeOpacity="0.22" />
        </g>
        <g stroke="url(#ecosystem-link)" strokeWidth="0.8">
          <path d="M1080 720 1160 640 1260 700" strokeOpacity="0.3" />
          <path d="M1160 640 1280 760 1260 700 1330 830" strokeOpacity="0.26" />
          <path d="M1080 720 1200 860 1280 760" strokeOpacity="0.2" />
        </g>
        <g stroke="url(#ecosystem-link)" strokeWidth="0.5">
          <path d="M300 500 600 430 900 520" strokeOpacity="0.14" />
          <path d="M900 520 1180 560" strokeOpacity="0.16" />
          <path d="M600 430 760 260" strokeOpacity="0.12" />
        </g>

        <g fill="url(#ecosystem-node)">
          <circle cx="90" cy="220" r="4" />
          <circle cx="170" cy="140" r="3" fill="url(#ecosystem-node-violet)" />
          <circle cx="250" cy="230" r="4.5" />
          <circle cx="330" cy="180" r="3" />
          <circle cx="120" cy="360" r="3.5" fill="url(#ecosystem-node-violet)" />
          <circle cx="220" cy="320" r="2.5" />
          <circle cx="300" cy="300" r="5" fill="url(#ecosystem-node-violet)" />
          <circle cx="1180" cy="280" r="4" />
          <circle cx="1240" cy="210" r="3" fill="url(#ecosystem-node-violet)" />
          <circle cx="1300" cy="300" r="4.5" />
          <circle cx="1360" cy="250" r="2.5" />
          <circle cx="1200" cy="400" r="3.5" />
          <circle cx="1330" cy="380" r="3" />
          <circle cx="1180" cy="560" r="2.5" fill="url(#ecosystem-node-violet)" />
          <circle cx="1290" cy="540" r="3.5" />
          <circle cx="1080" cy="720" r="3" />
          <circle cx="1160" cy="640" r="4" fill="url(#ecosystem-node-violet)" />
          <circle cx="1260" cy="700" r="3.5" />
          <circle cx="1280" cy="760" r="2.5" />
          <circle cx="1200" cy="860" r="3" fill="url(#ecosystem-node-violet)" />
          <circle cx="1330" cy="830" r="4" />
        </g>

        {STREAMS.map((d, i) => (
          <path
            key={`stream-${i}`}
            d={d}
            stroke={i === 0 ? "#22d3ee" : "#6366f1"}
            strokeWidth={i === 0 ? 1.4 : 1}
            strokeDasharray="2 22"
            strokeLinecap="round"
            opacity="0.5"
            className="animate-dash-flow"
          />
        ))}

        <g stroke="url(#ecosystem-arc)" fill="none" strokeWidth="1.2">
          <path d="M880 -30 C 1130 160, 1110 460, 1340 660" />
          <path d="M900 -10 C 1190 240, 1120 520, 1380 700" strokeOpacity="0.6" />
        </g>
        <g stroke="url(#ecosystem-arc)" fill="none" strokeWidth="1">
          <path d="M60 660 C 260 720, 380 640, 480 720" />
          <path d="M-20 880 C 180 800, 360 940, 520 860" strokeOpacity="0.6" />
        </g>
      </svg>

      <div className="absolute inset-x-0 top-1/4 h-[26rem] -translate-y-1/2 rounded-full bg-gradient-to-r from-transparent via-cyan-400/[0.04] to-transparent blur-3xl animate-aurora" />
      <div className="absolute inset-x-0 bottom-[10%] h-72 rounded-full bg-gradient-to-r from-transparent via-indigo-500/[0.05] to-transparent blur-3xl animate-aurora-slow" />

      <div className="absolute left-[12%] top-[16%] h-24 w-24 rounded-full bg-cyan-400/20 blur-2xl animate-float" />
      <div className="absolute right-[14%] top-[58%] h-16 w-16 rounded-full bg-violet-400/15 blur-2xl animate-float [animation-delay:2.4s]" />
      <div className="absolute left-[24%] bottom-[12%] h-20 w-20 rounded-full bg-indigo-500/15 blur-3xl animate-float [animation-delay:1.2s]" />

      {PARTICLES.map((p, i) => (
        <span
          key={`particle-${i}`}
          className="absolute rounded-full bg-cyan-200/70 animate-drift-up"
          style={{
            top: p.top,
            left: p.left,
            width: p.size,
            height: p.size,
            animationDelay: p.delay,
            ["--drift" as string]: p.drift,
            ["--drift-x" as string]: p.driftX,
            boxShadow: "0 0 6px rgba(103,232,249,0.8)",
          }}
        />
      ))}

      <div className="absolute inset-x-0 h-36 bg-gradient-to-b from-cyan-300/[0.05] via-sky-400/[0.06] to-transparent blur-2xl animate-scan" />
    </div>
  );
}