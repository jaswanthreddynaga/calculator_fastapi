# main.py

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator  # Use @validator for Pydantic 1.x
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.operations import add, subtract, multiply, divide  # Ensure correct import path
from app.database import Base, engine, get_db
from app.models import User, Calculation
from app.schemas import UserCreate, UserRead, CalculationCreate, CalculationRead
from app.security import hash_password, verify_password
import uvicorn
import logging

# Setup logging with detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
logger.info("FastAPI Calculator application starting up...")

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

# Setup templates directory
templates = Jinja2Templates(directory="templates")

# Pydantic model for request data
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator('a', 'b')  # Correct decorator for Pydantic 1.x
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError('Both a and b must be numbers.')
        return value

# Pydantic model for successful response
class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")

# Pydantic model for error response
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")

# Custom Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extracting error messages
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(
        status_code=400,
        content={"error": error_messages},
    )

@app.get("/")
async def read_root(request: Request):
    """
    Serve the index.html template.
    """
    logger.info(f"Serving index page to {request.client.host if request.client else 'unknown'}")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def add_route(operation: OperationRequest):
    """
    Add two numbers.
    """
    logger.info(f"Received add request: a={operation.a}, b={operation.b}")
    try:
        result = add(operation.a, operation.b)
        logger.info(f"Add operation successful: {operation.a} + {operation.b} = {result}")
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Add Operation Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/subtract", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def subtract_route(operation: OperationRequest):
    """
    Subtract two numbers.
    """
    logger.info(f"Received subtract request: a={operation.a}, b={operation.b}")
    try:
        result = subtract(operation.a, operation.b)
        logger.info(f"Subtract operation successful: {operation.a} - {operation.b} = {result}")
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Subtract Operation Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/multiply", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def multiply_route(operation: OperationRequest):
    """
    Multiply two numbers.
    """
    logger.info(f"Received multiply request: a={operation.a}, b={operation.b}")
    try:
        result = multiply(operation.a, operation.b)
        logger.info(f"Multiply operation successful: {operation.a} * {operation.b} = {result}")
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Multiply Operation Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/divide", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def divide_route(operation: OperationRequest):
    """
    Divide two numbers.
    """
    logger.info(f"Received divide request: a={operation.a}, b={operation.b}")
    try:
        result = divide(operation.a, operation.b)
        logger.info(f"Divide operation successful: {operation.a} / {operation.b} = {result}")
        return OperationResponse(result=result)
    except ValueError as e:
        logger.error(f"Divide Operation Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Divide Operation Internal Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/users/register", response_model=UserRead)
async def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user_in.password)
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_password,
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    return user


@app.post("/users/login")
async def login_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user.id}


@app.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/calculations", response_model=list[CalculationRead])
async def read_calculations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    calculations = db.query(Calculation).offset(skip).limit(limit).all()
    return calculations


@app.get("/calculations/{calculation_id}", response_model=CalculationRead)
async def read_calculation(calculation_id: int, db: Session = Depends(get_db)):
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calculation


@app.post("/calculations", response_model=CalculationRead)
async def create_calculation(calculation_in: CalculationCreate, user_id: int, db: Session = Depends(get_db)):
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    calculation = Calculation(
        a=calculation_in.a,
        b=calculation_in.b,
        type=calculation_in.type,
        user_id=user_id,
        result=0 # Placeholder, should be calculated
    )
    
    # Calculate result based on type
    if calculation.type == "Add":
        calculation.result = calculation.a + calculation.b
    elif calculation.type == "Subtract":
        calculation.result = calculation.a - calculation.b
    elif calculation.type == "Multiply":
        calculation.result = calculation.a * calculation.b
    elif calculation.type == "Divide":
        if calculation.b == 0:
             raise HTTPException(status_code=400, detail="Cannot divide by zero")
        calculation.result = calculation.a // calculation.b # Integer division as per model

    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    return calculation


@app.put("/calculations/{calculation_id}", response_model=CalculationRead)
async def update_calculation(calculation_id: int, calculation_in: CalculationCreate, db: Session = Depends(get_db)):
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")

    calculation.a = calculation_in.a
    calculation.b = calculation_in.b
    calculation.type = calculation_in.type
    
    # Recalculate result
    if calculation.type == "Add":
        calculation.result = calculation.a + calculation.b
    elif calculation.type == "Subtract":
        calculation.result = calculation.a - calculation.b
    elif calculation.type == "Multiply":
        calculation.result = calculation.a * calculation.b
    elif calculation.type == "Divide":
        if calculation.b == 0:
             raise HTTPException(status_code=400, detail="Cannot divide by zero")
        calculation.result = calculation.a // calculation.b

    db.commit()
    db.refresh(calculation)
    return calculation


@app.delete("/calculations/{calculation_id}")
async def delete_calculation(calculation_id: int, db: Session = Depends(get_db)):
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    db.delete(calculation)
    db.commit()
    return {"message": "Calculation deleted successfully"}


if __name__ == "__main__":
    logger.info("Starting FastAPI server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
