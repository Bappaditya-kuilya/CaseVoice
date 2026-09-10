import { Routes, Route, Link, useLocation } from "react-router-dom";
import Dashboard from "./pages/Dashboard.tsx";
import LiveCall from "./pages/LiveCall.tsx";
import CaseDetail from "./pages/CaseDetail.tsx";

export default function App() {
  const location = useLocation();
  const hideNav = location.pathname === "/call";

  return (
    <div className="app">
      {!hideNav && (
        <nav className="nav">
          <Link to="/" className="nav-logo">
            ⚖ CaseVoice
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
        </Routes>
      </main>
    </div>
  );
}
