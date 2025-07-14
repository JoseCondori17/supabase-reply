'use client'
import { useRef, useState } from "react"
import { MusicIcon, XIcon } from "lucide-react"
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import { useFileStore } from "@/store/file-store"

export function ContentUploadMusic() {
  const inputRef = useRef<HTMLInputElement | null>(null)
  const [file, setFile] = useState<File | null>(null)
  const [progress, setProgress] = useState(0)
  const [uploading, setUploading] = useState(false)
  const { setFileServer } = useFileStore();

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile && selectedFile.type === "audio/mpeg") {
      setFile(selectedFile)
      uploadFile(selectedFile)
    } else {
      alert("Please select a valid MP3 file.")
    }
  }

  const uploadFile = async (file: File) => {
    setUploading(true)
    setProgress(0)

    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch("http://localhost:8000/query/upload-music", {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) throw new Error('Upload failed')

      const res = await response.json()
      setFileServer(res.data || "")
    } catch (error) {
      alert("Error uploading file")
    } finally {
      setUploading(false)
    }
  }
  
  const removeFile = () => {
    setFile(null)
    setProgress(0)
    setUploading(false)
  }

  return (
    <>
      <div
        className="flex flex-col h-48 items-center justify-center border-2 border-dashed border-gray-300 p-6 rounded-md cursor-pointer bg-gray-50 hover:bg-gray-100 transition"
        onClick={() => inputRef.current?.click()}
      >
        <Input
          type="file"
          accept="audio/mpeg"
          ref={inputRef}
          onChange={handleFileSelect}
          className="hidden"
        />
        <MusicIcon className="w-8 h-8 text-gray-400 mb-2" />
        <p className="text-sm text-gray-500">
          Click to upload MP3
        </p>
      </div>
      {file && (
        <div className="mt-4 border rounded-md p-4 relative">
          <Button
            variant="ghost"
            size="sm"
            onClick={removeFile}
            className="absolute top-2 right-2 text-gray-400 hover:text-red-500"
          >
            <XIcon className="w-4 h-4" />
          </Button>
          <p className="text-sm font-medium truncate mb-2">{file.name}</p>
          <div className="w-full bg-gray-200 h-2 rounded overflow-hidden">
            <div
              className="bg-blue-500 h-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-xs text-gray-500 mt-1">
            {uploading ? `Uploading... ${progress}%` : "Upload completed"}
          </p>
        </div>
      )}
    </>
  )
}