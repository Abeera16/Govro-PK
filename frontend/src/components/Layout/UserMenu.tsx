import React, { useEffect, useRef, useState } from "react";
import { ChevronDown, LogOut, UserRound } from "lucide-react";
import ConfirmDialog from "../ui/ConfirmDialog";
import type { User } from "../../types";

const initials = (name: string) =>
  name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0]?.toUpperCase())
    .join("");

const UserMenu: React.FC<{ user: User; onLogout: () => void }> = ({ user, onLogout }) => {
  const [open, setOpen] = useState(false);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const onClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, []);

  return (
    <>
      <div className="user-menu" ref={menuRef}>
        <button className="user-chip" onClick={() => setOpen((o) => !o)} aria-haspopup="menu" aria-expanded={open}>
          <span className="user-avatar">{initials(user.full_name) || <UserRound size={15} />}</span>
          <span className="user-chip-name">{user.full_name}</span>
          <ChevronDown size={15} className={`user-chip-chevron ${open ? "open" : ""}`} />
        </button>

        {open && (
          <div className="user-dropdown" role="menu">
            <div className="user-dropdown-header">
              <span className="user-dropdown-name">{user.full_name}</span>
              <span className="user-dropdown-email">{user.email}</span>
            </div>
            <div className="user-dropdown-divider" />
            <button
              className="user-dropdown-item danger"
              role="menuitem"
              onClick={() => {
                setOpen(false);
                setConfirmOpen(true);
              }}
            >
              <LogOut size={16} />
              Log out
            </button>
          </div>
        )}
      </div>

      <ConfirmDialog
        open={confirmOpen}
        title="Log out of GovroPK?"
        message="You'll need to sign in again to access your conversations and account."
        confirmLabel="Log out"
        cancelLabel="Stay signed in"
        destructive
        onConfirm={() => {
          setConfirmOpen(false);
          onLogout();
        }}
        onCancel={() => setConfirmOpen(false)}
      />
    </>
  );
};

export default UserMenu;
