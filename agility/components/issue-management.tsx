"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Check, X, Edit } from "lucide-react"

interface Issue {
  id: string
  title: string
  description: string
}

interface IssueManagementProps {
  issues: Issue[]
  onAcceptIssue: (id: string) => void
  onRejectIssue: (id: string) => void
  onModifyIssue: (id: string, newTitle: string, newDescription: string) => void
}

export function IssueManagement({ issues, onAcceptIssue, onRejectIssue, onModifyIssue }: IssueManagementProps) {
  const [editingIssue, setEditingIssue] = useState<string | null>(null)
  const [editTitle, setEditTitle] = useState("")
  const [editDescription, setEditDescription] = useState("")

  const handleModify = (issue: Issue) => {
    setEditingIssue(issue.id)
    setEditTitle(issue.title)
    setEditDescription(issue.description)
  }

  const handleSaveModification = (id: string) => {
    onModifyIssue(id, editTitle, editDescription)
    setEditingIssue(null)
  }

  return (
    <div className="h-full flex flex-col">
      <h2 className="text-xl font-bold mb-4 px-4 py-3 border-b">Issues</h2>
      <div className="space-y-4 overflow-y-auto flex-grow">
        {[
          { id: "1", title: "Implement user authentication", description: "Create a secure login system for users." },
          { id: "2", title: "Design responsive UI", description: "Ensure the application is mobile-friendly." },
          {
            id: "3",
            title: "Integrate with backend API",
            description: "Connect frontend components with backend services.",
          },
          {
            id: "4",
            title: "Implement data caching",
            description: "Improve performance by caching frequently accessed data.",
          },
          {
            id: "5",
            title: "Add user profile management",
            description: "Allow users to view and edit their profile information.",
          },
          {
            id: "6",
            title: "Implement role-based access control",
            description: "Set up different access levels for various user roles.",
          },
        ].map((issue) => (
          <Card key={issue.id} className="text-sm">
            <CardHeader className="py-3">
              {editingIssue === issue.id ? (
                <Input value={editTitle} onChange={(e) => setEditTitle(e.target.value)} className="text-sm" />
              ) : (
                <CardTitle className="text-sm font-medium">{issue.title}</CardTitle>
              )}
            </CardHeader>
            <CardContent className="py-2">
              {editingIssue === issue.id ? (
                <Textarea
                  value={editDescription}
                  onChange={(e) => setEditDescription(e.target.value)}
                  className="min-h-[60px] text-sm"
                />
              ) : (
                <p className="text-sm">{issue.description}</p>
              )}
            </CardContent>
            <CardFooter className="py-2 flex justify-end space-x-1">
              {editingIssue === issue.id ? (
                <>
                  <Button
                    onClick={() => setEditingIssue(null)}
                    variant="outline"
                    size="sm"
                    className="h-8 px-2 text-xs"
                  >
                    <X className="w-3 h-3 mr-1" />
                    Cancel
                  </Button>
                  <Button onClick={() => handleSaveModification(issue.id)} size="sm" className="h-8 px-2 text-xs">
                    <Check className="w-3 h-3 mr-1" />
                    Save
                  </Button>
                </>
              ) : (
                <>
                  <Button
                    onClick={() => onRejectIssue(issue.id)}
                    variant="outline"
                    size="sm"
                    className="h-8 px-2 text-xs"
                  >
                    <X className="w-3 h-3 mr-1" />
                    Reject
                  </Button>
                  <Button onClick={() => handleModify(issue)} variant="outline" size="sm" className="h-8 px-2 text-xs">
                    <Edit className="w-3 h-3 mr-1" />
                    Modify
                  </Button>
                  <Button onClick={() => onAcceptIssue(issue.id)} size="sm" className="h-8 px-2 text-xs">
                    <Check className="w-3 h-3 mr-1" />
                    Accept
                  </Button>
                </>
              )}
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  )
}

