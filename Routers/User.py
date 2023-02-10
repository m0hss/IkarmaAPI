from fastapi import FastAPI, Depends, Request, Path, HTTPException, status, Response, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc
from sqlalchemy.orm import Session
from db.database import get_db_session
from typing import List
from Schemas import UserSchema
from db import Models
from Routers.Login import oauth2_scheme 


router = APIRouter()

# Get All users
@router.get('/users', tags=['Users'], response_model=List[UserSchema.User])
def show_all_users(db:Session=Depends(get_db_session)):
    users = db.query(Models.User).all()
    return users

# Get User By Id
@router.get('/users/{user_id}', tags=['Users'], response_model=UserSchema.User)
def show_user_by_id(user_id: int= Path(None, description="ID of the User"), db:Session=Depends(get_db_session), token:str=Depends(oauth2_scheme)):
    user = db.query(Models.User).filter_by(id=user_id).first()
    if user:
        return user
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user id: {user_id} does not exist !')
  
# Create New User  
@router.post('/users/', tags=['Users'], response_model=UserSchema.User)
def create_user(values:UserSchema.User, db:Session=Depends(get_db_session)):
    try:
        users = db.query(Models.User).all()
        new_user = Models.User(
            id = len(users)+ 1 if users else 1,
            gender = values.gender,
            first_name = values.first_name,
            last_name = values.last_name,
            thumbnail = values.thumbnail,
            username = values.username,
            password_hash = values.set_password_hash(values.password_hash),
            city = values.city,
            state = values.state,
            country = values.country,
            email = values.email,
            phone = values.phone,
            registred_on = values.registred_on,
            is_active = values.is_active
        )
    
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Username or Email already exist !')

# Update User Query
@router.put('/users/{user_id}', tags=['Users'], response_model= UserSchema.UserUpdate)
def update_user(user_id:int, values:UserSchema.UserUpdate, db:Session=Depends(get_db_session), token:str=Depends(oauth2_scheme)):
    user = db.query(Models.User).filter_by(id= user_id).first()
    for key, value in vars(values).items():
        setattr(user, key, value) if value else None 
        
    db.commit()
    db.refresh(user)
    return user 

# Partial Update to User
@router.patch('/users/{user_id}', tags=['Users'], response_model= UserSchema.UserUpdate)
async def patch_user(user_id:int, values:UserSchema.UserUpdate, db:Session=Depends(get_db_session), token:str=Depends(oauth2_scheme)):  
    user = db.query(Models.User).filter_by(id= user_id).first()

    for key, value in vars(values).items():
        setattr(user, key, value) if value else getattr(user, key)
    db.commit()
    db.refresh(user)
    # reponse = UserSchema.reponse(msg= f'{user_id} updated with Success !')
    return user

# Delete User 
@router.delete('/users/{user_id}', tags=['Users'], response_model= UserSchema.reponse)
def delete_user(user_id:int, db:Session=Depends(get_db_session), token:str=Depends(oauth2_scheme)):
    try:
        user = db.query(Models.User).filter_by(id= user_id).first()
        db.delete(user)
        db.commit()
        reponse = UserSchema.reponse(msg= f'User {user_id} deleted !')
        return reponse   
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user id: {user_id} does not exist !')
    
    
    
# @router.get("/user/posts/{user_id}", tags=['Users'])
# def read_video_by_user_id(user_id: int, db: Session = Depends(get_db_session)):
#     video_post = db.query(PostModel.Post).filter(PostModel.Post.user_id == user_id).all()
#     if not video_post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return video_post