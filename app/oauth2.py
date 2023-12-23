from jose import JWTError,jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def createAccessToken(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verifyAccessToken(token: str, credentialsException):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if not id:
            raise credentialsException
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentialsException
    
    return token_data

def getCurrentUser(token: str = Depends(oauth_scheme)):
    credentialsException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Could Not Validate Credentials",
                                         headers={"WWW-Authneticate":"Bearer"})
    
    token= verifyAccessToken(token, credentialsException)
    return token
