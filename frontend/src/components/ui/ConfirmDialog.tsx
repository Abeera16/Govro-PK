import React, { useEffect, useRef } from "react";

interface Props {
  open: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  destructive?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

const ConfirmDialog: React.FC<Props> = ({
  open,
  title,
  message,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  destructive = false,
  onConfirm,
  onCancel,
}) => {
  const confirmRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (open) confirmRef.current?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onCancel();
    };
    if (open) document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, onCancel]);

  if (!open) return null;

  return (
    <div className="dialog-overlay" onMouseDown={onCancel}>
      <div
        className="dialog-card"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
        onMouseDown={(e) => e.stopPropagation()}
      >
        <h2 id="dialog-title" className="dialog-title">{title}</h2>
        <p className="dialog-message">{message}</p>
        <div className="dialog-actions">
          <button className="btn-ghost" onClick={onCancel}>{cancelLabel}</button>
          <button
            ref={confirmRef}
            className={destructive ? "btn-danger" : "btn-primary"}
            onClick={onConfirm}
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmDialog;
