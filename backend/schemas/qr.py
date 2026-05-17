from pydantic import BaseModel, constr

class QRValidateSchema(BaseModel):
    qr_payload: constr(min_length=1)
