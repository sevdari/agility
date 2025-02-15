import { type CoreMessage, streamText } from "ai"
import { openai } from "@ai-sdk/openai"
import { tools } from "@/app/lib/tools"

export async function POST(req: Request) {
  const { messages }: { messages: CoreMessage[] } = await req.json()

  const epicContent =
    messages.find((m) => m.role === "system" && m.content.startsWith("Current epic:"))?.content.split('"')[1] || ""

  const result = streamText({
    model: openai("gpt-4o-mini"),
    system:
      "You are a helpful assistant specializing in improving and refining project epics. When asked about the epic, provide suggestions to improve it or answer questions about it. Your suggestions should be clear, concise, and aimed at creating a well-defined and actionable epic.",
    messages: [
      { role: "system", content: `Current epic: "${epicContent}"` },
      ...messages.filter((m) => m.role !== "system"),
    ],
    tools,
  })

  return result.toDataStreamResponse()
}

