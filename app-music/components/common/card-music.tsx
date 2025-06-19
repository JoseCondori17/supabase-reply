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

interface Music {
  id: string;
  name: string;
  author: string;
  image_url: string;
  bmp: number;
}

export function CardMusic({
  id,
  name,
  author,
  image_url,
  bmp
}: Music) {
  const [imageError, setImageError] = useState(false);
  const fallbackMusicImage = "@/assets/image/fallback-music.jpg";

  return (
    <Card className="rounded-lg py-3">
      <CardContent className="flex flex-col gap-y-4 px-3">
      <div className="relative group w-fit">
        <img
          src={imageError ? fallbackMusicImage : image_url}
          alt={`${name} cover`}
          width={300}
          height={300}
          className="rounded-lg object-cover w-full h-64"
          onError={() => setImageError(true)}
        />
        <Button
          size="icon"
          className="rounded-full absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        >
          <PlayIcon />
        </Button>
      </div>
        <div className="flex justify-between items-start">
          <div className="flex flex-col gap-y-1">
            <CardTitle>{name}</CardTitle>
            <CardDescription>by {author}</CardDescription>
          </div>
          <span className="text-sm font-bold text-muted-foreground">{bmp} bpms</span>
        </div>
      </CardContent>
    </Card>
  );
}