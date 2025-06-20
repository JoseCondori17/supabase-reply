'use client'
import { useState } from "react";
import { Music } from "@/interfaces/music.interface";
import { PlayMusic } from "@/components/common/play-music";

export function SectionDetailsMusic({
  name,
  author,
  music_url,
  year,
  genre,
  label,
  bmp,
  image_url
}: Music) {
  const [imageError, setImageError] = useState(false);
  const fallbackMusicImage = "@/assets/image/fallback-music.jpg";
  return (
    <section className="container mx-auto px-24 py-10 grid grid-cols-3 gap-2">
      <div className="flex items-center justify-start">
        <img
          src={imageError ? fallbackMusicImage : image_url}
          alt={`${name} cover`}
          width={300}
          height={300}
          className="rounded-lg object-cover w-60 h-64"
          onError={() => setImageError(true)}
        />
      </div>
      <div className="flex flex-col gap-y-2 items-start">
        <h1 className="font-bold text-4xl">{name}</h1>
        <span className="text-muted-foreground">by {author}</span>
        <PlayMusic src="/music/test.mp3" />
      </div>
      <div className="grid grid-rows-2 justify-start">
        <div className="flex gap-x-20">
          <div className="flex flex-col gap-y-2">
            <span className="text-sm font-bold text-muted-foreground">YEAR</span>
            <span>{year}</span>
          </div>
          <div className="flex flex-col gap-y-2">
            <span className="text-sm font-bold text-muted-foreground">GENRE</span>
            <span>{genre}</span>
          </div>
        </div>
        <div className="flex gap-x-20">
          <div className="flex flex-col gap-y-2">
            <span className="text-sm font-bold text-muted-foreground">BPM</span>
            <span>{bmp}</span>
          </div>
          <div className="flex flex-col gap-y-2">
            <span className="text-sm font-bold text-muted-foreground">LABEL</span>
            <span>{label}</span>
          </div>
        </div>
      </div>
    </section>
  );
}