import os
from dotenv import load_dotenv
from openai import OpenAI
from parser import Issue, Parser

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_proposals_with_feedback(user_feedback, issues):
    """
    Given user feedback and a list of Issue objects, generate LLM-based proposals for modifying the issues.
    Returns a tuple: (updated list of Issue objects, proposal_summary)
    """
    current_issues_context = "\n".join(
        f"Issue {issue.issue_id}:\nTitle: {issue.issue_title}\nBody: {issue.issue_body}\n"
        for issue in issues
    )
    
    prompt = f"""
You are an experienced project management assistant. Below are the current issues and user feedback.
Please propose modifications for each issue as follows:
- For existing issues, specify an action (Update or Delete). If updating, provide:
    Proposed Title: <revised title>
    Proposed Body:
    <revised description>
- For missing issues, propose a new issue with:
    Action: Add
    Proposed Title: <title>
    Proposed Body:
    <description>

User Feedback:
\"\"\"{user_feedback}\"\"\"

Current Issues:
\"\"\"{current_issues_context}\"\"\"

Proposal Summary:
<Provide a concise summary of the proposed changes.>
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an experienced project management assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    proposals_text = response.choices[0].message.content
    
    # Parse the LLM response.
    modifications, new_proposals, proposal_summary = Parser.parse_issue_feedback(proposals_text)

    # Update existing Issue objects.
    for issue in issues:
        if issue.issue_id in modifications:
            mod = modifications[issue.issue_id]
            issue.proposed_action = mod.get("action")
            if mod.get("action", "").lower() == "update":
                issue.proposed_issue_title = mod.get("proposed_title")
                issue.proposed_issue_body = mod.get("proposed_body")

    # Create new Issue objects for proposals.
    max_id = max((issue.issue_id for issue in issues), default=0)
    for proposal in new_proposals:
        max_id += 1
        new_issue = Issue(
            issue_id=max_id,
            issue_title=proposal.get("proposed_title"),
            issue_body=proposal.get("proposed_body"),
            proposed_action=proposal.get("action")
        )
        issues.append(new_issue)
    
    return issues, proposal_summary

if __name__ == "__main__":
    issues = [
        Issue(issue_id=1, issue_title="Implement user authentication", issue_body="Create endpoints for login, logout, and registration."),
        Issue(issue_id=2, issue_title="Integrate third-party OAuth providers", issue_body="Support sign-in with providers like Google and Facebook."),
        Issue(issue_id=3, issue_title="Unwanted Issue", issue_body="This issue should be removed.")
    ]
    
    user_feedback = (
        "The issues are too generic. For Issue 1, focus on backend authentication logic. " 
        "For Issue 2, detail the OAuth configuration. Please remove Issue 3 and consider adding an issue for front-end integration."
    )
    
    updated_issues, proposal_summary = generate_proposals_with_feedback(user_feedback, issues)
    for issue in updated_issues:
        print(issue)
    print("Proposal Summary:\n", proposal_summary) 