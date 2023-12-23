from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def AuthLogin(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    access_token = oauth2.createAccessToken(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}