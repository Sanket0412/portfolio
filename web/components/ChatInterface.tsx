"use client";

import { useState, useRef, useEffect, KeyboardEvent } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";
import { useAgentChat } from "@/hooks/useAgentChat";

const AVATAR = "/avatar.jpg"; // self-hosted face crop (public/avatar.jpg)

function ToolActivity({ items }: { items: string[] }) {
  if (!items.length) return null;
  return (
    <div className="flex flex-wrap gap-1.5 mb-2">
      {items.map((item, i) => (
        <span key={i} className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-blue-950/40 border border-blue-900/50 text-blue-400">
          <svg className="w-3 h-3 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3V4a10 10 0 100 20v-4l-3 3 3 3v-4a8 8 0 01-8-8z" />
          </svg>
          {item}
        </span>
      ))}
    </div>
  );
}

function isJobDescription(text: string): boolean {
  if (text.length < 200) return false;
  const signals = [
    "requirements",
    "responsibilities",
    "qualifications",
    "you will",
    "we are looking",
    "what you",
    "must have",
    "nice to have",
    "years of experience",
  ];
  const lower = text.toLowerCase();
  return signals.filter((s) => lower.includes(s)).length >= 2;
}

export default function ChatInterface() {
  const { messages, turn, suggestions, sendMessage, clear } = useAgentChat();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, turn.streamText]);

  const submit = () => {
    const text = input.trim();
    if (!text || turn.streaming) return;
    setInput("");
    sendMessage(text);
  };

  const onKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="border-b border-zinc-800 px-6 py-4 flex items-center justify-between bg-zinc-950/80 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <Image
            src={AVATAR}
            alt="Sanket Shah"
            width={36}
            height={36}
            className="rounded-full object-cover h-9 w-9"
          />
          <div>
            <p className="text-zinc-50 font-semibold text-sm">CloneAMA</p>
            <p className="text-zinc-500 text-xs">Chat with Sanket Shah (AI)</p>
          </div>
        </div>
        <button
          onClick={clear}
          className="text-zinc-500 hover:text-zinc-300 text-xs flex items-center gap-1.5 transition-colors px-3 py-1.5 rounded-lg hover:bg-zinc-800"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Clear
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
        {messages.length === 0 && !turn.streaming && (
          <div className="text-center py-16">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full overflow-hidden border-2 border-zinc-700">
              <Image src={AVATAR} alt="Sanket" width={64} height={64} className="h-full w-full object-cover" />
            </div>
            <p className="text-zinc-300 font-medium mb-1">Hi, I&apos;m Sanket (AI)</p>
            <p className="text-zinc-500 text-sm max-w-sm mx-auto">
              Ask me about my work, projects, publications, or paste a job description for a
              fit analysis.
            </p>
          </div>
        )}

        <AnimatePresence initial={false}>
          {messages.map((msg, i) => {
            const isUser = msg.role === "user";
            const jdDetected = isUser && isJobDescription(msg.content);
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25 }}
                className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
              >
                {!isUser && (
                  <Image
                    src={AVATAR}
                    alt="Sanket"
                    width={32}
                    height={32}
                    className="rounded-full object-cover h-8 w-8 shrink-0 mt-0.5"
                  />
                )}
                <div className={`max-w-[80%] ${isUser ? "items-end" : "items-start"} flex flex-col gap-1.5`}>
                  {jdDetected && (
                    <span className="text-xs text-amber-400 bg-amber-950/40 border border-amber-900/60 px-2 py-0.5 rounded-full self-start">
                      Recruiter / job-fit mode detected
                    </span>
                  )}
                  <div
                    className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
                      isUser
                        ? "bg-blue-600 text-white rounded-br-sm"
                        : "bg-zinc-900 border border-zinc-800 text-zinc-100 rounded-bl-sm"
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>

        {/* Streaming assistant turn */}
        {turn.streaming && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex gap-3 justify-start"
          >
            <Image
              src={AVATAR}
              alt="Sanket"
              width={32}
              height={32}
              className="rounded-full object-cover h-8 w-8 shrink-0 mt-0.5"
            />
            <div className="max-w-[80%] flex flex-col gap-1.5">
              <ToolActivity items={turn.toolActivity} />
              <div className="px-4 py-3 rounded-2xl rounded-bl-sm bg-zinc-900 border border-zinc-800 text-zinc-100 text-sm leading-relaxed">
                {turn.streamText ? (
                  <span className="whitespace-pre-wrap">{turn.streamText}</span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-zinc-500">
                    <span className="animate-pulse">●</span>
                    <span className="animate-pulse" style={{ animationDelay: "0.2s" }}>●</span>
                    <span className="animate-pulse" style={{ animationDelay: "0.4s" }}>●</span>
                  </span>
                )}
              </div>
            </div>
          </motion.div>
        )}

        {/* Error */}
        {turn.error && (
          <div className="text-red-400 text-sm bg-red-950/30 border border-red-900/50 rounded-xl px-4 py-3">
            {turn.error}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Suggestions */}
      {suggestions.length > 0 && !turn.streaming && (
        <div className="px-4 pb-2 flex flex-wrap gap-2">
          {suggestions.map((s, i) => (
            <button
              key={i}
              onClick={() => sendMessage(s)}
              className="text-xs px-3 py-1.5 rounded-full border border-zinc-700 bg-zinc-900 text-zinc-400 hover:text-zinc-50 hover:border-zinc-500 transition-colors"
            >
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="border-t border-zinc-800 px-4 py-4 bg-zinc-950">
        <div className="flex items-end gap-2 rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-3 focus-within:border-zinc-500 transition-colors">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={onKeyDown}
            rows={1}
            placeholder="Ask me about my work, projects, or experience..."
            disabled={turn.streaming}
            className="flex-1 bg-transparent text-zinc-100 placeholder:text-zinc-600 text-sm resize-none outline-none leading-relaxed max-h-32 overflow-y-auto disabled:opacity-50"
            style={{ fieldSizing: "content" } as React.CSSProperties}
          />
          <button
            onClick={submit}
            disabled={!input.trim() || turn.streaming}
            className="shrink-0 p-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            aria-label="Send"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
        <p className="text-zinc-600 text-xs mt-2 text-center">
          Grounded in my portfolio content. May not have all the answers.
        </p>
      </div>
    </div>
  );
}
