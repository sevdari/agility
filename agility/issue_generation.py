import os
from dotenv import load_dotenv
from openai import OpenAI
from parser import Issue

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_issues(user_prompt, repository_context=None):
    """
    Generates a list of issues (as Issue objects) and a summary based on the user prompt.
    Optionally, repository_context can be used to provide additional context.
    
    Returns:
         tuple (issues, summary) where issues is a list of Issue objects.
    """
    # For demonstration, we return dummy issues.
    dummy_issues = [
        Issue(issue_id=1, issue_title="Implement user authentication", issue_body="Design backend endpoints for login and registration."),
        Issue(issue_id=2, issue_title="Set up OAuth integration", issue_body="Integrate third-party OAuth providers such as Google and Facebook.")
    ]
    summary = "Generated 2 issues based on the provided prompt."
    return dummy_issues, summary

if __name__ == "__main__":
    prompt = "Add support for multi-factor authentication and social login integration."
    issues, summary = generate_issues(prompt)
    for issue in issues:
        print(issue)
    print("Summary:", summary) 