import Image from "next/image";
import Link from "next/link";
import AnimatedSection from "@/components/AnimatedSection";

const HIGHLIGHTS = [
  {
    title: "Agentic Portfolio Chat",
    desc: "LangGraph ReAct agent with tool-calling, and recruiter job-fit mode.",
    href: "/chat",
    cta: "Try it",
  },
  {
    title: "Weighted Hybrid RecSys",
    desc: "SVD + cosine similarity. Published in Springer CCIS vol 1572.",
    href: "/publications",
    cta: "Read paper",
  },
  {
    title: "Video Summarization",
    desc: "Key frame extraction + TensorFlow caption generation from uploaded video.",
    href: "/projects",
    cta: "View project",
  },
];

export default function HomePage() {
  return (
    <div className="mx-auto max-w-6xl px-6 py-16">
      {/* Hero */}
      <AnimatedSection className="grid grid-cols-1 lg:grid-cols-[1.6fr_1fr] gap-12 items-start">
        {/* Left */}
        <div>
          <p className="text-blue-400 text-sm font-medium tracking-wide uppercase mb-3">
            Data Scientist &amp; ML Engineer
          </p>
          <h1 className="text-5xl font-bold text-zinc-50 leading-tight mb-4">
            Hi, I&apos;m Sanket Shah
          </h1>
          <p className="text-zinc-400 text-lg leading-relaxed mb-8 max-w-xl">
            I build end-to-end data and ML systems that power personalization, audience insights,
            and agentic AI workflows. This site showcases selected projects, publications, and a
            live chat backed by retrieval over my work.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/projects"
              className="px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium transition-colors"
            >
              View Projects
            </Link>
            <Link
              href="/chat"
              className="px-5 py-2.5 rounded-lg border border-zinc-700 hover:border-zinc-500 hover:bg-zinc-800/60 text-zinc-300 text-sm font-medium transition-colors"
            >
              Chat with Sanket
            </Link>
            <Link
              href="/publications"
              className="px-5 py-2.5 rounded-lg border border-zinc-700 hover:border-zinc-500 hover:bg-zinc-800/60 text-zinc-300 text-sm font-medium transition-colors"
            >
              Publications
            </Link>
            <Link
              href="/experience"
              className="px-5 py-2.5 rounded-lg border border-zinc-700 hover:border-zinc-500 hover:bg-zinc-800/60 text-zinc-300 text-sm font-medium transition-colors"
            >
              Experience
            </Link>
          </div>
        </div>

        {/* Right — Education */}
        <AnimatedSection delay={0.1}>
          <h2 className="text-zinc-400 text-xs uppercase tracking-widest font-semibold mb-4">
            Education
          </h2>
          <div className="space-y-3">
            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4 flex items-center gap-4">
              <Image
                src="/logos/stevens_logo.png"
                alt="Stevens Institute of Technology"
                width={56}
                height={56}
                className="object-contain"
              />
              <div>
                <p className="text-zinc-50 font-medium text-sm">
                  M.S. Computer Science
                </p>
                <p className="text-zinc-400 text-xs">Stevens Institute of Technology, Hoboken NJ</p>
                <p className="text-zinc-500 text-xs">Graduated January 2024</p>
              </div>
            </div>
            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4 flex items-center gap-4">
              <Image
                src="/logos/ahduni_logo.png"
                alt="Ahmedabad University"
                width={56}
                height={56}
                className="object-contain"
              />
              <div>
                <p className="text-zinc-50 font-medium text-sm">
                  B.Tech, Information and Communication Technology
                </p>
                <p className="text-zinc-400 text-xs">Ahmedabad University, India</p>
                <p className="text-zinc-500 text-xs">Graduated May 2022</p>
              </div>
            </div>
          </div>
        </AnimatedSection>
      </AnimatedSection>

      {/* Divider */}
      <AnimatedSection delay={0.2} className="border-t border-zinc-800 my-16">{null}</AnimatedSection>

      {/* Highlights */}
      <AnimatedSection delay={0.25}>
        <h2 className="text-zinc-400 text-xs uppercase tracking-widest font-semibold mb-6">
          Highlights
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {HIGHLIGHTS.map((h) => (
            <div
              key={h.title}
              className="rounded-xl border border-zinc-800 bg-zinc-900 p-5 flex flex-col gap-3 hover:border-zinc-600 transition-colors"
            >
              <p className="text-zinc-50 font-semibold text-sm">{h.title}</p>
              <p className="text-zinc-400 text-sm flex-1">{h.desc}</p>
              <Link
                href={h.href}
                className="text-blue-400 text-sm hover:text-blue-300 transition-colors inline-flex items-center gap-1"
              >
                {h.cta} <span aria-hidden>&#8594;</span>
              </Link>
            </div>
          ))}
        </div>
      </AnimatedSection>
    </div>
  );
}
