'use client';
import { SectionDetailsMusic } from '@/components/layouts/section-details-music';
import { SectionRelatedTracks } from '@/components/layouts/section-related-tracks';
import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function MusicSlugPage() {
  const params = useParams();
  const id = params.id;

  const [music, setMusics] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchMusics() {
      try {
        const response = await fetch("http://127.0.0.1:8000/query/sql", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: `SELECT id, track_name, track_artist, image_url FROM music WHERE id = ${id};` }),
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
    <div className='container mx-auto flex flex-col gap-y-4 py-6'>
      <h1 className='text-2xl'>Music</h1>
      <SectionDetailsMusic {...music[0]}/>
      <SectionRelatedTracks id={music[0]?.id ?? 1}/>
    </div>
  )
}