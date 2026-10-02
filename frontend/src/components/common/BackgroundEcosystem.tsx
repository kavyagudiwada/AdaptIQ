export default function BackgroundEcosystem() {
  return (
    <div
      id="adaptive-ecosystem"
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 -z-10 overflow-hidden"
    >
      <div className="absolute inset-0 bg-gradient-to-b from-[#04060f] via-[#0a1230] to-[#04060f]" />

      <div className="absolute -left-40 -top-48 h-[46rem] w-[46rem] rounded-full bg-cyan-400/[0.05] blur-[130px]" />
      <div className="absolute -right-52 -top-40 h-[44rem] w-[44rem] rounded-full bg-indigo-500/[0.12] blur-[140px]" />
      <div className="absolute bottom-[-20rem] left-[34%] h-[42rem] w-[42rem] rounded-full bg-violet-600/[0.08] blur-[150px]" />
      <div className="absolute left-[18%] top-[45%] h-[32rem] w-[32rem] rounded-full bg-blue-500/[0.08] blur-[130px]" />
      <div className="absolute right-[8%] top-[68%] h-[26rem] w-[26rem] rounded-full bg-cyan-300/[0.04] blur-[120px]" />
    </div>
  );
}