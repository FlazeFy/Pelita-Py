from fastapi.responses import JSONResponse
from configs.const import RESPONSE_MESSAGES

def build_response(status_code: int, type_response: str, context_key: str, method: str, data=None):
    message = RESPONSE_MESSAGES.get(method, method)

    content = {
        "status": type_response,
        "message": f"{context_key} {message}",
    }

    if data:
        content["data"] = data

    return JSONResponse(
        status_code=status_code,
        content=content
    )
