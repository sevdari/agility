import { streamText } from "ai"
import { openai } from "@ai-sdk/openai"

export async function POST(req: Request) {
  const { prompt } = await req.json()

  const result = await streamText({
    model: openai("gpt-4o-mini"),
    system:
      "You are an AI assistant specialized in creating concise and effective project epics based on user input. Generate a short, clear epic title that captures the essence of the user's request.",
    messages: [{ role: "user", content: prompt }],
  })

  const epic = await result.text

  return new Response(JSON.stringify({ epic }), {
    headers: { "Content-Type": "application/json" },
  })
}

