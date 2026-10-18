import type { Metadata } from "next";
import Image from "next/image";
import AnimatedSection from "@/components/AnimatedSection";
import Tag from "@/components/Tag";
import { EXPERIENCES } from "@/data/experience";

export const metadata: Metadata = {
  title: "Experience — Sanket J Shah",
  description: "Professional work history of Sanket J Shah: Data Scientist and ML Engineer.",
};

function markdownToHtml(md: string): string {
  const lines = md.trim().split("\n");
  const out: string[] = [];
  let inList = false;

  for (const raw of lines) {
    const line = raw.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    if (line.startsWith("## ") || line.startsWith("### ")) {
      if (inList) { out.push("</ul>"); inList = false; }
      out.push(`<h3>${line.replace(/^#+\s/, "")}</h3>`);
    } else if (line.startsWith("- ")) {
      if (!inList) { out.push("<ul>"); inList = true; }
      out.push(`<li>${line.slice(2)}</li>`);
    } else if (line.trim() === "") {
      if (inList) { out.push("</ul>"); inList = false; }
    } else {
      if (inList) { out.push("</ul>"); inList = false; }
      out.push(`<p>${line}</p>`);
    }
  }
  if (inList) out.push("</ul>");
  return out.join("\n");
}

export default function ExperiencePage() {
  return (
    <div className="mx-auto max-w-4xl px-6 py-16">
      <AnimatedSection>
        <h1 className="text-4xl font-bold text-zinc-50 mb-2">Experience</h1>
        <p className="text-zinc-400 mb-10">Professional work history and career highlights</p>
      </AnimatedSection>

      <div className="space-y-6">
        {EXPERIENCES.map((exp, i) => (
          <AnimatedSection key={exp.company} delay={i * 0.08}>
            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
              {/* Header */}
              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-5">
                <div className="flex items-center gap-4">
                  {exp.logo && (
                    <div className="shrink-0 w-14 h-14 flex items-center justify-center">
                      <Image
                        src={exp.logo}
                        alt={exp.company}
                        width={56}
                        height={56}
                        className="object-contain"
                      />
                    </div>
                  )}
                  <div>
                    <h2 className="text-2xl font-bold text-zinc-50">{exp.title}</h2>
                    <p className="text-zinc-300 text-sm mt-0.5">
                      {exp.website ? (
                        <a
                          href={exp.website}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="hover:text-blue-400 transition-colors"
                        >
                          <strong>{exp.company}</strong>
                        </a>
                      ) : (
                        <strong>{exp.company}</strong>
                      )}
                      {exp.location && (
                        <span className="text-zinc-500"> &bull; {exp.location}</span>
                      )}
                    </p>
                  </div>
                </div>
                <span className="text-zinc-500 text-sm shrink-0 sm:text-right">{exp.period}</span>
              </div>

              {/* Description */}
              <div
                className="prose-content text-zinc-300 text-sm leading-relaxed mb-5"
                dangerouslySetInnerHTML={{ __html: markdownToHtml(exp.description) }}
              />

              {/* Tags */}
              {exp.tags.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {exp.tags.map((tag) => (
                    <Tag key={tag} label={tag} />
                  ))}
                </div>
              )}
            </div>
          </AnimatedSection>
        ))}
      </div>
    </div>
  );
}
