import { create } from "zustand"

interface FileState {
  fileServer: string
  setFileServer: (value: string) => void
}

export const useFileStore = create<FileState>((set) => ({
  fileServer: "",
  setFileServer: (value) => set({ fileServer: value }),
}))