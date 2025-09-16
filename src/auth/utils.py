from passlib.context import CryptContext
from datetime import timedelta,datetime
import jwt
from src.config import settings
import uuid
import logging
from itsdangerous import URLSafeTimedSerializer

pwd_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) -> str:
    hash =  pwd_context.hash(password)
    return hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if pwd_context.verify(plain_password, hashed_password):
        return True
    return False


def create_access_token(user_data: dict, expiry: timedelta = None, refresh:bool = False) -> str: #type: ignore
    payload = {}
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload= payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def decode_access_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, 
            key=settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return {}
    

serializer = URLSafeTimedSerializer(
    secret_key=settings.JWT_SECRET_KEY,
    salt="email-configuration"
)


def create_url_safe_token(data: dict):
    token = serializer.dumps(data)
    return token


def decode_url_safe_token(token: str):
    try:
        token_data = serializer.loads(token)
        return token_data
    except Exception as e:
        logging.error(str(e))