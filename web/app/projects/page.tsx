"use client";

import Image from "next/image";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Tag from "@/components/Tag";
import AnimatedSection from "@/components/AnimatedSection";
import { PROJECTS, Project } from "@/data/projects";

function ProjectModal({ project, onClose }: { project: Project; onClose: () => void }) {
  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 16 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 16 }}
          transition={{ duration: 0.2 }}
          className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl border border-zinc-700 bg-zinc-950 shadow-2xl"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Cover */}
          {project.image && (
            <div className="h-48 overflow-hidden rounded-t-2xl bg-zinc-800">
              <Image
                src={project.image}
                alt={project.title}
                width={800}
                height={192}
                className="w-full h-full object-cover"
                unoptimized={project.image.startsWith("http")}
              />
            </div>
          )}

          <div className="p-6">
            {/* Close */}
            <button
              onClick={onClose}
              className="absolute top-4 right-4 p-1.5 rounded-full bg-zinc-800 hover:bg-zinc-700 text-zinc-400 hover:text-zinc-50 transition-colors"
              aria-label="Close"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            <h2 className="text-xl font-bold text-zinc-50 mb-2 pr-8">{project.title}</h2>

            {/* Links */}
            {Object.entries(project.links).length > 0 && (
              <div className="flex flex-wrap gap-2 mb-4">
                {Object.entries(project.links).map(([label, url]) => (
                  <a
                    key={label}
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3 py-1 text-xs rounded-lg border border-zinc-700 bg-zinc-900 text-zinc-300 hover:text-blue-400 hover:border-blue-800 transition-colors"
                  >
                    {label} &#8599;
                  </a>
                ))}
              </div>
            )}

            {/* Description */}
            <div className="text-zinc-300 text-sm leading-relaxed mb-5 prose-content">
              {project.description
                .trim()
                .split("\n")
                .map((line, i) => {
                  if (line.startsWith("## "))
                    return <h3 key={i} className="text-zinc-50 font-semibold mt-4 mb-1">{line.slice(3)}</h3>;
                  if (line.startsWith("- "))
                    return <li key={i} className="ml-4 list-disc">{line.slice(2).replace(/\*\*(.+?)\*\*/g, "$1")}</li>;
                  if (line.trim() === "") return <br key={i} />;
                  return (
                    <p key={i} dangerouslySetInnerHTML={{
                      __html: line.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
                    }} />
                  );
                })}
            </div>

            {/* Tech */}
            {project.tech.length > 0 && (
              <div className="mb-4">
                <p className="text-zinc-500 text-xs uppercase tracking-wide mb-2">Tech Stack</p>
                <div className="flex flex-wrap gap-1.5">
                  {project.tech.map((t) => (
                    <span key={t} className="px-2.5 py-0.5 text-xs rounded-full bg-blue-950/50 border border-blue-900/60 text-blue-300">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Tags */}
            {project.tags.length > 0 && (
              <div className="flex flex-wrap gap-1.5">
                {project.tags.map((tag) => (
                  <Tag key={tag} label={tag} />
                ))}
              </div>
            )}
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

function ProjectCard({ project, onClick }: { project: Project; onClick: () => void }) {
  return (
    <motion.div
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
      className="rounded-xl border border-zinc-800 bg-zinc-900 overflow-hidden cursor-pointer hover:border-zinc-600 transition-colors flex flex-col"
      onClick={onClick}
    >
      {/* Cover */}
      <div className="h-44 bg-zinc-800 overflow-hidden">
        <Image
          src={project.image}
          alt={project.title}
          width={600}
          height={176}
          className="w-full h-full object-cover"
          unoptimized={project.image.startsWith("http")}
        />
      </div>

      <div className="p-5 flex flex-col flex-1 gap-3">
        <h2 className="text-zinc-50 font-semibold text-base leading-snug">{project.title}</h2>
        <p className="text-zinc-400 text-sm leading-relaxed flex-1 line-clamp-3">
          {project.summary}
        </p>
        <div className="flex flex-wrap gap-1.5">
          {project.tags.slice(0, 4).map((tag) => (
            <Tag key={tag} label={tag} />
          ))}
          {project.tags.length > 4 && (
            <span className="text-zinc-500 text-xs self-center">+{project.tags.length - 4}</span>
          )}
        </div>
        <button className="mt-1 text-sm text-blue-400 hover:text-blue-300 text-left transition-colors">
          View details &#8594;
        </button>
      </div>
    </motion.div>
  );
}

export default function ProjectsPage() {
  const [selected, setSelected] = useState<Project | null>(null);

  return (
    <div className="mx-auto max-w-6xl px-6 py-16">
      <AnimatedSection>
        <h1 className="text-4xl font-bold text-zinc-50 mb-2">Projects</h1>
        <p className="text-zinc-400 mb-10">Click any card to read the full description</p>
      </AnimatedSection>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {PROJECTS.map((project, i) => (
          <AnimatedSection key={project.slug} delay={i * 0.07}>
            <ProjectCard project={project} onClick={() => setSelected(project)} />
          </AnimatedSection>
        ))}
      </div>

      {selected && (
        <ProjectModal project={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
