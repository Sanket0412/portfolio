export default function Footer() {
  return (
    <footer className="border-t border-zinc-800 mt-16 py-8 text-center text-zinc-500 text-sm">
      <div className="mx-auto max-w-6xl px-6">
        <p>
          &copy; {new Date().getFullYear()} Sanket J Shah | Built with Next.js &amp; FastAPI
        </p>
        <p className="mt-1 text-zinc-600">
          <a
            href="https://github.com/Sanket0412/Portfolio"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-zinc-400 transition-colors"
          >
            View source
          </a>
          {" · "}
          <a
            href="https://www.linkedin.com/in/sanketjshah/"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-zinc-400 transition-colors"
          >
            LinkedIn
          </a>
          {" · "}
          <a
            href="https://github.com/Sanket0412"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-zinc-400 transition-colors"
          >
            GitHub
          </a>
        </p>
      </div>
    </footer>
  );
}
