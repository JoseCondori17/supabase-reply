'use client'
import {
  Card,
  CardContent,
  CardDescription,
  CardTitle
} from "@/components/ui/card";
import { useState } from "react";
import { Button } from "../ui/button";
import { PlayIcon } from "lucide-react";
import Link from "next/link";

interface Music {
  id: string;
  track_name: string;
  track_artist: string;
  image_url: string;
}

export function CardPreviewMusic({
  id,
  track_name,
  track_artist,
  image_url,
}: Music) {
  const [imageError, setImageError] = useState(false);
  const fallbackMusicImage = "@/assets/image/fallback-music.jpg";

  return (
    <Card className="rounded-lg py-3">
      <CardContent className="flex flex-col gap-y-4 px-3">
        <div className="relative group w-fit">
          <img
            src={imageError ? fallbackMusicImage : image_url}
            alt={`${track_name} cover`}
            width={300}
            height={300}
            className="rounded-lg object-cover w-full h-60"
            onError={() => setImageError(true)}
          />
          <Link href={`/music/${id}`}>
            <Button
              size="icon"
              className="rounded-full absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
            >
              <PlayIcon />
            </Button>
          </Link>
        </div>
        <div className="flex justify-between items-start">
          <div className="flex flex-col gap-y-1">
            <CardTitle>{track_name}</CardTitle>
            <CardDescription>by {track_artist}</CardDescription>
          </div>
          {/* <span className="text-sm font-bold text-muted-foreground">{bmp} bpms</span> */}
        </div>
      </CardContent>
    </Card>
  );
}