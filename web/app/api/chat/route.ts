import { NextRequest } from "next/server";

const API_URL = process.env.PORTFOLIO_API_URL ?? "http://localhost:8000";

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
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : "upstream unreachable";
    return new Response(
      `event: error\ndata: ${JSON.stringify({ message: msg })}\n\nevent: done\ndata: "[DONE]"\n\n`,
      {
        status: 200,
        headers: {
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          Connection: "keep-alive",
        },
      }
    );
  }

  if (!upstream.ok || !upstream.body) {
    const errMsg = `backend returned ${upstream.status}`;
    return new Response(
      `event: error\ndata: ${JSON.stringify({ message: errMsg })}\n\nevent: done\ndata: "[DONE]"\n\n`,
      {
        status: 200,
        headers: {
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          Connection: "keep-alive",
        },
      }
    );
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
