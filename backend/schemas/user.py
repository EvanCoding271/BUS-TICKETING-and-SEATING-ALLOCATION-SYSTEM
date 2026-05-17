from pydantic import BaseModel, EmailStr, constr

class UserRegisterSchema(BaseModel):
    full_name: constr(min_length=3)
    email: EmailStr
    phone: constr(min_length=10, max_length=15)
    password: constr(min_length=8)

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
