"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { cn } from "@/lib/utils"
import { useChat } from "ai/react"
import { FolderIcon, Plus, MessageSquare, ChevronRight, Search, MoreHorizontal, Mic, ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { AutoResizeTextarea } from "@/components/autoresize-textarea"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { EditableEpicHeader } from "@/components/editable-epic-header"
import { InitialView } from "@/components/initial-view"
import { AnimatePresence, motion } from "framer-motion"
import { EpicAcceptance } from "@/components/epic-acceptance"
import { IssueManagement } from "@/components/issue-management"

const exampleProjects = [
  {
    id: 1,
    name: "Website Redesign",
    lastUpdated: "2 hours ago",
    epics: [
      { id: "e1", name: "User Authentication" },
      { id: "e2", name: "Dashboard UI" },
    ],
  },
  {
    id: 2,
    name: "Mobile App",
    lastUpdated: "1 day ago",
    epics: [{ id: "e3", name: "Offline Mode" }],
  },
  {
    id: 3,
    name: "API Integration",
    lastUpdated: "3 days ago",
    epics: [{ id: "e4", name: "Third-party APIs" }],
  },
]

const previousChats = [
  { id: 1, name: "Chat about React", date: "Today" },
  { id: 2, name: "NextJS Discussion", date: "Yesterday" },
  { id: 3, name: "API Design Chat", date: "2 days ago" },
]

export function ChatForm({ className, ...props }: React.ComponentProps<"form">) {
  const { messages, input, setInput, append, setMessages } = useChat({
    api: "/api/chat",
  })
  const [selectedProject, setSelectedProject] = useState<number | null>(null)
  const [selectedEpic, setSelectedEpic] = useState<string | null>(null)
  const [openProjects, setOpenProjects] = useState<number[]>([])
  const [epicContent, setEpicContent] = useState("")
  const [isInitialView, setIsInitialView] = useState(true)
  const [isEpicAccepted, setIsEpicAccepted] = useState(false)
  const [isIssueView, setIsIssueView] = useState(false)
  const [issues, setIssues] = useState<{ id: string; title: string; description: string }[]>([])
  const [previousMessages, setPreviousMessages] = useState<typeof messages>([])
  const chatContainerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
    }
  }, [chatContainerRef]) //Corrected dependency

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!input.trim()) return

    if (isInitialView) {
      setIsInitialView(false)
      // Generate epic from first message
      setEpicContent("New Epic: " + input.split("\n")[0])
    }

    await append({ content: input, role: "user" })
    setInput("")
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e as unknown as React.FormEvent<HTMLFormElement>)
    }
  }

  const toggleProject = (projectId: number) => {
    setOpenProjects((prev) => (prev.includes(projectId) ? prev.filter((id) => id !== projectId) : [...prev, projectId]))
  }

  const selectEpic = (projectId: number, epicId: string) => {
    setSelectedProject(projectId)
    setSelectedEpic(epicId)
    setMessages([]) // Clear previous messages
    const selectedEpic = exampleProjects.find((p) => p.id === projectId)?.epics.find((e) => e.id === epicId)
    if (selectedEpic) {
      setEpicContent(selectedEpic.name)
      append({
        content: `Let's discuss the epic: ${selectedEpic.name}. How can I assist you with this epic?`,
        role: "assistant",
      })
    }
  }

  const handleAcceptEpic = () => {
    setIsEpicAccepted(true)
    setIsIssueView(true)
    setPreviousMessages(messages)
    setMessages([])
    // Generate issues based on the epic
    setIssues([
      { id: "1", title: "Implement user authentication", description: "Create a secure login system for users." },
      { id: "2", title: "Design responsive UI", description: "Ensure the application is mobile-friendly." },
      {
        id: "3",
        title: "Integrate with backend API",
        description: "Connect frontend components with backend services.",
      },
    ])
  }

  const handleModifyEpic = () => {
    // Logic for modifying the epic
  }

  const handleAcceptAllIssues = () => {
    // Logic for accepting all issues
  }

  const handleAcceptIssue = (id: string) => {
    // Logic for accepting a single issue
  }

  const handleRejectIssue = (id: string) => {
    // Logic for rejecting a single issue
  }

  const handleModifyIssue = (id: string, newTitle: string, newDescription: string) => {
    setIssues((prevIssues) =>
      prevIssues.map((issue) => (issue.id === id ? { ...issue, title: newTitle, description: newDescription } : issue)),
    )
  }

  const handleBackToEpicChat = () => {
    setIsIssueView(false)
    setIsEpicAccepted(false)
    setMessages(previousMessages)
  }

  const messageList = (
    <motion.div
      className="flex flex-col gap-6 py-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      {messages.map((message, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className={cn("flex", message.role === "user" ? "justify-end" : "justify-start")}
        >
          <div
            className={cn(
              "max-w-[80%] rounded-lg px-4 py-2 text-base",
              message.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted",
            )}
          >
            {message.content}
          </div>
        </motion.div>
      ))}
    </motion.div>
  )

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="bg-white text-foreground w-64 min-h-screen flex flex-col border-r border-gray-200 fixed left-0 top-0">
        <div className="p-4 border-b">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-xl font-bold text-primary">Agility</h1>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="h-8 w-8">
                  <Plus className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                {previousChats.map((chat) => (
                  <DropdownMenuItem key={chat.id} className="flex items-center gap-2">
                    <MessageSquare className="h-4 w-4" />
                    <div className="flex flex-col">
                      <span className="text-sm">{chat.name}</span>
                      <span className="text-xs text-muted-foreground">{chat.date}</span>
                    </div>
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <nav className="space-y-1">
            <a href="#" className="text-primary block py-2">
              Chat
            </a>
            <a href="#" className="hover:text-primary block py-2">
              Projects
            </a>
          </nav>
        </div>

        {/* Projects Section */}
        <div className="flex-1 overflow-auto p-4">
          <h2 className="text-sm font-semibold text-muted-foreground mb-3">Projects</h2>
          <div className="space-y-2">
            {exampleProjects.map((project) => (
              <Collapsible
                key={project.id}
                open={openProjects.includes(project.id)}
                onOpenChange={() => toggleProject(project.id)}
              >
                <CollapsibleTrigger className="w-full">
                  <div
                    className={cn(
                      "flex items-center gap-2 p-2 rounded-lg text-left text-sm transition-colors",
                      selectedProject === project.id ? "bg-primary/10 text-primary" : "hover:bg-muted",
                    )}
                  >
                    <ChevronRight
                      className={cn("h-4 w-4 transition-transform", openProjects.includes(project.id) && "rotate-90")}
                    />
                    <FolderIcon className="h-4 w-4" />
                    <div className="flex flex-col">
                      <span>{project.name}</span>
                      <span className="text-xs text-muted-foreground">{project.lastUpdated}</span>
                    </div>
                  </div>
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <div className="ml-9 mt-1 space-y-1">
                    {project.epics.map((epic) => (
                      <button
                        key={epic.id}
                        onClick={() => selectEpic(project.id, epic.id)}
                        className={cn(
                          "w-full text-left p-2 rounded-lg text-sm transition-colors",
                          selectedEpic === epic.id ? "bg-primary/10 text-primary" : "hover:bg-muted",
                        )}
                      >
                        {epic.name}
                      </button>
                    ))}
                  </div>
                </CollapsibleContent>
              </Collapsible>
            ))}
          </div>
        </div>

        {/* Bottom Navigation */}
        <div className="p-4 border-t">
          <nav className="space-y-1">
            <a href="#" className="hover:text-primary block py-2">
              Settings
            </a>
            <a href="#" className="hover:text-primary block py-2">
              Account
            </a>
          </nav>
        </div>
      </aside>

      {/* Main content */}
      <main
        className={cn("flex flex-col ml-64 flex-1", isEpicAccepted && !isInitialView && "mr-80", className)}
        {...props}
      >
        <AnimatePresence mode="wait">
          {!isInitialView && epicContent && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="fixed top-0 left-64 right-0 bg-background z-10 py-4 px-4 sm:px-6 lg:px-8 border-b"
            >
              {isEpicAccepted ? (
                <div className="flex items-center justify-between">
                  <EditableEpicHeader initialText={epicContent} onSave={setEpicContent} />
                  <Button onClick={handleBackToEpicChat} variant="outline" size="sm">
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Back to Epic Chat
                  </Button>
                </div>
              ) : (
                <EpicAcceptance epicContent={epicContent} onAccept={handleAcceptEpic} onModify={handleModifyEpic} />
              )}
            </motion.div>
          )}
        </AnimatePresence>

        <div className="flex flex-1 overflow-hidden">
          <div
            className={cn("h-full overflow-y-auto px-4 sm:px-6 lg:px-8", !isInitialView && "mt-[73px] mb-[89px]")}
            ref={chatContainerRef}
          >
            <AnimatePresence mode="wait">
              {isInitialView ? (
                <InitialView>
                  <div className="w-full max-w-3xl">
                    <div className="flex items-center gap-2 p-3 rounded-lg border bg-background">
                      <div className="flex gap-2">
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <Plus className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <Search className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </div>
                      <AutoResizeTextarea
                        onKeyDown={handleKeyDown}
                        onChange={(v) => setInput(v)}
                        value={input}
                        placeholder="Message Agility..."
                        className="flex-1 min-h-[32px] resize-none border-0 focus:ring-0 p-0 pl-2 placeholder:text-muted-foreground text-base"
                      />
                      <Button variant="ghost" size="icon" className="h-8 w-8">
                        <Mic className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </InitialView>
              ) : (
                messageList
              )}
            </AnimatePresence>
          </div>

          {/* Right Sidebar for Issues */}
          {isEpicAccepted && (
            <div className="w-80 border-l border-gray-200 overflow-hidden flex flex-col fixed right-0 top-0 bottom-0">
              <div className="overflow-y-auto flex-grow mt-[73px] mb-[89px]">
                <IssueManagement
                  issues={issues}
                  onAcceptIssue={handleAcceptIssue}
                  onRejectIssue={handleRejectIssue}
                  onModifyIssue={handleModifyIssue}
                />
              </div>
            </div>
          )}
        </div>

        {!isInitialView && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed bottom-0 left-64 right-0 border-t border-input bg-background py-4 px-4 sm:px-6 lg:px-8"
          >
            <div className="flex items-center max-w-3xl mx-auto gap-2">
              <div className="flex gap-2">
                <Button variant="ghost" size="icon" className="h-8 w-8">
                  <Plus className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon" className="h-8 w-8">
                  <Search className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon" className="h-8 w-8">
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </div>
              <AutoResizeTextarea
                onKeyDown={handleKeyDown}
                onChange={(v) => setInput(v)}
                value={input}
                placeholder="Message Agility..."
                className="flex-1 min-h-[32px] resize-none border-0 focus:ring-0 p-0 pl-2 placeholder:text-muted-foreground text-base"
              />
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <Mic className="h-4 w-4" />
              </Button>
            </div>
          </motion.div>
        )}
      </main>
    </div>
  )
}

