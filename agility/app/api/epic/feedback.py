import json
from epic_feedback import generate_epic_feedback
from parser import Epic
from starlette.responses import JSONResponse

def handler(request):
    try:
        body = request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    current_epic_content = body.get("current_epic")
    user_feedback = body.get("user_feedback")
    if not current_epic_content or not user_feedback:
        return JSONResponse({"error": "Missing input"}, status_code=400)
    
    current_epic = Epic(epic_id=1, epic_content=current_epic_content)
    updated_epic, changes_summary = generate_epic_feedback(current_epic, user_feedback)
    return JSONResponse({
        "updated_epic": updated_epic.to_dict(),
        "changes_summary": changes_summary
    }) 