from pydantic import BaseModel, EmailStr, constr

class EmployeeLoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    role: constr(min_length=3)
