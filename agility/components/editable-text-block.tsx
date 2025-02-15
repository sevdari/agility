"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { diffChars } from "diff"

interface EditableTextBlockProps {
  initialText: string
  onApprove: (newText: string) => void
}

export function EditableTextBlock({ initialText, onApprove }: EditableTextBlockProps) {
  const [text, setText] = useState(initialText)
  const [suggestedText, setSuggestedText] = useState<string | null>(null)

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value)
  }

  const renderDiff = () => {
    if (!suggestedText) return null

    const diff = diffChars(text, suggestedText)

    return (
      <div className="mt-4 p-4 bg-gray-100 rounded-md">
        <h3 className="text-lg font-semibold mb-2">Suggested Changes:</h3>
        <div>
          {diff.map((part, index) => (
            <span key={index} className={part.added ? "bg-green-200" : part.removed ? "bg-red-200" : ""}>
              {part.value}
            </span>
          ))}
        </div>
        <div className="mt-4 flex space-x-2">
          <Button
            onClick={() => {
              setText(suggestedText)
              onApprove(suggestedText)
              setSuggestedText(null)
            }}
          >
            Approve
          </Button>
          <Button variant="outline" onClick={() => setSuggestedText(null)}>
            Reject
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="mb-6">
      <Textarea
        value={text}
        onChange={handleTextChange}
        className="w-full p-4 text-lg border-2 border-primary rounded-md focus:ring-2 focus:ring-primary"
        rows={5}
      />
      {renderDiff()}
    </div>
  )
}

