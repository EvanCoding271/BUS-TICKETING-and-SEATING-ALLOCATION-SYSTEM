<<<<<<< HEAD
from pydantic import BaseModel, constr

class QRValidateSchema(BaseModel):
    qr_payload: constr(min_length=1)
=======
from pydantic import BaseModel, constr

class QRValidateSchema(BaseModel):
    qr_payload: constr(min_length=1)
>>>>>>> a96f8434797859db5b8f2889941570f4dc9b35d0
