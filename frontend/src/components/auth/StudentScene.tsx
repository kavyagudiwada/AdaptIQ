import { cn } from "@/utils/cn";

type Pose = "neutral" | "wave" | "point" | "cheer";

/**
 * One student, drawn in its own 0..70 x 0..130 space so the scene can place
 * each figure with a simple translate/scale.
 *
 * Flat vector shapes with a lighter top edge and a darker base on each form,
 * which is what gives the group a soft 3D-cartoon read without any licensed
 * artwork.
 */
function Student({
  skin,
  hair,
  hairStyle,
  top,
  bottom,
  shoe,
  bag,
  pose,
  flip = false,
}: {
  skin: string;
  hair: string;
  hairStyle: 0 | 1 | 2 | 3;
  top: string;
  bottom: string;
  shoe: string;
  bag: string;
  pose: Pose;
  flip?: boolean;
}) {
  return (
    <g transform={flip ? "translate(70,0) scale(-1,1)" : undefined} data-student="">
      {/* Backpack sits behind the torso */}
      <rect x="20" y="62" width="30" height="34" rx="11" fill={bag} />
      <rect x="20" y="62" width="30" height="12" rx="6" fill="#000" opacity="0.07" />

      {/* Legs and shoes */}
      <rect x="25" y="88" width="8" height="26" rx="4" fill={bottom} />
      <rect x="37" y="88" width="8" height="26" rx="4" fill={bottom} />
      <rect x="21" y="112" width="14" height="8" rx="4" fill={shoe} />
      <rect x="35" y="112" width="14" height="8" rx="4" fill={shoe} />

      {/* Torso */}
      <rect x="19" y="56" width="32" height="36" rx="13" fill={top} />
      <rect x="19" y="56" width="32" height="11" rx="5.5" fill="#fff" opacity="0.14" />

      {/* Arms */}
      {pose === "wave" || pose === "cheer" ? (
        <rect
          x="49"
          y="24"
          width="8"
          height="30"
          rx="4"
          fill={top}
          transform="rotate(30 53 54)"
        />
      ) : null}
      {pose === "point" ? (
        <rect
          x="48"
          y="20"
          width="8"
          height="30"
          rx="4"
          fill={top}
          transform="rotate(58 52 50)"
        />
      ) : null}
      <rect x="13" y="58" width="8" height="30" rx="4" fill={top} />
      <circle cx="17" cy="90" r="5" fill={skin} />
      {pose === "wave" || pose === "cheer" ? (
        <circle cx="63" cy="26" r="5" fill={skin} />
      ) : null}
      {pose === "point" ? <circle cx="66" cy="20" r="5" fill={skin} /> : null}

      {/* Neck and head */}
      <rect x="30" y="48" width="10" height="10" rx="4" fill={skin} />
      <circle cx="35" cy="34" r="16" fill={skin} />

      {/* Hair variants */}
      {hairStyle === 0 ? (
        <path d="M19 32a16 16 0 0 1 32 0c-1-9-7-13-16-13s-15 4-16 13z" fill={hair} />
      ) : null}
      {hairStyle === 1 ? (
        <>
          <path d="M19 30a16 16 0 0 1 32 0c0-11-7-14-16-14s-16 3-16 14z" fill={hair} />
          <circle cx="19" cy="40" r="7" fill={hair} />
          <circle cx="51" cy="40" r="7" fill={hair} />
        </>
      ) : null}
      {hairStyle === 2 ? (
        <path d="M19 33a16 16 0 0 1 32 0c1-6 0-16-16-16s-17 10-16 16z" fill={hair} />
      ) : null}
      {hairStyle === 3 ? (
        <>
          <path d="M19 32a16 16 0 0 1 32 0c0-10-6-13-16-13s-16 3-16 13z" fill={hair} />
          <path d="M47 22c6 2 8 8 6 14 3-8 1-16-6-19z" fill={hair} />
        </>
      ) : null}

      {/* Face */}
      <circle cx="29" cy="35" r="2" fill="#171a21" />
      <circle cx="41" cy="35" r="2" fill="#171a21" />
      <path
        d="M30 41q5 4 10 0"
        stroke="#171a21"
        strokeWidth="1.8"
        strokeLinecap="round"
        fill="none"
      />
      <circle cx="24" cy="39" r="2.6" fill="#f472b6" opacity="0.3" />
      <circle cx="46" cy="39" r="2.6" fill="#f472b6" opacity="0.3" />
    </g>
  );
}

/**
 * Hero illustration: a diverse group of seven students, selfie-style, with a
 * couple pointing upward. Entirely original vector art.
 */
