import os
from dotenv import load_dotenv
from openai import OpenAI
from parser import Issue, Parser

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_proposals_with_feedback(user_feedback, issues):
    """
    Given user feedback and a list of current Issue objects, generate LLM-based proposals
    for modifications to the issues. The LLM is instructed to produce proposals for each issue,
    indicating for existing issues one of the following actions:
      - Update: Provide a new title and revised body.
      - Delete: Recommend that the issue be removed.
    Additionally, if an issue is missing, the LLM should propose a new issue (using the action 'Add').

    The LLM response is parsed by Parser.parse_issue_feedback, which returns:
      - modifications: a dict mapping issue IDs (int) to a dict with keys:
            { "action": "Update" or "Delete",
              "proposed_title": <value> (if applicable),
              "proposed_body": <value> (if applicable) }
      - new_proposals: a list of dicts, each with keys:
            { "action": "Add",
              "proposed_title": <value>,
              "proposed_body": <value> }
      - proposal_summary: a string summarizing the proposed changes.

    After parsing, the existing Issue objects are updated with the proposed changes. For new issues,
    new Issue objects are created and appended to the issues list.

    Returns:
         tuple (issues, proposal_summary)
         - issues: the updated list of Issue objects (each containing the proposed_action and changes).
         - proposal_summary: a string summarizing the proposed changes.
    """
    # Build context for the current state of all issues.
    current_issues_context = "\n".join(
        f"Issue {issue.issue_id}:\nTitle: {issue.issue_title}\nBody: {issue.issue_body}\n"
        for issue in issues
    )
    
    prompt = f"""
You are an experienced project management assistant. Below are the current issues for a project and some user feedback.
Based solely on the current details and the user feedback, please propose modifications for each issue:
- For existing issues, propose one of the following actions:
   - Update: Provide a new title and revised description.
   - Delete: Recommend that the issue be removed.
- If an issue is missing, propose a new issue.
Follow this format exactly:

For existing issues:
Issue <ID>:
Action: <Update or Delete>
If Action is Update, then include:
Proposed Title: <revised title>
Proposed Body:
<revised description>

For new issues:
New Issue:
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
    
    print("Proposals Text:")
    print(proposals_text)
    print("--------------------------------")
    # Parse the LLM response using the centralized parser.
    modifications, new_proposals, proposal_summary = Parser.parse_issue_feedback(proposals_text)

    # Update existing Issue objects with the proposed modifications.
    for issue in issues:
        if issue.issue_id in modifications:
            mod = modifications[issue.issue_id]
            issue.proposed_action = mod.get("action")
            if mod.get("action", "").lower() == "update":
                issue.proposed_issue_title = mod.get("proposed_title")
                issue.proposed_issue_body = mod.get("proposed_body")

    # Create new Issue objects for each proposed new issue.
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
    # Example usage:
    issues = [
        Issue(issue_id=1, issue_title="Implement user authentication", issue_body="Create endpoints for login, logout, and registration."),
        Issue(issue_id=2, issue_title="Integrate third-party OAuth providers", issue_body="Support sign-in with providers like Google and Facebook."),
        Issue(issue_id=3, issue_title="Unwanted Issue", issue_body="This issue should be removed as it is not actionable.")
    ]
    
    print("Initial Issues:")
    for issue in issues:
        print(issue)
    
    user_feedback = (
        "The issues are too generic. For Issue 1, focus on backend authentication logic. "
        "For Issue 2, be explicit about the configuration for multiple OAuth providers. "
        "Please remove Issue 3 and consider adding an issue for front-end integration."
    )
    
    issues, proposal_summary = generate_proposals_with_feedback(user_feedback, issues)
    
    print("\nUpdated Issues:")
    for issue in issues:
        print(issue)
    
    print("\nProposal Summary:")
    print(proposal_summary) 