'use client'
import { SectionPreviewMusic } from "@/components/layouts/section-preview-music";
import { SectionGenreMusic } from "@/components/layouts/section-genre-music";
import { SectionAuthorMusic } from "@/components/layouts/section-author-music";
import { useSearchStore } from "@/store/search-store";
import { SectionSearchMusic } from "@/components/layouts/section-search-music";
import { useFileStore } from "@/store/file-store";
import { SectionRelatedTracksFile } from "@/components/layouts/section-related-tracks-file";
export default function Home() {
  const { query } = useSearchStore();
  const { fileServer } = useFileStore();
  const isSearching = query.trim() !== "";
  const isExistFileServer = fileServer.trim() !== "";

  return (
    <div className="p-4">
      {isExistFileServer ? (
        <div className="flex items-center justify-center h-[50vh]">
          <SectionRelatedTracksFile filepath={fileServer} />
        </div>
      ) : isSearching ? (
        <SectionSearchMusic query={query} />
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