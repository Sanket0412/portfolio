import { NextRequest } from "next/server";

const API_URL = process.env.PORTFOLIO_API_URL ?? "http://localhost:8000";
const INTERNAL_KEY = process.env.INTERNAL_API_KEY ?? "";

const SSE_HEADERS = {
  "Content-Type": "text/event-stream",
  "Cache-Control": "no-cache",
  Connection: "keep-alive",
};

function sseError(message: string): Response {
  return new Response(
    `event: error\ndata: ${JSON.stringify({ message })}\n\nevent: done\ndata: "[DONE]"\n\n`,
    { status: 200, headers: SSE_HEADERS }
  );
}

export async function POST(req: NextRequest) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: "invalid JSON" }), { status: 400 });
  }

  let upstream: Response;
  try {
    upstream = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Forward the visitor IP so the backend rate limits per visitor, not per BFF.
        "X-Forwarded-For": req.headers.get("x-forwarded-for") ?? "",
        ...(INTERNAL_KEY ? { "X-Internal-Key": INTERNAL_KEY } : {}),
      },
      body: JSON.stringify(body),
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : "upstream unreachable";
    return sseError(msg);
  }

  if (upstream.status === 429) {
    return sseError("You're sending messages too quickly. Please wait a moment and try again.");
  }

  if (!upstream.ok || !upstream.body) {
    return sseError(`backend returned ${upstream.status}`);
  }

  return new Response(upstream.body, {
    status: 200,
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
      "X-Accel-Buffering": "no",
    },
  });
}
