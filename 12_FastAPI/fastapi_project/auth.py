import os
import secrets
import warnings
from datetime import datetime, timedelta
from typing import Optional
import jwt  # PyJWT (replaces python-jose, which is no longer maintained)
from pwdlib import PasswordHash  # replaces passlib (unmaintained, breaks with bcrypt>=4.1)
from pwdlib.hashers.bcrypt import BcryptHasher
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from schemas import TokenData

# Read the signing key from the environment, e.g.  export SECRET_KEY="$(openssl rand -hex 32)"
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    # Dev fallback: random key per process (tokens stop working after a restart and are
    # not shared between workers), so always set SECRET_KEY in production.
    SECRET_KEY = secrets.token_hex(32)
    warnings.warn(
        "SECRET_KEY env var is not set; using a random development key. "
        "Set SECRET_KEY (e.g. `openssl rand -hex 32`) before deploying.",
        RuntimeWarning,
        stacklevel=2,
    )
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = PasswordHash((BcryptHasher(),))  # still verifies existing "$2b$..." bcrypt hashes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:  # also covers expired tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    payload = decode_token(token)
    if payload.get("type") != "access":  # a refresh token must not be accepted as an access token
        raise HTTPException(status_code=401, detail="Invalid token type")
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return TokenData(username=username)
