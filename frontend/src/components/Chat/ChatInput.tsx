import React, { useState } from "react";
import { SendHorizontal } from "lucide-react";

interface Props {
  onSend: (text: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

const ChatInput: React.FC<Props> = ({ onSend, disabled, placeholder }) => {
  const [text, setText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText("");
  };

  return (
    <form className="chat-input-form" onSubmit={handleSubmit}>
      <textarea
        className="chat-input"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={placeholder || "Ask about passports, NADRA, taxes, scholarships, driving license…"}
        rows={2}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
          }
        }}
      />
      <button type="submit" className="btn-send" disabled={disabled || !text.trim()} aria-label="Send message">
        <SendHorizontal size={17} />
      </button>
    </form>
  );
};

export default ChatInput;
