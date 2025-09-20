from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.core.constants import StatusCodes, Messages

def _clean_strings(obj):
    if isinstance(obj, dict):
        return {k: _clean_strings(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_clean_strings(i) for i in obj]
    elif isinstance(obj, str):
        return obj.strip()
    else:
        return obj

def response(
    detail=None,
    status_code: int = StatusCodes.SUCCESS,
):
    encoded_data = jsonable_encoder(detail) 
    cleaned_data = _clean_strings(encoded_data) if encoded_data else encoded_data

    return JSONResponse(
        status_code=status_code,
        content={
            "detail": cleaned_data
        },
    )
