from fastapi import HTTPException, Depends, status, Response, APIRouter
from .. import models, utils, schemas, oauth2
from ..database import get_db, engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
    )

@router.get("/", response_model=List[schemas.PostOut])
def getPosts(db: Session = Depends(get_db), 
                   current_user = Depends(oauth2.getCurrentUser), 
                   limit: int = 10, skip: int = 0, search: Optional[str]= ""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                                         models.Vote.post_id == models.Post.id, 
                                         isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def createPost(post: schemas.PostCreate, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.getCurrentUser)):
    #cursor.execute("""INSERT INTO posts (title,content,published) 
    #               VALUES (%s, %s, %s) RETURNING *""", 
    #               (post.title, post.content, post.published))
    #newPost = cursor.fetchone()
    #conn.commit()
    newPost = models.Post(owner_id= current_user.id, **post.model_dump())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

@router.get("/{id}", response_model=schemas.PostOut)
def getRequestedPost(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE
    #                     id = %s""", (str(id)))
    # post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                                         models.Vote.post_id == models.Post.id, 
                                         isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id:{id} not found')
        
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), 
               current_user: int = Depends(oauth2.getCurrentUser)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s
    #                RETURNING *""", (str(id),))
    # deletedPost = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}", response_model=schemas.Post)
def updatePost(id: int, post: schemas.PostBase, db: Session = Depends(get_db),
               current_user: int = Depends(oauth2.getCurrentUser)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s
    #                WHERE id = %s RETURNING *""",(post.title, post.content, 
    #                                              post.published, str(id)))
    # updatedPost = cursor.fetchone()
    # conn.commit()

    updatedPost = db.query(models.Post).filter(models.Post.id == id)
    find_post = updatedPost.first()
    if not find_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message id:{id} not found")
    
    if find_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    updatedPost.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return updatedPost.first()