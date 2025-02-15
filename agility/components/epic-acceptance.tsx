import { Button } from "@/components/ui/button"
import { Pencil, Check } from "lucide-react"

interface EpicAcceptanceProps {
  epicContent: string
  onAccept: () => void
  onModify: () => void
}

export function EpicAcceptance({ epicContent, onAccept, onModify }: EpicAcceptanceProps) {
  return (
    <div className="flex items-center justify-between p-4 bg-background border-b">
      <h2 className="text-xl font-semibold">{epicContent}</h2>
      <div className="flex gap-2">
        <Button onClick={onModify} variant="outline" size="sm">
          <Pencil className="w-4 h-4 mr-2" />
          Modify
        </Button>
        <Button onClick={onAccept} size="sm">
          <Check className="w-4 h-4 mr-2" />
          Accept
        </Button>
      </div>
    </div>
  )
}

