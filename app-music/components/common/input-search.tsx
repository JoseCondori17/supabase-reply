'use client'
import { cn } from "@/lib/utils"
import { SearchIcon } from "lucide-react"
import { useEffect, useState } from "react"
import { Input } from "../ui/input"

export function InputSearch({
  onSearch
}: {
  onSearch?: (query: string) => void
}) {
  const [query, setQuery] = useState("")
  const [debouncedQuery, setDebouncedQuery] = useState("")

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(query)
    }, 400)

    return () => clearTimeout(handler)
  }, [query, 400])

  useEffect(() => {
    if (onSearch) onSearch(debouncedQuery)
  }, [debouncedQuery, onSearch])

  return (
    <div className="relative w-full max-w-sm">
      <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground pointer-events-none" />
      <Input
        type="search"
        placeholder="Search..."
        value={query}

        onChange={(e) => setQuery(e.target.value)}
        className={cn("pl-10 h-8")}
      />
    </div>
  )
}