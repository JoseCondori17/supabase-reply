'use client'
import { useState } from "react";
import { Music } from "@/interfaces/music.interface";
import { ScrollArea } from "../ui/scroll-area";
import { PlayMusic } from "@/components/common/play-music";

export function SectionDetailsMusic({
  id,
  track_name,
  track_artist,
  path_download_wav,
  lyrics,
  image_url,
}: Music) {
  const [imageError, setImageError] = useState(false);
  const fallbackMusicImage = "@/assets/image/fallback-music.jpg";
  return (
    <section className="container mx-auto px-24 py-10 grid grid-cols-3 gap-2">
      <div className="flex items-center justify-start">
        <img
          src={imageError ? fallbackMusicImage : image_url}
          alt={`${track_name} cover`}
          width={300}
          height={300}
          className="rounded-lg object-cover w-60 h-64"
          onError={() => setImageError(true)}
        />
      </div>
      <div className="flex flex-col gap-y-2 items-start">
        <h1 className="font-bold text-4xl">{track_name}</h1>
        <span className="text-muted-foreground">by {track_artist}</span>
        <PlayMusic src={`${path_download_wav}`} />
      </div>
      <div className="w-full max-w-sm">
        <h2 className="text-md font-semibold mb-2 text-muted-foreground">Letra</h2>
        <ScrollArea className="h-[200px] w-full rounded-md py-4 pr-2">
          {lyrics.split('\n').map((line, idx) => (
            <p key={idx} className="text-gray-700">{line}</p>
          ))}
        </ScrollArea>
      </div>
    </section>
  );
}