import { Component, type ReactNode } from "react";
import { Routes, Route, Link, useLocation } from "react-router-dom";
import Dashboard from "./pages/Dashboard.tsx";
import LiveCall from "./pages/LiveCall.tsx";
import CaseDetail from "./pages/CaseDetail.tsx";

class ErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean }> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 24, textAlign: "center" }}>
          <h2>Something went wrong.</h2>
          <Link to="/">Back to Dashboard</Link>
        </div>
      );
    }
    return this.props.children;
  }
}

function NotFound() {
  return (
    <div style={{ padding: 24, textAlign: "center" }}>
      <h2>Page not found.</h2>
      <Link to="/">Back to Dashboard</Link>
    </div>
  );
}

export default function App() {
  const location = useLocation();
  const hideNav = location.pathname === "/call";

  return (
    <div className="app">
      {!hideNav && (
        <nav className="nav">
          <Link to="/" className="nav-logo">
            CaseVoice
          </Link>
          <div className="nav-links">
            <Link
              to="/"
              className={location.pathname === "/" ? "active" : ""}
            >
              Dashboard
            </Link>
            <Link
              to="/call"
              className={location.pathname === "/call" ? "active" : ""}
            >
              New Call
            </Link>
          </div>
        </nav>
      )}
      <main className={hideNav ? "main main-full" : "main"}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/call" element={<LiveCall />} />
            <Route path="/case/:id" element={<CaseDetail />} />
            <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </div>
  );
}
