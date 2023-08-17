from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.constant.app_status import AppStatus


def make_error_response(app_status=AppStatus.ERROR_INTERNAL_SERVER_ERROR, detail=None):
    if detail is None:
        detail = {}

    return JSONResponse(
        status_code=app_status.status_code,
        content=jsonable_encoder({"detail": detail}),
    )


def make_response_object(data: object, meta: object = {}) -> object:
    return {
        "data": data,
        "meta": meta
    }
