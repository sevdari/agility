import json
from epic_generation import generate_epic
from starlette.responses import JSONResponse

def handler(request):
    try:
        body = request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    user_prompt = body.get("user_prompt")
    if not user_prompt:
        return JSONResponse({"error": "Missing user_prompt"}, status_code=400)
    
    # Call the epic generation function (which uses OpenAI)
    epic_obj, summary = generate_epic(user_prompt)
    return JSONResponse({"epic": epic_obj.to_dict(), "summary": summary}) 