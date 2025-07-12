'use client'
import { useEffect, useState } from "react";

function getRandomGradient() {
  const hue = Math.floor(Math.random() * 360);
  const saturation = 70 + Math.random() * 20; // 70–90%
  const lightness1 = 40 + Math.random() * 20; // 40–60%
  const lightness2 = 60 + Math.random() * 20; // 60–80%

  return `linear-gradient(135deg, hsl(${hue}, ${saturation}%, ${lightness1}%) 0%, hsl(${(hue + 60) % 360}, ${saturation}%, ${lightness2}%) 100%)`;
}

export default function AuthorPage() {
  const [author, setAuthor] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [gradients, setGradients] = useState<string[]>([]);

  useEffect(() => {
    async function fetchAuthor() {
      try {
        const response = await fetch("http://127.0.0.1:8000/query/sql", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: "SELECT DISTINCT(track_artist) FROM music;" }),
        });

        const result = await response.json();
        if (result.success) {
          setAuthor(result.data);
          setGradients(result.data.map(() => getRandomGradient()));
        } else {
          console.error("Error fetching genres:", result);
        }
      } catch (err) {
        console.error("Fetch error:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchAuthor();
  }, []);

  return (
    <div className="container mx-auto px-24 py-6 flex flex-col gap-y-8 select-none">
      <div className="flex items-center gap-x-6">
        <h2 className="text-2xl align-top">Authors</h2>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {loading && <p>Loading...</p>}
        {!loading && author.slice(1,50).map((item, idx) => (
          <div className="flex flex-col items-center gap-y-3" key={idx}>
            <div
              className="rounded-full shadow-md hover:shadow-xl transition-all font-semibold text-lg h-40 w-40"
              style={{
                background: gradients[idx],
              }}
            ></div>
            <span className="font-semibold text-sm">{item.track_artist}</span>
          </div>
        ))}
      </div>
    </div>
  );
}