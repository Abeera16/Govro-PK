import React from "react";
import { LayoutGrid, GitBranch, HelpCircle, Search, Globe2, ShieldCheck } from "lucide-react";
import type { AgentStep } from "../../types";

const AGENT_META: Record<string, { label: string; icon: React.ReactNode }> = {
  supervisor: { label: "Supervisor", icon: <LayoutGrid size={13} /> },
  router: { label: "Router", icon: <GitBranch size={13} /> },
  clarification_agent: { label: "Clarification Agent", icon: <HelpCircle size={13} /> },
  retrieval_agent: { label: "Retrieval Agent (RAG)", icon: <Search size={13} /> },
  fallback_agent: { label: "Fallback Agent (Web Search)", icon: <Globe2 size={13} /> },
  citation_agent: { label: "Citation & Synthesis Agent", icon: <ShieldCheck size={13} /> },
};

const AgentStatus: React.FC<{ trace: AgentStep[] }> = ({ trace }) => {
  if (!trace || trace.length === 0) return null;

  return (
    <div className="agent-trace">
      <div className="agent-trace-title">Agent workflow</div>
      <ol className="agent-trace-list">
        {trace.map((step, i) => {
          const meta = AGENT_META[step.agent] || { label: step.agent, icon: null };
          return (
            <li key={i} className="agent-trace-step">
              <span className="agent-trace-index">{String(i + 1).padStart(2, "0")}</span>
              <span className="agent-badge">{meta.icon}{meta.label}</span>
              <span className="agent-detail">{step.detail}</span>
            </li>
          );
        })}
      </ol>
    </div>
  );
};

export default AgentStatus;
