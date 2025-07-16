'use client'
import { LoaderCircle } from "lucide-react";
import { useEffect, useState } from "react";
import { CardPreviewMusic } from "../common/card-preview";

export function SectionSearchMusic({ query }: { query: string }) {
  const [music, setMusics] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchMusics() {
      try {
        const response = await fetch("http://127.0.0.1:8000/query/sql", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: `SELECT id, track_name, track_artist, image_url FROM music WHERE lyrics @@ '${query}' LIMIT 10;` }),
        });
        console.log(`SELECT id, track_name, track_artist, image_url FROM music WHERE lyrics @@ '${query}'`);
        const result = await response.json();
        if (result.success) {
          setMusics(result.data);
        } else {
          console.error("Error fetching search music:", result);
        }
      } catch (err) {
        console.error("Fetch error:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchMusics();
  }, [query]);

  return (
    <div className="container mx-auto px-24 py-6 flex flex-col gap-y-8 select-none">
      {loading &&
        <div className="flex-1 flex items-center justify-center">
          <LoaderCircle className="w-5 h-5 animate-spin text-gray-500" />
        </div>
      }
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {!loading && music.length === 0 && (
          <p className="text-muted-foreground">No se encontraron resultados.</p>
        )}
        {!loading && music.map((item, idx) => (
          <CardPreviewMusic
            key={idx}
            {...item}
          />
        ))}
      </div>
    </div>
  )
}