'use client'
import { useEffect, useState } from "react";
import { CardPreviewMusic } from "../common/card-preview";

export function SectionRelatedTracks({id}:{id: number}) {
  const [music, setMusics] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchMusics() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/query/top/${id}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: "SELECT id, track_name, track_artist, image_url FROM music LIMIT 5;" }),
        });

        const result = await response.json();
        if (result.success) {
          setMusics(result.data);
        } else {
          console.error("Error fetching genres:", result);
        }
      } catch (err) {
        console.error("Fetch error:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchMusics();
  }, []);

  return (
    <div className="container mx-auto px-24 py-6 flex flex-col gap-y-8">
      <div className="flex items-center gap-x-6">
        <h2 className="text-2xl align-top">Related Tracks</h2>
      </div>
      <div className="grid grid-cols-5 gap-4">
        {loading && <p>Loading...</p>}
        {!loading && music.map((item, idx) => (
          <CardPreviewMusic
            key={idx}
            {...item}
          />
        ))}
      </div>
    </div>
  );
}