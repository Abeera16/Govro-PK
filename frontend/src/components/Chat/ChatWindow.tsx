import React, { useEffect, useRef, useState } from "react";
import { chatApi, historyApi } from "../../api/client";
import type { Message } from "../../types";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";
import Seal from "../Brand/Seal";

interface Props {
  conversationId: string | null;
  onConversationCreated: (id: string) => void;
}

const SUGGESTED_PROMPTS = [
  "How do I apply for a new Pakistani passport?",
  "What documents do I need for a NADRA CNIC renewal?",
  "How do I file my income tax return with FBR?",
  "How can I apply for an HEC scholarship?",
];

const ChatWindow: React.FC<Props> = ({ conversationId, onConversationCreated }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [pendingClarification, setPendingClarification] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (conversationId) {
      historyApi.get(conversationId).then((res) => setMessages(res.data.messages));
    } else {
      setMessages([]);
      setPendingClarification(false);
    }
  }, [conversationId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async (text: string) => {
    setError(null);
    const userMsg: Message = {
      id: `local-${Date.now()}`,
      role: "user",
      content: text,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await chatApi.send(
        text,
        conversationId || undefined,
        pendingClarification ? text : undefined
      );
      const data = res.data;

      if (!conversationId) onConversationCreated(data.conversation_id);

      const assistantMsg: Message = {
        id: data.message_id,
        role: "assistant",
        content: data.answer,
        citations: data.citations,
        agent_trace: data.agent_trace,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setPendingClarification(data.requires_clarification);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-messages">
        {messages.length === 0 && !loading && (
          <div className="chat-empty-state">
            <Seal size={52} />
            <h2>Assalam-o-Alaikum</h2>
            <p>Ask me anything about Pakistani government services — I'll answer with sources.</p>
            <div className="suggested-prompts">
              {SUGGESTED_PROMPTS.map((p) => (
                <button key={p} className="suggested-prompt" onClick={() => sendMessage(p)}>
                  {p}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m) => (
          <MessageBubble key={m.id} message={m} />
        ))}
        {loading && (
          <div className="message-row assistant">
            <div className="message-avatar"><Seal size={22} /></div>
            <div className="message-content">
              <div className="message-bubble typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        {error && <div className="chat-error">{error}</div>}
        <div ref={bottomRef} />
      </div>
      <ChatInput
        onSend={sendMessage}
        disabled={loading}
        placeholder={
          pendingClarification
            ? "Please answer the clarifying question above…"
            : undefined
        }
      />
    </div>
  );
};

export default ChatWindow;
