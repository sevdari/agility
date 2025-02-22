import os
from model import Model
from parser import EpicParser as parser
from ticket import Epic


epic_generation_agent = Model(
    model_name="gpt-4o",
    system_prompt="You are an experienced project manager working as a scrum master",
    temperature=0.7,
)

epic_generation_prompt = """
    You are an experienced project manager working as a scrum master with a knack for defining 
    high-level visions. Based on the provided user prompt below, generate an epic for the 
    current project (details provided below) and provide a brief summary of your reasoning for 
    these epics.

    Format your response exactly as follows:
    \"\"\"
    Epic:
    <Your epic statement here>

    Summary:
    <Your summary explaining the key points used to arrive at this epic>
    \"\"\"
"""

def generate_epic(user_prompt, project_summary) -> tuple[Epic, str]:
    """
    Generates an epic statement based on the user's input prompt.
    The LLM is expected to provide:
      - An epic statement.
      - A summary of how the epic was derived, highlighting key points.

    Returns:
         tuple (epic, summary)
    """
    
    prompt = f"""
        {epic_generation_prompt}
        Here is the user prompt:
        {user_prompt}
        Here are the details and current status of the project:
        {project_summary}
    """
    response = epic_generation_agent.prompt(
        system_prompt=epic_generation_prompt,
        user_prompt=prompt
    )
    
    # Parse the response into epic and summary.
    return parser.parse(response)


if __name__ == "__main__":
    project_summary = (
        "Project mission statement: To provide a secure access solution for users across various platforms.\n"
        "Project summary: We need a comprehensive solution for multi-factor authentication and secure access for users across various platforms.\n"
        "Current epics: [None]"
    )
    user_prompt = (
        "We need a comprehensive solution for multi-factor authentication and secure access for users across various platforms."
    )

    print("-" * 100)
    print("Project Summary:\n", project_summary)
    print("-" * 100)
    print("User Prompt:\n", user_prompt)
    print("-" * 100)

    epic, summary = generate_epic(user_prompt, project_summary)
    print("Generated Epic:\n", epic)
    print("\nSummary:\n", summary) 