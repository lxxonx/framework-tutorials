from fastapi import FastAPI, Request, status, Response
from fastapi.exceptions import RequestValidationError
from app.routes import router, static_router

app = FastAPI()

app.include_router(router=router)

app.mount("/11/assets", static_router, name="assets")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(await request.body())
    print(exc.errors())
    return Response(
        status_code=status.HTTP_400_BAD_REQUEST,
    )
