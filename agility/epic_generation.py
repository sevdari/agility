import os
from dotenv import load_dotenv
from openai import OpenAI
from parser import Epic  # Import Epic for returning an object

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_epic(user_prompt):
    """
    Generates an epic based on the user's input prompt.

    Expected response format from the LLM:
    
    Epic:
    <Your epic statement here>
    
    Summary:
    <Your summary explaining the reasoning>

    Returns:
         tuple (epic, summary) where epic is an Epic instance.
    """
    prompt = f"""
You are an experienced project management assistant with a knack for defining high-level visions. Based on the user's input below, 
please generate an epic for a project and provide a brief summary of your reasoning.

Format your response exactly as follows:

Epic:
<Your epic statement here>

Summary:
<Your summary explaining the key points used to arrive at this epic>

User Prompt:
\"\"\"{user_prompt}\"\"\"
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
    
    epic_lines = []
    summary_lines = []
    mode = None
    for line in full_response.splitlines():
        if line.startswith("Epic:"):
            mode = "epic"
            text = line[len("Epic:"):].strip()
            if text:
                epic_lines.append(text)
        elif line.startswith("Summary:"):
            mode = "summary"
            text = line[len("Summary:"):].strip()
            if text:
                summary_lines.append(text)
        elif mode == "epic":
            epic_lines.append(line.strip())
        elif mode == "summary":
            summary_lines.append(line.strip())
    
    epic_text = "\n".join(epic_lines).strip()
    summary = "\n".join(summary_lines).strip()

    # Create an Epic instance. The epic_id here is arbitrary—adjust as needed.
    epic_object = Epic(epic_id=1, epic_content=epic_text)
    return epic_object, summary

if __name__ == "__main__":
    user_prompt = (
        "We need a comprehensive solution for multi-factor authentication and secure access for users across various platforms."
    )
    epic, summary = generate_epic(user_prompt)
    print("Generated Epic:\n", epic)
    print("\nSummary:\n", summary) 