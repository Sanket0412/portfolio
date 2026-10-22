export interface Project {
  slug: string;
  title: string;
  summary: string;
  description: string;
  image: string;
  tags: string[];
  tech: string[];
  links: Record<string, string>;
}

export const PROJECTS: Project[] = [
  {
    slug: "cloneama",
    title: "CloneAMA — Agentic Portfolio Chat",
    summary:
      "A production-grade ReAct agent that answers as me, grounded in curated portfolio content with live tool-calling, streaming, and recruiter job-fit analysis.",
    description: `
## What it is
CloneAMA is a LangGraph ReAct agent that impersonates me in a grounded conversation. Recruiters can ask about my work, paste a job description for a fit analysis, or explore my GitHub — all from a single chat interface backed by a persistent Supabase pgvector corpus.

## How it works
- **LangGraph ReAct agent** on Claude Haiku 4.5 with four tools: semantic RAG retrieval, publication lookup (exact citation counts), live GitHub repo search, and job-fit assessment
- **Seeded retrieval** injects context before the first LLM call, cutting time-to-first-token from ~16 s to ~2 s
- **Streaming SSE** endpoint (\`/chat\`) emits token deltas, tool-call/result events, citations, and follow-up suggestions
- **Recruiter job-fit mode**: paste a JD; the agent maps requirements to grounded evidence per requirement and returns a structured fit report with honest gaps
- **Persistent vector store** on Supabase pgvector (60+ chunks from PDFs, Markdown, and vetted Q&A)

## Highlights
- Custom guardrails: rate limiting, prompt-injection blocking, em-dash stripping, secret redaction
- Follow-up suggestion generation (off the critical path, never surfaces excluded topics)
- Content exclusion pipeline: banned topics are stripped at ingest and from live tool output
    `,
    image: "/covers/CloneAMA.png",
    tags: ["LangGraph", "RAG", "LLM", "FastAPI", "Next.js", "Supabase", "pgvector", "Streaming"],
    tech: ["LangGraph", "FastAPI", "Supabase pgvector", "Claude Haiku 4.5", "Next.js", "TypeScript"],
    links: {
      Live: "https://sanketshah.dev/chat",
      Repo: "https://github.com/Sanket0412/Portfolio",
    },
  },
  {
    slug: "todaysponsor",
    title: "TodaySponsor — AI Influencer Matching",
    summary:
      "Personal project: an AI-native platform that matches brands with creators by embedding brand CRM data and creator audience profiles into the same vector space.",
    description: `
## What it is
TodaySponsor is a personal project I designed and built to explore AI-native influencer marketing: matching brands with creators by audience-to-customer overlap rather than follower counts or natural-language briefs.

## How it works
- **Shopify OAuth integration** with HMAC verification, CSRF protection, and scoped CRM access
- **Brand profile computation** from order/customer data: geography, AOV distribution, product category mix, RFM segmentation, gender inference
- **Two-stage matching engine** over 1,555-dimension embeddings (16 structured demographic + 1,536 semantic + 3 behavioral): Stage 1 is a semantic coarse filter, Stage 2 is decomposed cosine similarity across demographics, geography, and content-topic alignment
- **Agentic outreach** draft generation and a streaming campaign agent with persisted conversation history
- Full dashboard with match-score breakdowns and an outreach flow

## Tech
- Frontend: Next.js (App Router) on Vercel
- Backend: FastAPI on Railway, Python 3.11
- Embeddings: OpenAI text-embedding-3-large
- LLMs: GPT-4o-mini for drafts, GPT-4o for the campaign agent
- ML/orchestration: LangChain, LangGraph, Vertex AI
- Integrations: Shopify OAuth, Resend (email)
    `,
    image: "/covers/PortfolioChat.png",
    tags: ["LangGraph", "Embeddings", "FastAPI", "Next.js", "Shopify", "pgvector", "Agentic"],
    tech: ["Next.js", "FastAPI", "Supabase pgvector", "LangGraph", "OpenAI", "Shopify OAuth"],
    links: {
      Live: "https://todaysponsor.dev",
    },
  },
  {
    slug: "echos-asl",
    title: "Echos — Learn and Translate ASL",
    summary:
      "Flutter + Firebase full-stack mobile app for interactive ASL learning, with an ML module for sign translation.",
    description: `
## What it is
Echos is a mobile application designed as one place to learn and translate ASL through interactive tutorials.

## How it works
- Flutter frontend for a smooth mobile UX
- Firebase backend for auth, storage, and app data
- Machine learning module for ASL-related translation capabilities

## Highlights
- Full-stack mobile app architecture (Flutter + Firebase)
- Learning-oriented UX built around interactive tutorials
- ML module integrated into the product experience
    `,
    image: "/covers/ECHOS2.png",
    tags: ["Flutter", "Firebase", "Mobile", "ASL", "Machine Learning"],
    tech: ["Flutter", "Firebase", "Dart", "ML module"],
    links: {
      Repo: "https://github.com/Sanket0412/Echos",
    },
  },
  {
    slug: "video-summarization",
    title: "Video Summarization (Key Frames + Captions)",
    summary:
      "Upload a video and get a compact visual summary: unique key frames and natural-language captions from a TensorFlow captioning model.",
    description: `
## What it is
A video summarization pipeline that takes a user-uploaded video and returns a curated set of unique frames with natural-language captions for each.

## How it works
- React frontend uploads a video and renders returned frames + captions
- Flask backend runs the inference pipeline and serves image outputs
- Captioning uses Beam Search (width 3 by default), configurable from the frontend

## Highlights
- End-to-end flow from upload to summarized outputs
- Key frame selection and caption generation behind a simple UI
- Clear separation of concerns between UI and model serving
    `,
    image: "https://github.com/Sanket0412/Video-Summarization/raw/master/images/default.png",
    tags: ["Computer Vision", "TensorFlow", "Flask", "React", "Beam Search"],
    tech: ["TensorFlow", "Flask", "React", "OpenCV", "CNN features", "Beam Search"],
    links: {
      Repo: "https://github.com/Sanket0412/Video-Summarization",
    },
  },
];
