import React, { useState } from "react";
import ChatWindow from "../Chat/ChatWindow";
import HistorySidebar from "../History/HistorySidebar";
import Wordmark from "../Brand/Wordmark";
import UserMenu from "./UserMenu";
import { useAuth } from "../../context/AuthContext";

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleConversationCreated = (id: string) => {
    setConversationId(id);
    setRefreshKey((k) => k + 1);
  };

  const handleNewChat = () => setConversationId(null);

  return (
    <div className="dashboard-layout">
      <header className="topbar">
        <Wordmark size="sm" />
        {user && <UserMenu user={user} onLogout={logout} />}
      </header>
      <div className="dashboard-body">
        <HistorySidebar
          activeConversationId={conversationId}
          onSelect={setConversationId}
          onNewChat={handleNewChat}
          refreshKey={refreshKey}
        />
        <ChatWindow conversationId={conversationId} onConversationCreated={handleConversationCreated} />
      </div>
    </div>
  );
};

export default Dashboard;
