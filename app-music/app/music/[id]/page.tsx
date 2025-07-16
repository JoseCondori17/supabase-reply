'use client'
import { SectionDetailsMusic } from '@/components/layouts/section-details-music'
import { SectionRelatedTracks } from '@/components/layouts/section-related-tracks'
import { LoaderCircle } from 'lucide-react'
import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function MusicSlugPage() {
  const params = useParams()
  const id = params.id

  const [music, setMusic] = useState<any | null>(null)
  const [related, setRelated] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      try {
        const [mainRes, relatedRes] = await Promise.all([
          fetch("http://127.0.0.1:8000/query/sql", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: `SELECT id, track_name, track_artist, path_download_wav, lyrics, image_url FROM music WHERE id = ${id};` }),
          }),
          fetch(`http://127.0.0.1:8000/query/top/${id}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: "SELECT id, track_name, track_artist, image_url FROM music LIMIT 5;" }),
          }),
        ])

        const mainResult = await mainRes.json()
        const relatedResult = await relatedRes.json()

        if (mainResult.success) setMusic(mainResult.data[0])
        if (relatedResult.success) setRelated(relatedResult.data)
      } catch (err) {
        console.error("Error fetching data:", err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading || !music) {
    return (
      <div className="h-full flex-1 flex items-center justify-center">
        <LoaderCircle className="w-6 h-6 animate-spin text-gray-500" />
      </div>
    )
  }

  return (
    <div className="container mx-auto flex flex-col gap-y-4 py-6">
      <SectionDetailsMusic {...music} />
      <SectionRelatedTracks items={related} />
    </div>
  )
}