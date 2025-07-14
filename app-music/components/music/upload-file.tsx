import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
  DialogFooter,
} from "@/components/ui/dialog"
import { UploadCloudIcon } from "lucide-react"
import { ContentUploadMusic } from "./content-upload-music"
import { useState } from "react"

export function UploadFile() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [open, setOpen] = useState(false)

  const handleContinue = () => {
    if (selectedFile) {
      setIsUploading(true)
    }
  }

  const handleDialogClose = () => {
    setOpen(false)
    setSelectedFile(null)
    setIsUploading(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button size="icon" variant="outline" className="h-8 w-8">
          <UploadCloudIcon className="size-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="select-none">
        <DialogHeader>
          <DialogTitle>Sube una música</DialogTitle>
          <DialogDescription>
            No olvides subir solo en formato MP3 (max. 5 MB) y mira la magia.
          </DialogDescription>
        </DialogHeader>

        <ContentUploadMusic
          onFileSelect={setSelectedFile}
          isUploading={isUploading}
          onUploadComplete={(success) => {
            setIsUploading(false)
            if (success) {
              setOpen(false)
              setSelectedFile(null)
            }
          }}
        />

        <DialogFooter>
          <DialogClose asChild>
            <Button
              variant="outline"
              size="sm"
              onClick={handleDialogClose}
              disabled={isUploading}
            >
              Cancel
            </Button>
          </DialogClose>
          <Button
            size="sm"
            onClick={handleContinue}
            disabled={!selectedFile || isUploading}
          >
            {isUploading ? "Cargando..." : "Continue"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}