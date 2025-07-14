'use client'
import { useRef, useState, useEffect } from "react"
import { MusicIcon, XIcon } from "lucide-react"
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import { useFileStore } from "@/store/file-store"

interface ContentUploadMusicProps {
  onFileSelect: (file: File | null) => void
  isUploading: boolean
  onUploadComplete: (success: boolean) => void
}

export function ContentUploadMusic({
  onFileSelect,
  isUploading,
  onUploadComplete
}: ContentUploadMusicProps) {
  const inputRef = useRef<HTMLInputElement | null>(null)
  const [file, setFile] = useState<File | null>(null)
  const [progress, setProgress] = useState(0)
  const { setFileServer } = useFileStore()

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile && selectedFile.type === "audio/mpeg") {
      setFile(selectedFile)
      onFileSelect(selectedFile)
    } else {
      alert("Please select a valid MP3 file.")
    }
  }

  const uploadFile = async (file: File) => {
    setProgress(0)
    const formData = new FormData()
    formData.append("file", file)

    const xhr = new XMLHttpRequest()

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percentComplete = Math.round((event.loaded / event.total) * 100)
        setProgress(percentComplete)
      }
    }

    xhr.onload = () => {
      if (xhr.status === 201) {
        const res = JSON.parse(xhr.responseText)
        setFileServer(res.data)
        onUploadComplete(true)
      } else {
        alert("Upload failed")
        onUploadComplete(false)
      }
    }

    xhr.onerror = () => {
      alert("Upload error")
      onUploadComplete(false)
    }

    xhr.open("POST", "http://localhost:8000/query/upload-music")
    xhr.send(formData)
  }

  // Efecto para iniciar la subida cuando isUploading se vuelve true
  useEffect(() => {
    if (isUploading && file) {
      uploadFile(file)
    }
  }, [isUploading, file])

  const removeFile = () => {
    setFile(null)
    setProgress(0)
    onFileSelect(null)
  }

  return (
    <>
      <div
        className="flex flex-col h-48 items-center justify-center border-2 border-dashed border-gray-300 p-6 rounded-md cursor-pointer bg-gray-50 hover:bg-gray-100 transition"
        onClick={() => !isUploading && inputRef.current?.click()}
      >
        <Input
          type="file"
          accept="audio/mpeg"
          ref={inputRef}
          onChange={handleFileSelect}
          className="hidden"
          disabled={isUploading}
        />
        <MusicIcon className="w-8 h-8 text-gray-400 mb-2" />
        <p className="text-sm text-gray-500">
          {isUploading ? "Subiendo archivo..." : "Click to upload MP3"}
        </p>
      </div>

      {file && (
        <div className="mt-4 border rounded-md p-4 relative">
          <Button
            variant="ghost"
            size="sm"
            onClick={removeFile}
            className="absolute top-2 right-2 text-gray-400 hover:text-red-500"
            disabled={isUploading}
          >
            <XIcon className="w-4 h-4" />
          </Button>
          <p className="text-sm font-medium truncate mb-2">{file.name}</p>

          {isUploading && (
            <>
              <div className="w-full bg-gray-200 h-2 rounded overflow-hidden">
                <div
                  className="bg-blue-500 h-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Subiendo... {progress}%
              </p>
            </>
          )}

          {!isUploading && (
            <p className="text-xs text-gray-500 mt-1">
              Archivo listo para subir
            </p>
          )}
        </div>
      )}
    </>
  )
}