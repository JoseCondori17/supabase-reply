import { musicList } from "@/constants/music";
import { Button } from "../ui/button";
import { CardMusic } from "../common/card-music";

export function SectionRelatedTracks() {
  return (
    <div className="container mx-auto px-24 py-6 flex flex-col gap-y-8">
      <div className="flex items-center gap-x-6">
        <h2 className="text-2xl align-top">Related Tracks</h2>
        <Button size='sm' variant='outline'>View all</Button>
      </div>
      <div className="grid grid-cols-5 gap-4">
        {musicList.map((item) => (
          <CardMusic
            id="a"
            name={item.name}
            author={item.author}
            image_url={item.image_url}
            bmp={item.bmp}
            key={item.id}
          />
        ))}
      </div>
    </div>
  );
}