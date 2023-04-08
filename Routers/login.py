from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import models
from db.database import get_db_session
from schemas import user_schema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError
import dotenv
import os
from sqlalchemy.orm.collections import InstrumentedList

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
dotenv.load_dotenv()
                                                             

# Login Form OAuth2 Obviously a POST Request
@router.post("/login", tags=['login'])
async def login_for_access_token(db:Session=Depends(get_db_session), form_data:OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.email==form_data.username).scalar()    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    check_password  = user.verify_password_hash(form_data.password, user.password)

    
    if not check_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    # response = user_schema.reponse(msg= f'access_token: {access_token}')
    
    
    
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm= os.getenv('ALGORITHM'))
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db:Session=Depends(get_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        email: str = payload.get("email")
        # is_active: bool = payload.get('is_active')
        # print(is_active)
        if email is None:
            raise credentials_exception
        print(f'current_user: {email}')
        print(f'token = <{token}>')
        print("************************************************************")
        # token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email==email).one()
    
    if user is None:
        raise credentials_exception
    # print(vars(user))
    return vars(user)


def to_dict_list(instrumented_list):
    return [obj.__dict__ for obj in instrumented_list]


@router.get("/users/me/", tags=['login'], response_model=user_schema.User)
async def read_user_me(db: Session = Depends(get_db_session),current_user: user_schema.User = Depends(get_current_user)):
    user = db.query(models.User).filter_by(id=current_user['id']).first()
    for post in user.posts:
        print(post.title)
    return user


# @router.post("/logout", tags=['login'])
# def logout(db: Session = Depends(get_db_session), current_user: user_schema.User = Depends(get_current_user), form_data: OAuth2PasswordRequestForm = Depends()):
    

#     # Set the user's is_active status to False
#     update_user_activity(db, user_id, False)

#     return {"message": "User logged out"}