'use client'
import { useState, useEffect } from "react";
import { CardPreviewMusic } from "../common/card-preview";


export function SectionRelatedTracksFile({filepath} : {filepath: string}) {
  const [music, setMusics] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchMusics() {
      try {
        const response = await fetch("http://127.0.0.1:8000/query/sql", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: `
            SELECT id, track_name, track_artist, image_url 
            FROM music
            WHERE path_download_wav <-> '${filepath}'
            LIMIT 10;
          ` }),
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
  }, [filepath]);

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      {loading && <p>Loading...</p>}
      {!loading && music.map((item, idx) => (
        <CardPreviewMusic
          key={idx}
          {...item}
        />
      ))}
    </div>
  )
}