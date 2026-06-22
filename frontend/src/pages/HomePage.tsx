import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <section className="page">
      <h1>AI Learning Adventure</h1>
      <p>Practice short learning challenges and track your first score.</p>
      <Link to="/play">
        <button>Start</button>
      </Link>
    </section>
  );
}
