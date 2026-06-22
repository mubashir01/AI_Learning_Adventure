import { useEffect, useState } from "react";
import {
  getCategories,
  getDifficulties,
  getRandomQuestion,
  Question,
  submitAnswer,
} from "../services/api";

export function PlayPage() {
  const [categories, setCategories] = useState<string[]>([]);
  const [difficulties, setDifficulties] = useState<string[]>([]);
  const [category, setCategory] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [question, setQuestion] = useState<Question | null>(null);
  const [timeLeft, setTimeLeft] = useState(0);
  const [result, setResult] = useState("");

  useEffect(() => {
    getCategories().then((items) => {
      setCategories(items);
      setCategory(items[0] ?? "");
    });
    getDifficulties().then((items) => {
      setDifficulties(items);
      setDifficulty(items[0] ?? "");
    });
  }, []);

  useEffect(() => {
    if (!question || result) return;
    if (timeLeft <= 0) {
      setResult("Time is up.");
      return;
    }
    const timer = window.setTimeout(() => setTimeLeft((value) => value - 1), 1000);
    return () => window.clearTimeout(timer);
  }, [question, result, timeLeft]);

  async function startQuestion() {
    if (!category || !difficulty) return;
    const nextQuestion = await getRandomQuestion(category, difficulty);
    setQuestion(nextQuestion.id ? nextQuestion : null);
    setTimeLeft(nextQuestion.seconds ?? 0);
    setResult("");
  }

  async function chooseAnswer(answer: string) {
    if (!question || result) return;
    const response = await submitAnswer(question.id, answer, timeLeft);
    setResult(response.correct ? `Correct. +${response.earned_xp} XP` : `Answer: ${response.correct_answer}`);
  }

  return (
    <section className="page">
      <h1>Play</h1>
      <div className="panel">
        <div className="controls">
          <label>
            Category
            <select value={category} onChange={(event) => setCategory(event.target.value)}>
              {categories.map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>
          </label>
          <label>
            Difficulty
            <select value={difficulty} onChange={(event) => setDifficulty(event.target.value)}>
              {difficulties.map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>
          </label>
          <button onClick={startQuestion}>Random Question</button>
        </div>
      </div>

      {question && (
        <div className="panel question">
          <p>Time: {timeLeft}s</p>
          <h2>{question.question}</h2>
          <div className="answers">
            {question.options.map((option) => (
              <button key={option} onClick={() => chooseAnswer(option)}>
                {option}
              </button>
            ))}
          </div>
          {result && <p>{result}</p>}
        </div>
      )}
      {!question && result && <p>{result}</p>}
    </section>
  );
}
