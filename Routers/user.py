from fastapi import FastAPI, Depends, Request, Path, HTTPException, status, Response, APIRouter, File, UploadFile, Query, Form, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc
from sqlalchemy.orm import Session
from db.database import get_db_session, SessionLocal
from typing import List, Optional, Dict, Any
from schemas import user_schema
from db import models
from .login import get_current_user, oauth2_scheme
from PIL import Image, ImageDraw
import secrets
from datetime import date
import tempfile
from pathlib import Path
from zipfile import ZipFile




router = APIRouter()
PATH_FOLDER = "images/avatar"
ALLOWED_EXTENSIONS = {"jpg", "png"}


#####################################################################
# Get All users
#####################################################################
@router.get('/users', tags=['Users'], response_model=List[user_schema.User])
def show_all_users(db:Session=Depends(get_db_session)):
    users = db.query(models.User).all()
    return users

########################################################################
## Create New User
########################################################################
@router.post('/add_user', tags=['Users'], response_model=user_schema.reponse)
async def add_user(values: user_schema.Useradd, db:Session=Depends(get_db_session)):
    users = db.query(models.User).all()
    try:  
        
        print(users)
        new_user = models.User(
            id = len(users)+ 1 if users else 1,
            first_name = values.first_name,
            last_name = values.last_name,
            email = values.email,
            password = values.set_password_hash(values.password),
            registred_on = date.today(),
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        response = user_schema.reponse(msg= f'User {new_user.email} created successufully ')
        
        return response
    except exc.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Email already exists !')


## Generator to Read Data Chunks
def read_data(file_path):
    with open(file_path, mode='rb') as buffer:
        while True:
            data = buffer.read(4096)
            if not data:
                break
            yield data
            
## Circular Avatar form
def resize_n_circle(path, size=(150, 150)):
    img = Image.open(path)
    # Crop the image to a square
    width, height = img.size
    if width > height:
        left = (width - height) / 2
        right = (width + height) / 2
        top = 0
        bottom = height
    else:
        left = 0
        right = width
        top = (height - width) / 2
        bottom = (height + width) / 2
    img = img.crop((left, top, right, bottom))
    # Create a circular mask
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)
    # Apply the mask to the image
    img.putalpha(mask)
    # Create a circular thumbnail
    img.thumbnail(size, Image.ANTIALIAS)
    # Save the thumbnail
    img.save(path)
   
    
########################################################################################
# Update User Avatar
########################################################################################
@router.put('/users/avatar/', tags=['Users'])
async def Upload_avatar(avatar: UploadFile = File(None),
                    db:Session=Depends(get_db_session),
                    current_user: user_schema.User = Depends(get_current_user)) -> bytes:
    
    user = db.query(models.User).filter_by(id= current_user['id']).first()
    
    if avatar:
        print(user.avatar)
        if user.avatar:
            Path(user.avatar).unlink(missing_ok=True)
            
        avatar_path = f'{PATH_FOLDER}/{secrets.token_hex(10)}.png'
        print(avatar_path)
        with open(avatar_path, "wb") as f:
            f.write(await avatar.read())
            # contents = await avatar.read()
        await avatar.close()
        # setattr(user, user.avatar, avatar_path)
        resize_n_circle(avatar_path)
        user.avatar = avatar_path
        db.commit()
        db.refresh(user)
        
        #return {"messsage": "Avatar updated successfully !"}
        response = StreamingResponse(read_data(user.avatar), media_type=f'image/{avatar.filename.rsplit(".", 1)[1].lower()}')
        
        return response
    else:
        return {"message": "Avatar file is missing."}     
    


#################################################
# Patch User Data Patch Endpoint
##################################################
@router.patch('/users/', tags=['Users'], response_model= user_schema.UserUpdate)
async def patch_user(values: user_schema.UserUpdate = None, db:Session=Depends(get_db_session),
                     current_user: user_schema.User = Depends(get_current_user)):  
    print(current_user)
    try:
        user = db.query(models.User).filter_by(id= current_user['id']).first()
        if values:
            print(user.username)
            print(user.first_name)
            print(values.phone)
            for key, value in values.dict().items():
                print(key,value)
                setattr(user, key, value) if value else None
    
            if values.password:
                user.password = user_schema.User.set_password_hash(values.password)
        
            
        db.commit()
        db.refresh(user)
        # reponse = user_schema.reponse(msg= f'{user_id} updated with Success !')
        return user
    except exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Username or Email already exists !')

#########################################
## Delete User 
#########################################
@router.delete('/users/', tags=['Users'], response_model= user_schema.reponse)
def delete_user(db:Session=Depends(get_db_session), current_user: user_schema.User = Depends(get_current_user)):
    try:
        user = db.query(models.User).filter_by(id= current_user['id']).first()
        db.delete(user)
        db.commit()
        reponse = user_schema.reponse(msg= f'User {current_user["id"]} deleted !')
        return reponse   
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user id: {current_user["id"]} does not exist !')
    

