from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from starlette.requests import Request

from app.constant.app_status import AppStatus
from app.utils.response import make_error_response


async def validation_exception_handler(request: Request, validation_error: RequestValidationError):
    detail = validation_error.errors()[0]
    err_loc = detail.get('loc')
    err_field = err_loc[len(err_loc) - 1]
    err_msg = f"{detail.get('msg')}: {err_field}"
    return make_error_response(app_status=AppStatus.ERROR_VALIDATION, detail={
            "error_code": AppStatus.ERROR_VALIDATION.app_status_code,
            "message": err_msg
        })


def error_exception_handler(error, app_status: AppStatus):
    status_code, err_msg, data = app_status.status_code, None, {}

    if isinstance(error, ValidationError):
        detail = error.errors()[0]
        err_loc = detail.get('loc')
        err_field = err_loc[len(err_loc) - 1]
        err_msg = f"{detail.get('msg')}: {err_field}"

        return HTTPException(
            status_code=app_status.status_code,
            detail=err_msg
        )

    if isinstance(error, ValueError) and isinstance(error.args[0], AppStatus):
        app_status = error.args[0]

        if len(error.args) > 1:
            data = error.args[1]

    return HTTPException(
        status_code=app_status.status_code,
        detail={
            "error_code": app_status.app_status_code,
            "message": app_status.message,
            "data": data
        }
    )
