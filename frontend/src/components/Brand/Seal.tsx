import React from "react";

/**
 * GovroPK's signature mark — an abstracted verification seal (shield + check
 * within a ringed badge). Used as the logo, browser favicon source, and the
 * assistant's chat avatar, tying the whole product to its core promise:
 * verified, citation-backed answers rather than raw model guesses.
 */
const Seal: React.FC<{ size?: number; className?: string }> = ({ size = 32, className }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 48 48"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
    role="img"
    aria-label="GovroPK"
  >
    <circle cx="24" cy="24" r="22.5" fill="var(--seal-ring, #A9812E)" opacity="0.18" />
    <circle cx="24" cy="24" r="19" fill="var(--seal-bg, #0E4A38)" />
    <circle cx="24" cy="24" r="19" stroke="var(--seal-ring, #A9812E)" strokeWidth="1.4" opacity="0.85" />
    <path
      d="M24 10.5 L34.5 14.5 V23.2 C34.5 30.4 30.2 35.6 24 37.5 C17.8 35.6 13.5 30.4 13.5 23.2 V14.5 L24 10.5 Z"
      fill="none"
      stroke="var(--seal-fg, #F6F3EC)"
      strokeWidth="1.6"
      strokeLinejoin="round"
    />
    <path
      d="M18.5 23.5 L22.3 27.3 L29.5 19.5"
      fill="none"
      stroke="var(--seal-fg, #F6F3EC)"
      strokeWidth="2.1"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

export default Seal;
