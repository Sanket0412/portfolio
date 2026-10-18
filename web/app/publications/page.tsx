import type { Metadata } from "next";
import Image from "next/image";
import AnimatedSection from "@/components/AnimatedSection";
import { PUBLICATIONS } from "@/data/publications";

export const metadata: Metadata = {
  title: "Publications — Sanket J Shah",
  description: "Peer-reviewed research publications by Sanket J Shah.",
};

export default function PublicationsPage() {
  return (
    <div className="mx-auto max-w-4xl px-6 py-16">
      <AnimatedSection>
        <h1 className="text-4xl font-bold text-zinc-50 mb-2">Publications</h1>
        <p className="text-zinc-400 mb-10">Peer-reviewed research</p>
      </AnimatedSection>

      <div className="space-y-6">
        {PUBLICATIONS.map((pub, i) => (
          <AnimatedSection key={pub.doi} delay={i * 0.1}>
            <div className="rounded-xl border border-zinc-800 bg-zinc-900 overflow-hidden">
              <div className="flex flex-col md:flex-row">
                {/* Cover */}
                <div className="md:w-48 shrink-0 bg-zinc-800 flex items-center justify-center overflow-hidden">
                  <Image
                    src={pub.cover_image}
                    alt={pub.title}
                    width={192}
                    height={160}
                    className="w-full h-40 md:h-full object-cover"
                  />
                </div>

                {/* Content */}
                <div className="p-6 flex-1">
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <h2 className="text-zinc-50 font-semibold text-base leading-snug">
                      <a
                        href={pub.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="hover:text-blue-400 transition-colors"
                      >
                        {pub.title}
                      </a>
                    </h2>
                    <Image
                      src={pub.venue_logo}
                      alt={pub.publisher}
                      width={60}
                      height={30}
                      className="object-contain shrink-0 opacity-80"
                    />
                  </div>

                  <p className="text-zinc-500 text-xs mb-2">{pub.venue_name}</p>

                  <p className="text-zinc-500 text-xs mb-3">
                    {pub.authors.join(", ")} &bull;{" "}
                    {new Date(pub.date).toLocaleDateString("en-US", {
                      year: "numeric",
                      month: "long",
                    })}
                  </p>

                  <p className="text-zinc-400 text-sm leading-relaxed mb-4 line-clamp-3">
                    {pub.abstract}
                  </p>

                  <div className="flex items-center gap-4">
                    <span className="text-zinc-500 text-xs">
                      {pub.citations} citation{pub.citations !== 1 ? "s" : ""}
                    </span>
                    <a
                      href={pub.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-400 text-xs hover:text-blue-300 transition-colors"
                    >
                      View paper &#8594;
                    </a>
                    <a
                      href={`https://doi.org/${pub.doi}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-zinc-500 text-xs hover:text-zinc-400 transition-colors"
                    >
                      DOI
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </AnimatedSection>
        ))}
      </div>
    </div>
  );
}
