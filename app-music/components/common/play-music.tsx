import { useEffect, useRef, useState } from "react";
import { Howl } from "howler";
import { Button } from "@/components/ui/button";
import { Play, StopCircle } from "lucide-react";

interface PlayMusicProps {
  src: string;
}

export function PlayMusic({ src }: PlayMusicProps) {
  const soundRef = useRef<Howl | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    soundRef.current = new Howl({
      src: [src],
      html5: true,
      onend: () => {
        setIsPlaying(false);
        setProgress(0);
        if (intervalRef.current) clearInterval(intervalRef.current);
      },
    });

    return () => {
      if (soundRef.current) {
        soundRef.current.unload();
      }
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [src]);

  const handlePlay = () => {
    if (soundRef.current) {
      soundRef.current.play();
      setIsPlaying(true);

      intervalRef.current = setInterval(() => {
        if (soundRef.current) {
          const duration = soundRef.current.duration();
          const seek = soundRef.current.seek() as number;
          setProgress((seek / duration) * 100);
        }
      }, 500);
    }
  };

  const handleStop = () => {
    if (soundRef.current) {
      soundRef.current.stop();
      setIsPlaying(false);
      setProgress(0);
      if (intervalRef.current) clearInterval(intervalRef.current);
    }
  };

  return (
    <div className="flex flex-col gap-2 w-full">
      <div className="flex items-center gap-2">
        <Button size="icon" onClick={isPlaying ? handleStop : handlePlay}>
          {isPlaying ? <StopCircle className="w-5 h-5" /> : <Play className="w-5 h-5" />}
        </Button>
        {/* <Slider
          className="w-full"
          value={[progress]}
          max={100}
          step={0.1}
          onValueChange={() => {}}
        /> */}
      </div>
    </div>
  );
}