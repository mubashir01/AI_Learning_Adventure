const API_URL = "http://localhost:8000";

export type Question = {
  id: number;
  category: string;
  difficulty: string;
  question: string;
  options: string[];
  seconds: number;
};

export async function getCategories() {
  const response = await fetch(`${API_URL}/categories`);
  return response.json() as Promise<string[]>;
}

export async function getDifficulties() {
  const response = await fetch(`${API_URL}/difficulties`);
  return response.json() as Promise<string[]>;
}

export async function getRandomQuestion(category: string, difficulty: string) {
  const params = new URLSearchParams({ category, difficulty });
  const response = await fetch(`${API_URL}/questions/random?${params.toString()}`);
  return response.json() as Promise<Question>;
}

export async function submitAnswer(questionId: number, answer: string, timeLeft: number) {
  const response = await fetch(`${API_URL}/answers`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question_id: questionId, answer, time_left: timeLeft }),
  });
  return response.json() as Promise<{ correct: boolean; correct_answer: string; earned_xp: number }>;
}
