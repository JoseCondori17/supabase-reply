'use client'
import { useRef, useState } from 'react'
import { Button } from '../ui/button'
import { MicIcon } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useFileStore } from '@/store/file-store'

export function ButtonAudioRecorder() {
  const [isRecording, setIsRecording] = useState(false)
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null)
  const { setFileServer } = useFileStore()
  const chunks = useRef<Blob[]>([])

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const recorder = new MediaRecorder(stream)

    recorder.ondataavailable = (e) => {
      chunks.current.push(e.data)
    }

    recorder.onstop = async () => {
      const blob = new Blob(chunks.current, { type: 'audio/webm' })
      chunks.current = []

      const formData = new FormData()
      formData.append('file', blob, 'recording.webm')

      const response = await fetch("http://localhost:8000/query/record-audio", {
        method: 'POST',
        body: formData,
      })

      const res = await response.json()
      setFileServer(res.data || "")
    }

    recorder.start()
    setMediaRecorder(recorder)
    setIsRecording(true)
  }

  const stopRecording = () => {
    mediaRecorder?.stop()
    mediaRecorder?.stream.getTracks().forEach((track) => track.stop())
    setIsRecording(false)
  }

  return (
    <Button
      variant={isRecording ? "destructive" : "outline"}
      size="icon"
      onClick={() => isRecording ? stopRecording() : startRecording()}
      className={cn(
        'h-8 w-8 transition-all duration-300',
        isRecording && 'animate-pulse',
        'focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-red-500'
      )}
    >
      <MicIcon
        className={cn(
          'size-4',
          isRecording && 'text-white animate-pulse'
        )}
      />
    </Button>
  )
}