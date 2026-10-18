import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import PageShell from "@/components/PageShell";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: "Sanket J Shah | Data Scientist & ML Engineer",
  description:
    "Portfolio of Sanket J Shah: Data Scientist, ML Engineer, and GenAI specialist. Explore projects, publications, work experience, and chat with an AI version of Sanket.",
  openGraph: {
    title: "Sanket J Shah | Data Scientist & ML Engineer",
    description:
      "Data Scientist and ML Engineer specializing in GenAI, RAG, and production ML systems.",
    type: "website",
    url: "/",
    siteName: "Sanket J Shah",
  },
  twitter: { card: "summary" },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} antialiased`}
    >
      <body className="min-h-screen flex flex-col bg-zinc-950 text-zinc-50">
        <Navbar />
        <PageShell>{children}</PageShell>
      </body>
    </html>
  );
}
