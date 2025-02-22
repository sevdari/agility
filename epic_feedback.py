from model import Model
from parser import EpicParser as parser
from ticket import Epic


epic_feedback_agent = Model(
    model_name="gpt-4o",
    system_prompt="You are an experienced project manager working as a scrum master"
)

epic_feedback_prompt = """
    You are an experienced project manager working as a scrum master with a knack for defining 
    high-level visions. An epic for the current project (details provided below) is shown 
    below, along with feedback from your dev team. Please propose an updated epic that 
    incorporates the feedback and a brief summary of your reasoning for your the proposed 
    changes.

    Format your response exactly as follows:
    \"\"\"
    Epic:
    <Your epic statement with the proposed changes incorporated here>

    Summary:
    <Your reasoning summary here>
    \"\"\"
    """
    

def generate_epic_feedback(current_epic, user_feedback, project_summary) -> tuple[Epic, str]:
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
        {epic_feedback_prompt}
        Here is the current epic:
        \"\"\"
        {current_epic.get_current_content()}
        \"\"\"
        Here is the user feedback:
        \"\"\"
        {user_feedback}
        \"\"\"
        Here are the details and current status of the project:
        \"\"\"
        {project_summary}
        \"\"\"
    """
    
    response = epic_feedback_agent.prompt(
        system_prompt=epic_feedback_prompt,
        user_prompt=prompt
    )

    return parser.parse(response, current_epic)

if __name__ == "__main__":
    # Create an Epic object representing the current epic.
    current_epic = Epic(epic_content="Develop a secure multi-factor authentication system for all users.")

    project_summary = (
        "Project mission statement: To provide a secure access solution for users across various platforms.\n"
        "Project summary: We need a comprehensive solution for multi-factor authentication and secure access for users across various platforms.\n"
        "Current epics: 1 - \"Develop a secure multi-factor authentication system for all users.\""
    )

    user_feedback = (
        "The epic should also address user access management across various platforms. It would be helpful to include "
        "details about integration with third-party services and considerations for scalability."
    )

    print("-" * 100)
    print("Current Epic:")
    print(current_epic)
    print("-" * 100)
    print("User Feedback:")
    print(user_feedback)
    print("-" * 100)
    print("Project Summary:")
    print(project_summary)
    print("-" * 100)

    updated_epic, summary = generate_epic_feedback(current_epic, user_feedback, project_summary)
    print("Proposed Updated Epic:")
    print(updated_epic)
    print("\nChanges Summary:")
    print(summary)