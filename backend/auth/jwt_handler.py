from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()
SECRET = os.getenv('JWT_SECRET', 'change-me-very-secret')
ALGO = os.getenv('JWT_ALGORITHM', 'HS256')
EXP_MIN = int(os.getenv('JWT_EXP_MINUTES', '60'))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXP_MIN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGO)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])
    except JWTError as exc:
        raise exc
