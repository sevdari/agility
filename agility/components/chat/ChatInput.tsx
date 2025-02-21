import React, { useState } from "react";

interface ChatMessage {
  sender: "user" | "bot";
  text: string;
}

/**
 * ChatInput Component:
 * 
 * - Accepts an epic prompt from the user.
 * - When send is pressed, it calls /api/epic/generate with the user prompt.
 * - The returned summary is appended as the bot reply, and the generated epic content is shown along with an Accept button.
 * - When Accept is pressed, the epic_content is sent to /api/issue/generate.
 * - The list of generated issues and their summary is then added to the chat.
 */
export default function ChatInput() {
  const [inputText, setInputText] = useState("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [epicResponse, setEpicResponse] = useState<{ epic_id: number; epic_content: string; proposed_content?: string } | null>(null);
  const [isAcceptVisible, setAcceptVisible] = useState(false);
  const [isGenerating, setGenerating] = useState(false);

  // Handler for sending the epic prompt.
  const handleSend = async () => {
    if (!inputText.trim()) return;
    // Append the user's epic prompt to the chat history.
    setChatHistory(prev => [...prev, { sender: "user", text: inputText }]);
    setGenerating(true);
    try {
      const res = await fetch("/api/epic/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ user_prompt: inputText })
      });
      const data = await res.json();
      // data contains: { epic: { epic_id, epic_content, ...}, summary }
      setChatHistory(prev => [
        ...prev,
        { sender: "bot", text: data.summary }
      ]);
      // Save the epic response and show the Accept button.
      setEpicResponse(data.epic);
      setAcceptVisible(true);
    } catch (error) {
      console.error("Error generating epic:", error);
      setChatHistory(prev => [
        ...prev,
        { sender: "bot", text: "Error generating epic." }
      ]);
    }
    setGenerating(false);
    // Reset the prompt.
    setInputText("");
  };

  // Handler for accepting the generated epic. This sends the epic content to the issue generation API.
  const handleAcceptEpic = async () => {
    if (!epicResponse || !epicResponse.epic_content) return;
    setGenerating(true);
    try {
      const res = await fetch("/api/issue/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        // Use the generated epic content as the user prompt for issue generation.
        body: JSON.stringify({ user_prompt: epicResponse.epic_content })
      });
      const issueData = await res.json();
      // issueData contains: { issues: [...], summary }.
      let issuesText = issueData.summary + "\n\n";
      issueData.issues.forEach((issue: any) => {
        issuesText += `Issue ${issue.issue_id}: ${issue.issue_title}\n${issue.issue_body}\n\n`;
      });
      setChatHistory(prev => [
        ...prev,
        { sender: "bot", text: issuesText }
      ]);
    } catch (error) {
      console.error("Error generating issues:", error);
      setChatHistory(prev => [
        ...prev,
        { sender: "bot", text: "Error generating issues." }
      ]);
    }
    setGenerating(false);
    // Hide the Accept button once the issues have been generated.
    setAcceptVisible(false);
  };

  return (
    <div className="p-4">
      <div className="chat-history mb-4 space-y-2">
        {chatHistory.map((msg, idx) => (
          <div
            key={idx}
            className={msg.sender === "user" ? "text-right" : "text-left"}
          >
            <pre className="whitespace-pre-wrap">{msg.text}</pre>
          </div>
        ))}
      </div>
      {isAcceptVisible && epicResponse && (
        <div className="epic-review mb-4">
          <h3 className="mb-2 font-bold">Generated Epic:</h3>
          <div className="epic-content p-4 border rounded mb-2">
            <pre className="whitespace-pre-wrap">{epicResponse.epic_content}</pre>
          </div>
          <button
            onClick={handleAcceptEpic}
            disabled={isGenerating}
            className="bg-primary text-primary-foreground px-4 py-2 rounded"
          >
            Accept Epic and Generate Issues
          </button>
        </div>
      )}
      <textarea
        className="w-full p-2 border rounded mb-2"
        rows={3}
        placeholder="Enter epic prompt here..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      <button
        onClick={handleSend}
        disabled={isGenerating || !inputText.trim()}
        className="bg-primary text-primary-foreground px-4 py-2 rounded"
      >
        Send
      </button>
    </div>
  );
} 