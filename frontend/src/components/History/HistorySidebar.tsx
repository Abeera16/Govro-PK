import React, { useEffect, useState } from "react";
import { MessageSquarePlus, MessageSquareText, Trash2 } from "lucide-react";
import { historyApi } from "../../api/client";
import type { Conversation } from "../../types";

interface Props {
  activeConversationId: string | null;
  onSelect: (id: string) => void;
  onNewChat: () => void;
  refreshKey: number;
}

const HistorySidebar: React.FC<Props> = ({ activeConversationId, onSelect, onNewChat, refreshKey }) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    historyApi
      .list()
      .then((res) => setConversations(res.data))
      .finally(() => setLoading(false));
  }, [refreshKey]);

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    await historyApi.remove(id);
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeConversationId === id) onNewChat();
  };

  return (
    <aside className="history-sidebar">
      <button className="btn-new-chat" onClick={onNewChat}>
        <MessageSquarePlus size={16} />
        New conversation
      </button>
      <div className="history-list">
        {loading && <div className="history-empty">Loading…</div>}
        {!loading && conversations.length === 0 && (
          <div className="history-empty">No conversations yet</div>
        )}
        {conversations.map((c) => (
          <div
            key={c.id}
            className={`history-item ${activeConversationId === c.id ? "active" : ""}`}
            onClick={() => onSelect(c.id)}
          >
            <MessageSquareText size={15} className="history-item-icon" />
            <span className="history-item-title">{c.title}</span>
            <button className="history-item-delete" onClick={(e) => handleDelete(e, c.id)} title="Delete" aria-label="Delete conversation">
              <Trash2 size={14} />
            </button>
          </div>
        ))}
      </div>
    </aside>
  );
};

export default HistorySidebar;
