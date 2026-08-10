import React from "react";
import Seal from "./Seal";

const Wordmark: React.FC<{ size?: "sm" | "md" | "lg"; withTagline?: boolean }> = ({
  size = "md",
  withTagline = false,
}) => {
  const sealSize = size === "lg" ? 44 : size === "sm" ? 26 : 34;
  return (
    <div className={`wordmark wordmark-${size}`}>
      <Seal size={sealSize} />
      <div className="wordmark-text">
        <span className="wordmark-name">CivicAI</span>
        {withTagline && <span className="wordmark-tagline">Pakistan Citizen Services</span>}
      </div>
    </div>
  );
};

export default Wordmark;
