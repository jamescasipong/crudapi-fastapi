from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from database import db
from models import User

# Secret key to encode JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db["users"].find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user

# Routes
@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db["users"].find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user["username"], "role": user["role"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=dict)
async def register_user(user: User):
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user_dict.pop("password"))
    if db["users"].find_one({"username": user_dict["username"]}):
        raise HTTPException(status_code=400, detail="Username already registered")
    db["users"].insert_one(user_dict)
    return {"msg": "User registered successfully"}

@router.get("/", response_model=list, dependencies=[Depends(get_current_user)])
async def read_root():
    result = db["users"].find()
    users = []
    for user in result:
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@router.get("/{user_id}", response_model=dict, dependencies=[Depends(get_current_user)])
async def read_user(user_id: int):
    
    result = db["users"].find_one({"id": user_id})
    return result

@router.post("/", response_model=dict, dependencies=[Depends(get_current_user)])
async def create_user(user: User, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    doesExist = db["users"].find_one({"email": user.email})
    if doesExist:
        return {"error": "User already exists"}
    result = db["users"].insert_one(user.serialized())
    insert = db["users"].find_one({"_id": result.inserted_id})

    insert["_id"] = str(insert["_id"])
    return insert

@router.put("/{user_id}", response_model=dict, dependencies=[Depends(get_current_user)])
async def update_user(user_id: str, user: User):
    result = db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": user.serialized()})
    return {"modified_count": result.modified_count}

from bson import ObjectId

@router.delete("/{user_id}", response_model=dict, dependencies=[Depends(get_current_user)])
async def delete_user(user_id: str):
    result = db["users"].delete_one({"_id": ObjectId(user_id)})
    return {"deleted_count": result.deleted_count}