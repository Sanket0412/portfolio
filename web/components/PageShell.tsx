"use client";

import { usePathname } from "next/navigation";
import Footer from "./Footer";

export default function PageShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isChat = pathname === "/chat";

  if (isChat) {
    // Chat is an immersive, full-height view: no footer, and `main` itself
    // is exactly the viewport height so ChatInterface's `h-full` fills the
    // space below the fixed navbar with no page-level scroll.
    return (
      <main className="h-screen overflow-hidden pt-16">{children}</main>
    );
  }

  return (
    <>
      <main className="flex-1 pt-16">{children}</main>
      <Footer />
    </>
  );
}
