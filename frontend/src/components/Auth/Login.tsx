import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AlertCircle } from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import Wordmark from "../Brand/Wordmark";

const Login: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Login failed. Check your credentials.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-panel" />
      <div className="auth-card">
        <Wordmark size="lg" withTagline />
        <h1 className="auth-heading">Welcome back</h1>
        <p className="auth-subheading">Sign in to continue your conversation with CivicAI.</p>

        <form onSubmit={onSubmit} className="auth-form">
          <label>
            Email
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoFocus />
          </label>
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          {error && (
            <div className="form-error">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}
          <button type="submit" disabled={submitting} className="btn-primary btn-block">
            {submitting ? "Signing in…" : "Sign in"}
          </button>
        </form>
        <p className="auth-switch">
          Don't have an account? <Link to="/register">Create one</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
