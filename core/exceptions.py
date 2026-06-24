from fastapi import Request
from fastapi.responses import JSONResponse


class ERPException(Exception):
    # FIX: was _init_ (single underscore) — must be __init__
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


async def erp_exception_handler(request: Request, exc: ERPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.message}
    )