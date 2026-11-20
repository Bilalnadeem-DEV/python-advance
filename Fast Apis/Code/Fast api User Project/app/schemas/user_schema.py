from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(ge=18, le=100)
    email: EmailStr


class UserResponse(UserBase):
    id: int
    message: str