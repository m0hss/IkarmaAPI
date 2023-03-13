from fastapi import FastAPI, Depends, Request, Path, HTTPException, status, Response, APIRouter, UploadFile, File, Body, Form, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db.database import get_db_session
from typing import List
from schemas import post_schema, user_schema
from db import models
from .login import oauth2_scheme, get_current_user
import os
from datetime import datetime
from starlette.responses import StreamingResponse
import shutil
import uuid
import cv2
import numpy as np
from pathlib import Path
import tempfile



router = APIRouter()

UPLOAD_FOLDER = "videos"
ALLOWED_EXTENSIONS = {"mp4", "mkv", "flv", "avi", "mov"}
THUMBNAIL_FOLDER = "images/thumbnail"



def allowed_file(filename):
    return '.' in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_duration(file: UploadFile):
    with tempfile.NamedTemporaryFile(mode='wb') as f:
        f.write(file.file.read())
        data = cv2.VideoCapture(f.name)
        duration = round(data.get(cv2.CAP_PROP_FRAME_COUNT) / data.get(cv2.CAP_PROP_FPS))
        file.file.seek(0)
    return duration

def get_size(file: UploadFile):
    file.file.seek(0,2)
    size = file.file.tell()
    file.file.seek(0)
    return size

def get_thumbnail_url(file: UploadFile):
    with tempfile.NamedTemporaryFile(mode='wb', suffix=f'{file.filename.rsplit(".", 1)[1].lower()}') as f:
        f.write(file.file.read())
        capture = cv2.VideoCapture(f.name)
        capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = capture.read()
        if ret:
            print(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            thumbnail_url = f'{THUMBNAIL_FOLDER}/thumb_{timestamp}.jpg'
            cv2.imwrite(thumbnail_url, frame)
            capture.release()
            file.file.seek(0)
            Path(f.name).unlink(missing_ok=True)
            return thumbnail_url
        else:
            raise HTTPException(status_code=400, detail="Failed to capture video frame.")
 
 
# Generator to Read Data Chunks
def read_data(file_path):
    with open(file_path, mode='rb') as buffer:
        while True:
            data = buffer.read(4096)
            if not data:
                break
            yield data
            
########################################################################
## Create Video Endpoint
########################################################################

@router.post("/posts", tags=['Posts'], response_model= post_schema.Post)
async def create_video_post(title: str = Form(...), description: str = Form(...), file: UploadFile = File(description="Upload video "), db: Session = Depends(get_db_session), current_user: user_schema.User = Depends(get_current_user)):
  
    file_path = f'{UPLOAD_FOLDER}/{current_user["id"]}/{file.filename}'
    ext = file.filename.rsplit(".", 1)[1].lower()
    
    if not os.path.exists(f'{UPLOAD_FOLDER}/{current_user["id"]}'):
        os.makedirs(f'{UPLOAD_FOLDER}/{current_user["id"]}')
    
    
    if not allowed_file(file.filename):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error: Invalid file type. Allowed types are: .{}".format(", .".join(ALLOWED_EXTENSIONS)))
    
    if get_duration(file) > 30:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error: File size too large")
    
    print("********************************************")
    print(file_path)
    print(file.content_type)
    print(f'Duration: {get_duration(file)} seconds')
    print(f'size: {get_size(file)}')
    print("********************************************")
    # print(get_thumbnail_url(file))
    print("*********************************************")
    
    ##  Check if Post Already Uploded 
    
    print(current_user['id'])
    posts = db.query(models.Post).filter(models.Post.user_id == current_user["id"]).all()
    # print(posts.user_id)
    for post in posts:
        if file_path in post.url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'Element exists ! ') 
        # print(type(post.url))
        # print(post.user.username)
    
    
    ## Store the File in Video Folder
    with open(f'{file_path}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        file.file.seek(0)

  
    print(file_path)
    file_size = Path(file_path).stat().st_size
    print(f"Size of {file_path}: {file_size} bytes")
    print("Size with os: ", os.path.getsize(file_path))   
    print(datetime.now())
    
    
    posts = db.query(models.Post).all()
    new_post = models.Post(
        id = str(uuid.uuid1()),
        title =  title,
        description =  description,
        url = file_path,
        thumbnail = get_thumbnail_url(file),
        size = get_size(file),
        created_at  = datetime.now(),
        user_id = current_user["id"]
      )
     
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    response = FileResponse(file_path, media_type=f'video/{file.filename.rsplit(".", 1)[1].lower()}')
    response.headers["Content-Disposition"] = "attachment; filename=myvideo.mp4"
    return response

 
##########################################################
# Get Posts Current User
##########################################################
@router.get("/posts/{user_id}", tags=['Posts'])
def read_videos(db: Session = Depends(get_db_session), current_user: user_schema.User = Depends(get_current_user)):
    user_posts = db.query(models.Post).filter(models.Post.user_id == current_user['id']).all()
    print(current_user['id'])
    print(user_posts)
    if not user_posts:
        raise HTTPException(status_code=404, detail="No Posts Found !!")
    return user_posts

###########################################
# ALL Posts JSON Response
###########################################
@router.get("/posts", tags=['Posts'], response_model= List[user_schema.ReadPosts])
async def read_all_videos(db: Session = Depends(get_db_session)):

    posts = db.query(models.Post).all()
    for post in posts:
        print(vars(post))
    return posts
########################################################
## Delete Post
########################################################
@router.delete('/posts', tags=['Posts'])
def delete_post(title:str, db:Session=Depends(get_db_session), current_user: user_schema.User = Depends(get_current_user)):
    try:
        post = db.query(models.Post).filter(models.Post.title == title).first()
       
        Path(post.url).unlink(missing_ok=True)
        Path(post.thumbnail).unlink(missing_ok=True)
        db.delete(post)
        db.commit()
        reponse = post_schema.reponse(msg= f'Post {title} deleted !')
        return reponse   
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post: {title} does not exist !')
 
 
##################################################################################
## Get Post video from Title
################################################################################
@router.get("/posts/video/{title}", tags=["Posts"])
async def read_post_video(title: str, db: Session = Depends(get_db_session)):
    post = db.query(models.Post).filter(models.Post.title == title).first()
    print(post)
    print(post)
    if post and post.title:
        return FileResponse(post.url, media_type=f'video/mp4')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'No Video Found ! ') 
        # return Response(content="Avatar not found", status_code=404)    
        
##################################################################################
## Get Post thumbnail from Title
################################################################################
@router.get("/posts/thumbnail/{title}", tags=["Posts"])
async def read_post_video(title: str, db: Session = Depends(get_db_session)):
    post = db.query(models.Post).filter(models.Post.title == title).first()
    print(post)
    print(post)
    if post and post.title:
        return FileResponse(post.thumbnail, media_type=f'image/jpg')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'No Video Found ! ') 
        # return Response(content="Avatar not found", status_code=404)    

#############################
## Get User video
#############################
CHUNK_SIZE = 1024*1024

@router.get("/posts/video/url/{user_id}", tags=["Posts"])
async def get_video_url(user_id: int, db: Session = Depends(get_db_session)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user and user.posts:
        responses = []
        for post in user.posts:
            responses.append(post.url)
            
            
        return responses
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'Not Found ! ') 
        # return Response(content="Not found", status_code=404)



# def model_to_dict(model: models.User):
#     return {column.name: getattr(model, column.name) for column in model.__table__.columns}   








  
    