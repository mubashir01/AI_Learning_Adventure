import { useEffect, useState } from "react";

type Score = {
  xp: number;
  coins: number;
  level: number;
};

export function ScorePage() {
  const [score, setScore] = useState<Score | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/score")
      .then((response) => response.json())
      .then(setScore)
      .catch(() => setScore({ xp: 0, coins: 0, level: 1 }));
  }, []);

  return (
    <section className="page">
      <h1>Score</h1>
      <div className="panel">
        <p>XP: {score?.xp ?? 0}</p>
        <p>Coins: {score?.coins ?? 0}</p>
        <p>Level: {score?.level ?? 1}</p>
      </div>
    </section>
  );
}
