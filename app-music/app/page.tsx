'use client'
import { SectionPreviewMusic } from "@/components/layouts/section-preview-music";
import { SectionGenreMusic } from "@/components/layouts/section-genre-music";
import { SectionAuthorMusic } from "@/components/layouts/section-author-music";
import { useSearchStore } from "@/store/search-store";
import { SectionSearchMusic } from "@/components/layouts/section-search-music";
export default function Home() {
  const { query } = useSearchStore();
  const isSearching = query.trim() !== "";

  return (
    <div className="p-4">
      {isSearching ? (
        <SectionSearchMusic query={query}/>
      ) : (
        <div className="flex flex-col gap-y-4">
          <SectionPreviewMusic />
          <SectionGenreMusic />
          <SectionAuthorMusic />
        </div>
      )}
    </div>
  );
}