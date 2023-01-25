from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import get_db_session
from Models import UserModel
from Schemas import UserSchema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError
import dotenv
import os


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
dotenv.load_dotenv()
                                                             

# Login Form OAuth2 Obviously a POST Request
@router.post("/login", tags=['login'])
async def login_for_access_token(db:Session=Depends(get_db_session), form_data:OAuth2PasswordRequestForm = Depends()):
    user = db.query(UserModel.User).filter(UserModel.User.username==form_data.username).scalar()    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    check_password  = user.verify_password_hash(form_data.password, user.password_hash)
    print(user.is_active)
    # user.is_active = True
    # print(user.is_active)
    
    if not check_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



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
        username: str = payload.get("username")
        is_active: bool = payload.get('is_active')
        print(is_active)
        if username is None:
            raise credentials_exception
        print(username)
        # token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(UserModel.User).filter(UserModel.User.username==username).one()
    user.active()
    db.commit()
    db.refresh(user)
    print(user.is_active)
    print(user.is_active)

    if user is None:
        raise credentials_exception
    return vars(user)


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user



@router.get("/users/me/", tags=['login'], response_model=UserSchema.User)
async def read_users_me(current_user: UserSchema.User = Depends(get_current_user)):
    current_user['is_active'] = True
    return current_user


#  @app.get("/users/me/items/")
#  async def read_own_items(current_user: User = Depends(get_current_active_user)):
#      return [{"item_id": "Foo", "owner": current_user.username}]