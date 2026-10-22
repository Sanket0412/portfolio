"use client";

import { useState, useCallback, useRef } from "react";

export interface Citation {
  source: string;
  snippet: string;
  score: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
}

export interface TurnState {
  streaming: boolean;
  streamText: string;
  citations: Citation[];
  suggestions: string[];
  toolActivity: string[];
  error: string | null;
}

const INITIAL_TURN: TurnState = {
  streaming: false,
  streamText: "",
  citations: [],
  suggestions: [],
  toolActivity: [],
  error: null,
};

const STARTER_SUGGESTIONS = [
  "What personal projects have you built?",
  "What's your most impactful ML project?",
  "Tell me about your experience with LLMs and GenAI.",
];

export function useAgentChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [turn, setTurn] = useState<TurnState>(INITIAL_TURN);
  const [suggestions, setSuggestions] = useState<string[]>(STARTER_SUGGESTIONS);
  const sessionId = useRef(crypto.randomUUID());
  const abortRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim() || turn.streaming) return;

      const userMsg: ChatMessage = { role: "user", content: text };
      setMessages((prev) => [...prev, userMsg]);
      setSuggestions([]);
      setTurn({ ...INITIAL_TURN, streaming: true });

      abortRef.current?.abort();
      abortRef.current = new AbortController();

      let finalAnswer = "";
      let finalCitations: Citation[] = [];
      let finalSuggestions: string[] = [];
      const toolActivity: string[] = [];

      try {
        const history = messages.map((m) => ({ role: m.role, content: m.content }));
        const res = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: text,
            session_id: sessionId.current,
            history,
          }),
          signal: abortRef.current.signal,
        });

        if (!res.body) throw new Error("No response body");

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        const parseEvent = (block: string) => {
          const lines = block.split("\n");
          let eventType = "";
          let dataLine = "";
          for (const line of lines) {
            if (line.startsWith("event:")) eventType = line.slice(6).trim();
            else if (line.startsWith("data:")) dataLine = line.slice(5).trim();
          }
          if (!eventType || !dataLine) return;

          try {
            const payload = JSON.parse(dataLine);
            switch (eventType) {
              case "token":
                finalAnswer += (payload as { text: string }).text;
                setTurn((t) => ({
                  ...t,
                  streamText: t.streamText + (payload as { text: string }).text,
                }));
                break;
              case "tool_call":
                toolActivity.push(`Calling ${(payload as { name: string }).name}...`);
                setTurn((t) => ({
                  ...t,
                  toolActivity: [...t.toolActivity, `Calling ${(payload as { name: string }).name}...`],
                }));
                break;
              case "tool_result":
                break;
              case "citations":
                finalCitations = payload as Citation[];
                setTurn((t) => ({ ...t, citations: payload as Citation[] }));
                break;
              case "final":
                finalAnswer = (payload as { answer: string }).answer;
                setTurn((t) => ({ ...t, streamText: finalAnswer }));
                break;
              case "suggestions":
                finalSuggestions = payload as string[];
                break;
              case "error":
                setTurn((t) => ({
                  ...t,
                  error: (payload as { message: string }).message,
                  streaming: false,
                }));
                break;
            }
          } catch {
            /* ignore malformed events */
          }
        };

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          // sse-starlette emits CRLF line endings; normalize to LF before splitting.
          buffer += decoder.decode(value, { stream: true }).replace(/\r\n/g, "\n");
          const parts = buffer.split("\n\n");
          buffer = parts.pop() ?? "";
          for (const part of parts) {
            if (part.trim()) parseEvent(part);
          }
        }
        if (buffer.trim()) parseEvent(buffer);
      } catch (err) {
        if ((err as Error).name === "AbortError") return;
        setTurn((t) => ({
          ...t,
          error: `Connection error: ${(err as Error).message}`,
          streaming: false,
        }));
        return;
      }

      const assistantMsg: ChatMessage = {
        role: "assistant",
        content: finalAnswer || turn.streamText,
        citations: finalCitations,
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setTurn((prev) => ({ ...prev, streaming: false }));
      setSuggestions(finalSuggestions.length ? finalSuggestions : STARTER_SUGGESTIONS);

      void toolActivity;
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [messages, turn.streaming]
  );

  const clear = useCallback(() => {
    abortRef.current?.abort();
    setMessages([]);
    setTurn(INITIAL_TURN);
    setSuggestions(STARTER_SUGGESTIONS);
    sessionId.current = crypto.randomUUID();
  }, []);

  return { messages, turn, suggestions, sendMessage, clear };
}
