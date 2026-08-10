import React from "react";
import { ExternalLink, ShieldCheck, Globe } from "lucide-react";
import type { Citation } from "../../types";

const CitationList: React.FC<{ citations: Citation[] }> = ({ citations }) => {
  if (!citations || citations.length === 0) return null;

  return (
    <div className="citations-block">
      <div className="citations-title">Sources</div>
      <ul className="citations-list">
        {citations.map((c, i) => (
          <li key={i} className={`citation-item ${c.source_type}`}>
            <div className="citation-item-head">
              <span className={`citation-tag ${c.source_type}`}>
                {c.source_type === "gov_rag" ? <ShieldCheck size={12} /> : <Globe size={12} />}
                {c.source_type === "gov_rag" ? "Official Document" : "Web Search"}
              </span>
            </div>
            {c.url ? (
              <a href={c.url} target="_blank" rel="noreferrer" className="citation-link">
                {c.title || c.url}
                <ExternalLink size={12} />
              </a>
            ) : (
              <span className="citation-link">{c.title}</span>
            )}
            {c.snippet && <p className="citation-snippet">{c.snippet}</p>}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CitationList;
