'use client'
import { LoaderCircle } from "lucide-react";
import { useEffect, useState } from "react";

function getRandomGradient() {
  const hue = Math.floor(Math.random() * 360);
  const saturation = 70 + Math.random() * 20; // 70–90%
  const lightness1 = 40 + Math.random() * 20; // 40–60%
  const lightness2 = 60 + Math.random() * 20; // 60–80%

  return `linear-gradient(135deg, hsl(${hue}, ${saturation}%, ${lightness1}%) 0%, hsl(${(hue + 60) % 360}, ${saturation}%, ${lightness2}%) 100%)`;
}

export default function GenrePage() {
  const [genre, setGenre] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [gradients, setGradients] = useState<string[]>([]);

  useEffect(() => {
    async function fetchGenre() {
      try {
        const response = await fetch("http://127.0.0.1:8000/query/sql", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: "SELECT DISTINCT(playlist_genre) FROM music;" }),
        });

        const result = await response.json();
        if (result.success) {
          setGenre(result.data);
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

    fetchGenre();
  }, []);

  return (
    <div className="container mx-auto px-24 py-6 flex flex-col gap-y-8 select-none">
      <div className="flex items-center gap-x-6">
        <h2 className="text-2xl align-top">Géneros</h2>
      </div>
      {loading &&
        <div className="flex-1 flex items-center justify-center">
          <LoaderCircle className="w-5 h-5 animate-spin text-gray-500" />
        </div>
      }
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {!loading && genre.map((item, idx) => (
          <div
            key={idx}
            className="rounded-lg shadow-md hover:shadow-xl transition-all text-white font-semibold flex items-center justify-center h-32"
            style={{
              background: gradients[idx],
            }}
          >
            {item.playlist_genre.toUpperCase()}
          </div>
        ))}
      </div>
    </div>
  );
}