"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Pencil, Check, X } from "lucide-react"

interface EditableEpicHeaderProps {
  initialText: string
  onSave: (newText: string) => void
}

export function EditableEpicHeader({ initialText, onSave }: EditableEpicHeaderProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [text, setText] = useState(initialText)

  const handleSave = () => {
    onSave(text)
    setIsEditing(false)
  }

  const handleCancel = () => {
    setText(initialText)
    setIsEditing(false)
  }

  if (isEditing) {
    return (
      <div className="flex items-center space-x-2">
        <Input
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="text-2xl font-bold font-crimson"
          autoFocus
        />
        <Button size="icon" onClick={handleSave}>
          <Check className="h-4 w-4" />
        </Button>
        <Button size="icon" variant="outline" onClick={handleCancel}>
          <X className="h-4 w-4" />
        </Button>
      </div>
    )
  }

  return (
    <div className="flex items-center space-x-2">
      <h1 className="text-3xl font-crimson tracking-normal">{text}</h1>
      <Button size="icon" variant="ghost" onClick={() => setIsEditing(true)}>
        <Pencil className="h-4 w-4" />
      </Button>
    </div>
  )
}

