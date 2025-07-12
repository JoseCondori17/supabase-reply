import { Separator } from "@/components/ui/separator";
import { Header } from "@/components/layouts/header";
import { SectionPreviewMusic } from "@/components/layouts/section-preview-music";
import { SectionGenreMusic } from "@/components/layouts/section-genre-music";
import { SectionAuthorMusic } from "@/components/layouts/section-author-music";

export default function Home() {
  return (
    <div className="flex flex-col h-screen w-full">
      <Header />
      <Separator />
      <SectionPreviewMusic/>
      <SectionGenreMusic/>
      <SectionAuthorMusic/>
    </div>
  );
}
