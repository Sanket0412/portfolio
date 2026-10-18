import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Projects | Sanket J Shah",
  description:
    "Selected projects by Sanket J Shah: ASL recognition, video summarization, TodaySponsor, and the CloneAMA agent.",
};

export default function ProjectsLayout({ children }: { children: React.ReactNode }) {
  return children;
}
