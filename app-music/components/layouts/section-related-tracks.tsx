'use client'
import { CardPreviewMusic } from "../common/card-preview"

export function SectionRelatedTracks({ items }: { items: any[] }) {
  return (
    <div className="container mx-auto px-24 py-6 flex flex-col gap-y-8">
      <div className="flex items-center gap-x-6">
        <h2 className="text-2xl align-top">Related Tracks</h2>
      </div>
      <div className="grid grid-cols-5 gap-4">
        {items.map((item, idx) => (
          <CardPreviewMusic key={idx} {...item} />
        ))}
      </div>
    </div>
  )
}