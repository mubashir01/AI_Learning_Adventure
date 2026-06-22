import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, NavLink, Route, Routes } from "react-router-dom";
import "./styles.css";
import { AboutPage } from "./pages/AboutPage";
import { HomePage } from "./pages/HomePage";
import { PlayPage } from "./pages/PlayPage";
import { ScorePage } from "./pages/ScorePage";

function App() {
  return (
    <BrowserRouter>
      <header className="topbar">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/play">Play</NavLink>
        <NavLink to="/score">Score</NavLink>
        <NavLink to="/about">About</NavLink>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/play" element={<PlayPage />} />
          <Route path="/score" element={<ScorePage />} />
          <Route path="/about" element={<AboutPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
