import { Header } from "@/components/layouts/header";
import { SectionDetailsMusic } from "@/components/layouts/section-details-music";
import { SectionRelatedTracks } from "@/components/layouts/section-related-tracks";
import { Separator } from "@/components/ui/separator";
import { musicList } from "@/constants/music";

export default function Home() {
  return (
    <div className="flex flex-col h-screen w-screen">
      <Header />
      <Separator />
      <SectionDetailsMusic {...musicList[0]} />
      <SectionRelatedTracks />
    </div>
  );
}
