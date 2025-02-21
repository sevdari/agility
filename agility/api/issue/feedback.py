import json
from issue_feedback import generate_proposals_with_feedback
from parser import Issue
from starlette.responses import JSONResponse

def handler(request):
    try:
        body = request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    user_feedback = body.get("user_feedback")
    issues_data = body.get("issues", [])
    
    if not user_feedback or not issues_data:
        return JSONResponse({"error": "Missing input"}, status_code=400)
    
    # Create Issue objects from the provided data.
    issues = [
        Issue(
            issue_id=issue["issue_id"],
            issue_title=issue["issue_title"],
            issue_body=issue["issue_body"],
        )
        for issue in issues_data
    ]
    
    updated_issues, proposal_summary = generate_proposals_with_feedback(user_feedback, issues)
    updated_issues_serialized = [issue.to_dict() for issue in updated_issues]
    
    return JSONResponse({
        "updated_issues": updated_issues_serialized,
        "proposal_summary": proposal_summary
    }) 