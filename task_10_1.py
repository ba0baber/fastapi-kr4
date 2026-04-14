from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int


class CustomExceptionA(Exception):
    def __init__(self, message: str = "Condition not met"):
        self.message = message
        self.status_code = 400


class CustomExceptionB(Exception):
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        self.status_code = 404


@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
    print(f"CustomExceptionA caught: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "CustomExceptionA", "message": exc.message, "status_code": exc.status_code}
    )


@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
    print(f"CustomExceptionB caught: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "CustomExceptionB", "message": exc.message, "status_code": exc.status_code}
    )


@app.get("/check/{value}")
async def check_value(value: int):
    if value < 0:
        raise CustomExceptionA(message=f"Value {value} must be non-negative")
    return {"value": value, "status": "ok"}


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    items = {1: "Apple", 2: "Banana"}
    if item_id not in items:
        raise CustomExceptionB(message=f"Item with id={item_id} not found")
    return {"id": item_id, "name": items[item_id]}
