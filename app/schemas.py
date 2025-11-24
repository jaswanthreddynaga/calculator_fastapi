from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


from pydantic import BaseModel, EmailStr, field_validator, model_validator

class CalculationBase(BaseModel):
    a: int
    b: int
    type: str


class CalculationCreate(CalculationBase):
    @field_validator('type')
    def validate_type(cls, v):
        if v not in ['Add', 'Subtract', 'Multiply', 'Divide']:
            raise ValueError('Invalid operation type')
        return v

    @model_validator(mode='after')
    def validate_division_by_zero(self):
        if self.type == 'Divide' and self.b == 0:
            raise ValueError('Cannot divide by zero')
        return self


class CalculationRead(CalculationBase):
    id: int
    result: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
