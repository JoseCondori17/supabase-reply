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

export function UploadFile() {
  

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button size="icon" variant="outline" className="h-8 w-8" >
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
        <ContentUploadMusic />
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline" size="sm">Cancel</Button>
          </DialogClose>
          <DialogClose asChild>
            <Button size="sm">Continue</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}