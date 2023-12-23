from app import utils, schemas, models
from app.database import get_db
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createUser(user: schemas.CreateUser, db: Session = Depends(get_db)):
    
    hashedPwd = utils.hash(user.password)
    user.password = hashedPwd

    newuser = models.User(**user.model_dump())
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser

@router.get("/{id}", response_model=schemas.UserOut)
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="user with id: {id} does not exists")
    return user