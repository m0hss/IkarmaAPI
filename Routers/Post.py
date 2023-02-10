from fastapi import FastAPI, Depends, Request, Path, HTTPException, status, Response, APIRouter, UploadFile, File, Body, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc
from sqlalchemy.orm import Session
from db.database import get_db_session
from typing import List
from Schemas import PostSchema, UserSchema
from db import Models
from .Login import oauth2_scheme, get_current_user
import os
from datetime import datetime
from starlette.responses import StreamingResponse
import shutil
import uuid


router = APIRouter()

UPLOAD_FOLDER = "Videos"
ALLOWED_EXTENSIONS = {".mp4", ".mkv", ".flv", ".avi", ".jpg", ".png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/posts", tags=['Posts'])
async def create_video_post(title: str = Form(...), description: str = Form(...), file: UploadFile = File(description="Upload video "), db: Session = Depends(get_db_session), current_user: UserSchema.User = Depends(get_current_user)):
 
    # if not allowed_file(file.filename):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error: Invalid file type. Allowed types are: {}".format(", ".join(ALLOWED_EXTENSIONS)))
    # if file.content_type != "video/mp4" and file.content_length > 1 * 1024 * 1024:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error: File size too large")
    
    # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    print(file.filename)
    print(file.content_type)
    
    
    file_path = f'{UPLOAD_FOLDER}/{file.filename}'
    with open(f'{file_path}', "wb") as buffer:
         shutil.copyfileobj(file.file, buffer)
    print(file_path)
    
    print(os.path.getsize(file_path))   
    # with open(file_path, "wb") as f:
    #     f.write(await file.read())
    
   
     # Get the size of the uploaded video file
    file.file.seek(0, 2) # Seek to the end of the file
    size = file.file.tell()
    file.file.seek(0) # Reset the file position
    
    print(datetime.now())
    
    posts = db.query(Models.Post).all()
    
    new_post = Models.Post(
        id = str(uuid.uuid1()),
        title =  title,
        description =  description,
        path = file_path,
        size = size,
        created_at  = datetime.now(),
        user_id = current_user['id']
      )
     
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    
    return {"message": file.filename, "new_post": new_post}


# @router.get("/posts/{post_id}", tags=['Posts'])
# def read_video_by_id(post_id: int, db: Session = Depends(get_db_session)):
#     video_post = db.query(Models.Post).filter(Models.Post.id == post_id).first()
#     if not video_post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return video_post


@router.get("/posts", tags=['Posts'])
async def read_all_videos(db: Session = Depends(get_db_session)):
    videos = db.query(Models.Post).all()
    return videos

# Delete Post 
@router.delete('/posts/{post_id}', tags=['Posts'], response_model= PostSchema.reponse)
def delete_post(post_id:str, db:Session=Depends(get_db_session)):
    try:
        post = db.query(Models.Post).filter(Models.Post.id == post_id).first()
        # print(post.path)
        os.remove(post.path)
        db.delete(post)
        db.commit()
        reponse = PostSchema.reponse(msg= f'Post {post_id} Deleted Successfuly  !')
        return reponse
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post id: {post_id} not found !')
    