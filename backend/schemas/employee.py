<<<<<<< HEAD
from pydantic import BaseModel, EmailStr, constr

class EmployeeLoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    role: constr(min_length=3)
=======
from pydantic import BaseModel, EmailStr, constr

class EmployeeLoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    role: constr(min_length=3)
>>>>>>> a96f8434797859db5b8f2889941570f4dc9b35d0