export function StudentScene({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 720 470"
      className={cn("w-full", className)}
      role="img"
      aria-label="Illustration of a diverse group of seven students learning together"
    >
      <defs>
        <linearGradient id="aiq-blob" x1="0" y1="0" x2="0.6" y2="1">
          <stop offset="0%" stopColor="#ffffff" stopOpacity="0.9" />
          <stop offset="100%" stopColor="#d9f0ff" stopOpacity="0.55" />
        </linearGradient>
        <clipPath id="aiq-blob-clip">
          <path d="M360 34c96 0 186 44 232 116 46 72 34 168-30 224-64 56-176 62-262 40-86-22-172-84-186-166-14-82 30-160 106-192C282 26 320 34 360 34Z" />
        </clipPath>
      </defs>

      {/* Soft blob backdrop */}
      <path
        d="M360 34c96 0 186 44 232 116 46 72 34 168-30 224-64 56-176 62-262 40-86-22-172-84-186-166-14-82 30-160 106-192C282 26 320 34 360 34Z"
        fill="url(#aiq-blob)"
      />

      {/* Floating decorative dots and sparks, clipped to the blob */}
      <g clipPath="url(#aiq-blob-clip)">
        <circle cx="150" cy="120" r="7" fill="#8b5cf6" opacity="0.35" />
        <circle cx="590" cy="150" r="10" fill="#3366ff" opacity="0.22" />
        <circle cx="120" cy="330" r="5" fill="#10b981" opacity="0.4" />
        <circle cx="620" cy="330" r="6" fill="#f59e0b" opacity="0.4" />
        <path d="M96 208l4.5 12L112 224l-11.5 4L96 240l-4.5-12L80 224l11.5-4z" fill="#fbbf24" opacity="0.75" />
        <path d="M636 92l3.6 9.4 9.4 3.6-9.4 3.6-3.6 9.4-3.6-9.4-9.4-3.6 9.4-3.6z" fill="#8b5cf6" opacity="0.6" />
        <path d="M556 396l3 8 8 3-8 3-3 8-3-8-8-3 8-3z" fill="#3366ff" opacity="0.4" />

        {/* Back row: smaller, further away */}
        <g transform="translate(150 128) scale(0.78)">
          <Student
            skin="#8d5a3b"
            hair="#241a14"
            hairStyle={1}
            top="#8b5cf6"
            bottom="#1f2937"
            shoe="#171a21"
            bag="#0ea5e9"
            pose="point"
            flip
          />
        </g>
        <g transform="translate(268 116) scale(0.8)">
          <Student
            skin="#f3d0b0"
            hair="#a9714b"
            hairStyle={0}
            top="#10b981"
            bottom="#374151"
            shoe="#0f172a"
            bag="#f59e0b"
            pose="wave"
          />
        </g>
        <g transform="translate(400 122) scale(0.78)">
          <Student
            skin="#c98d63"
            hair="#2f2a26"
            hairStyle={2}
            top="#f59e0b"
            bottom="#1f2937"
            shoe="#171a21"
            bag="#ef4444"
            pose="neutral"
          />
        </g>
        <g transform="translate(516 130) scale(0.8)">
          <Student
            skin="#7a4a2b"
            hair="#1f2937"
            hairStyle={3}
            top="#0ea5e9"
            bottom="#4b5563"
            shoe="#171a21"
            bag="#8b5cf6"
            pose="cheer"
            flip
          />
        </g>

        {/* Front row: larger, overlapping the back row */}
        <g transform="translate(196 214) scale(1.02)">
          <Student
            skin="#e8b58c"
            hair="#3a2a20"
            hairStyle={0}
            top="#ef4444"
            bottom="#1f2937"
            shoe="#171a21"
            bag="#3366ff"
            pose="neutral"
          />
        </g>
        <g transform="translate(330 236) scale(1.14)">
          <Student
            skin="#f6d3b4"
            hair="#7c4a21"
            hairStyle={1}
            top="#3366ff"
            bottom="#0f172a"
            shoe="#171a21"
            bag="#fbbf24"
            pose="point"
          />
        </g>
        <g transform="translate(470 218) scale(1.04)">
          <Student
            skin="#a9714b"
            hair="#111827"
            hairStyle={3}
            top="#ec4899"
            bottom="#374151"
            shoe="#0f172a"
            bag="#10b981"
            pose="wave"
            flip
          />
        </g>
      </g>

      {/* Shared ground shadow ties the group together */}
      <ellipse cx="360" cy="452" rx="250" ry="14" fill="#0f172a" opacity="0.07" />
    </svg>
  );
}
