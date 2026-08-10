export interface Citation {
  title: string;
  url: string;
  snippet: string;
  source_type: "gov_rag" | "web_search";
}

export interface AgentStep {
  agent: string;
  action: string;
  detail: string;
  timestamp: string;
}

export interface ChatResponse {
  conversation_id: string;
  message_id: string;
  answer: string;
  requires_clarification: boolean;
  clarification_question?: string;
  citations: Citation[];
  agent_trace: AgentStep[];
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
  agent_trace?: AgentStep[];
  created_at: string;
}

export interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ConversationDetail extends Conversation {
  messages: Message[];
}

export interface User {
  id: string;
  full_name: string;
  email: string;
  is_active: boolean;
}
