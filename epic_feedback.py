import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_epic_feedback(current_epic, user_feedback):
    """
    Generates a proposed updated epic based on the current epic and the user feedback.
    The LLM should provide:
      - A revised (proposed) epic statement that incorporates the feedback.
      - A summary outlining the changes and the reasoning behind them.

    Expected output format:

    Proposed Epic:
    <updated epic statement>

    Changes Summary:
    <summary of the changes and reasoning>

    Returns:
         tuple (proposed_epic, changes_summary)
    """
    prompt = f"""
You are an experienced project management assistant.
The current epic for a project is shown below, along with user feedback.
Please propose an updated epic that incorporates the feedback. Additionally, provide a summary of the changes made 
and the reasoning behind these changes.

Format your response as follows:

Proposed Epic:
<updated epic statement>

Changes Summary:
<summary of the changes and reasoning>

Current Epic:
\"\"\"{current_epic}\"\"\"

User Feedback:
\"\"\"{user_feedback}\"\"\"
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a seasoned project planning assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    full_response = response.choices[0].message.content
    
    # Parse the response into a proposed epic and changes summary.
    epic_lines = []
    summary_lines = []
    mode = None
    for line in full_response.splitlines():
        if line.startswith("Proposed Epic:"):
            mode = "epic"
            text = line[len("Proposed Epic:"):].strip()
            if text:
                epic_lines.append(text)
        elif line.startswith("Changes Summary:"):
            mode = "summary"
            text = line[len("Changes Summary:"):].strip()
            if text:
                summary_lines.append(text)
        elif mode == "epic":
            epic_lines.append(line.strip())
        elif mode == "summary":
            summary_lines.append(line.strip())
    
    proposed_epic = "\n".join(epic_lines).strip()
    changes_summary = "\n".join(summary_lines).strip()
    return proposed_epic, changes_summary

if __name__ == "__main__":
    current_epic = "Develop a secure multi-factor authentication system for all users."
    user_feedback = (
        "The epic should also address user access management across various platforms. It would be helpful to include "
        "details about integration with third-party services and considerations for scalability."
    )
    proposed_epic, changes_summary = generate_epic_feedback(current_epic, user_feedback)
    print("Proposed Updated Epic:\n", proposed_epic)
    print("\nChanges Summary:\n", changes_summary) 