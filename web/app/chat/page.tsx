import type { Metadata } from "next";
import ChatInterface from "@/components/ChatInterface";

export const metadata: Metadata = {
  title: "Chat with Sanket — CloneAMA",
  description:
    "Chat with an AI version of Sanket Shah, backed by a LangGraph ReAct agent with tool-calling, and recruiter job-fit mode.",
};

export default function ChatPage() {
  return <ChatInterface />;
}
