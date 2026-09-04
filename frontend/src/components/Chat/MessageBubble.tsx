import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { UserRound } from "lucide-react";
import type { Message } from "../../types";
import Seal from "../Brand/Seal";
import AgentStatus from "../Agents/AgentStatus";
import CitationList from "../Citations/CitationList";

const MessageBubble: React.FC<{ message: Message }> = ({ message }) => {
  const isUser = message.role === "user";
  return (
    <div className={`message-row ${isUser ? "user" : "assistant"}`}>
      <div className="message-avatar">
        {isUser ? <UserRound size={16} /> : <Seal size={22} />}
      </div>
      <div className="message-content">
        <div className="message-bubble">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              table: ({ children }) => (
                <div className="message-table-wrap">
                  <table className="message-table">{children}</table>
                </div>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
        {!isUser && message.citations && message.citations.length > 0 && (
          <CitationList citations={message.citations} />
        )}
        {!isUser && message.agent_trace && message.agent_trace.length > 0 && (
          <AgentStatus trace={message.agent_trace as any} />
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