##############################################################################
## Get the User avatar
##############################################################################
@router.get("/users/avatar/{user_id}", tags=["Users"])
async def read_user_avatar(user_id: int, db: Session = Depends(get_db_session)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    try:
        return FileResponse(user.avatar, media_type=f'image/{user.avatar.rsplit(".",1)[1]}')
    except:
        return FileResponse("images/avatar/default1.png", media_type="image/png")


#############################################################################
## Get all avatars
#############################################################################
@router.get('/avatars/', tags=['Users'])
async def get_all_avatars():
    
    avatars_dir = Path(PATH_FOLDER)

    avatars = list(avatars_dir.glob("*"))
    with ZipFile("avatars.zip", "w") as zip:
        for avatar in avatars:
            zip.write(avatar)
            
    return FileResponse("avatars.zip", media_type="application/zip", headers= {
        'Content-Disposition': 'attachment; filename="avatars.zip"'})

#########################################################################
## Get User video
#########################################################################
@router.get("/user/posts/", tags=["Users"])
def user_posts(db: Session = Depends(get_db_session), current_user: user_schema.User = Depends(get_current_user)):
    user_posts = db.query(models.Post).filter(models.Post.user_id == current_user['id']).all()
    print(current_user['id'])
    print(user_posts)
    if not user_posts:
        raise HTTPException(status_code=404, detail="No Posts Found !!")
    return user_posts



# # Get User By Id
# @router.get('/users/{user_id}', tags=['Users'], response_model=user_schema.User)
# def show_user_by_id(user_id: int, db:Session=Depends(get_db_session), token:str=Depends(oauth2_scheme)):
#     user = db.query(models.User).filter_by(id=user_id).first()
#     if user:
#         return user
#     else: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user id: {user_id} does not exist !')



# ##############################################################################
# # Create New User  
# ##############################################################################
# @router.post('/users/', tags=['Users'], response_model=user_schema.UserUpdate)
# async def create_user(
#                 gender: str = Query(None, enum=["male", "female"]),
#                 first_name: str = Form(),
#                 last_name: str = Form(),
#                 avatar: UploadFile = File(...),
#                 username: str = Form(),
#                 password: str =Form(),
#                 state: str = Form(),
#                 country: str = Form(),
#                 email: str = Form(),
#                 phone: int = Form(),
#                 db:Session=Depends(get_db_session)
#                 ):
    
#     ext = avatar.filename.rsplit(".", 1)[1].lower()
    
#     if not ext in ALLOWED_EXTENSIONS:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error: Invalid file type. Allowed types are: .{}".format(", .".join(ALLOWED_EXTENSIONS)))
    
    
#     generate_name = f'{secrets.token_hex(10)}.{ext}'
#     avatar_path = f'{PATH_FOLDER}/{generate_name}'
#     print('************************************************')
#     print(generate_name)
#     print(avatar_path)  
#     print('************************************************') 
#     # file_content = await avatar.read()
    
#     try:  
#         users = db.query(models.User).all()
#         print(users)
#         new_user = models.User(
#             id = len(users)+ 1 if users else 1,
#             gender = gender,
#             first_name = first_name,
#             last_name = last_name,
#             avatar = avatar_path,
#             username = username,
#             password = user_schema.User.set_password_hash(password),
#             state = state,
#             country = country,
#             email = email,
#             phone = phone,
#             registred_on = date.today(),
#         )
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
        
#         # Save the Uploded Picture in avatar_path
#         with open(avatar_path, "wb") as f:
#             f.write(await avatar.read())
#         # profile_pic.file.seek(0)
        
#         #Resize the profile picture
#         img = Image.open(avatar_path)
#         img = img.resize(size = (200, 200))
#         img.save(avatar_path)
        
#         await avatar.close()  
#         return new_user
#     except exc.IntegrityError as e:
#         db.rollback()
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Username or Email already exists !')

# ###################################################################################################
# # Update User Query Put Endpoint
  ##################################################################################################
# @router.put('/users/{user_id}', tags=['Users'], response_model= user_schema.UserUpdate)
# def update_user(user_id:int, values:user_schema.UserUpdate, db:Session=Depends(get_db_session), token:str=Depends(oauth2_scheme)):
#     try:
#         user = db.query(models.User).filter_by(id= user_id).first()
#         for key, value in vars(values).items():
#             print(key,value)
#             setattr(user, key, value) if value else None 
            
#         db.commit()
#         db.refresh(user)
#         return user 
#     except exc.IntegrityError as e:
#         db.rollback()
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Username or Email already exists !')
    
    
# @router.get("/user/posts/{user_id}", tags=['Users'])
# def read_video_by_user_id(user_id: int, db: Session = Depends(get_db_session)):
#     video_post = db.query(PostModel.Post).filter(PostModel.Post.user_id == user_id).all()
#     if not video_post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return video_post

