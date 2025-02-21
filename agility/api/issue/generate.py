import json
from issue_generation import generate_issues
from starlette.responses import JSONResponse

def handler(request):
    try:
        body = request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    user_prompt = body.get("user_prompt")
    if not user_prompt:
        return JSONResponse({"error": "Missing user_prompt"}, status_code=400)

    issues, summary = generate_issues(user_prompt)
    issues_data = [issue.to_dict() for issue in issues]
    return JSONResponse({
        "issues": issues_data,
        "summary": summary
    }) 