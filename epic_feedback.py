import os
from dotenv import load_dotenv
from openai import OpenAI
from parser import Epic, Parser

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_epic_feedback(current_epic, user_feedback):
    """
    Generates a proposed updated epic based on the current epic and user feedback.
    The LLM's output is expected to include the following format:

    Proposed Epic:
    <updated epic statement>

    Changes Summary:
    <summary of the changes and reasoning>

    This function passes the raw output to Parser.parse_epic_feedback along with the provided 'current_epic'
    object and returns:
         tuple(updated_epic, changes_summary)
         - updated_epic: Epic instance with the updated proposed_content.
         - changes_summary: string description of the changes.
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
\"\"\"{current_epic.epic_content}\"\"\"

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
    raw_output = response.choices[0].message.content
    updated_epic, changes_summary = Parser.parse_epic_feedback(raw_output, current_epic)
    return updated_epic, changes_summary


if __name__ == "__main__":
    # Create an Epic object representing the current epic.
    current_epic = Epic(epic_id=1, epic_content="Develop a secure multi-factor authentication system for all users.")
    user_feedback = (
        "The epic should also address user access management across various platforms. It would be helpful to include "
        "details about integration with third-party services and considerations for scalability."
    )
    updated_epic, summary = generate_epic_feedback(current_epic, user_feedback)
    print("Proposed Updated Epic:")
    print(updated_epic)
    print("\nChanges Summary:")
    print(summary) 