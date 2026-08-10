import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AlertCircle } from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import Wordmark from "../Brand/Wordmark";

const Register: React.FC = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await register(fullName, email, password);
      navigate("/");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Registration failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-panel" />
      <div className="auth-card">
        <Wordmark size="lg" withTagline />
        <h1 className="auth-heading">Create your account</h1>
        <p className="auth-subheading">Get accurate, sourced answers on government services.</p>

        <form onSubmit={onSubmit} className="auth-form">
          <label>
            Full name
            <input value={fullName} onChange={(e) => setFullName(e.target.value)} required autoFocus />
          </label>
          <label>
            Email
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </label>
          <label>
            Password
            <input
              type="password"
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <span className="field-hint">At least 8 characters</span>
          </label>
          {error && (
            <div className="form-error">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}
          <button type="submit" disabled={submitting} className="btn-primary btn-block">
            {submitting ? "Creating account…" : "Create account"}
          </button>
        </form>
        <p className="auth-switch">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
