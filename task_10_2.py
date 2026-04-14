from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, conint, constr
from typing import Optional

app = FastAPI()


class User(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'


class ValidationErrorResponse(BaseModel):
    error: str
    details: list
    status_code: int


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"Validation error: {exc.errors()}")
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(
        status_code=422,
        content={"error": "Validation failed", "details": errors, "status_code": 422}
    )


@app.post("/users")
async def create_user(user: User):
    return {"message": "User created successfully", "user": user.model_dump()}
