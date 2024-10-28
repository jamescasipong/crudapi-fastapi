from fastapi import APIRouter, Depends, HTTPException, status # Importing the APIRouter, Depends, HTTPException, and status classes
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # Importing the OAuth2PasswordBearer and OAuth2PasswordRequestForm classes
from datetime import  timedelta # Importing the datetime and timedelta modules
from database import db # Importing the database connection
from models import User # Importing the User model
from dotenv import load_dotenv # Importing the load_dotenv function
from auth import verify_password, get_password_hash # Importing the helper functions
from auth import get_current_user, create_access_token # Importing the get_current_user and create_access_token functions
from bson import ObjectId
from jose import jwt
from auth import SECRET_KEY, ALGORITHM
load_dotenv()


router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    user_dict = user.serialized()
    user_dict["password"] = get_password_hash(user_dict.pop("password"))
    if db["users"].find_one({"username": user_dict["username"]}):
        raise HTTPException(status_code=400, detail="Username already registered")
    db["users"].insert_one(user_dict)
    return {"msg": "User registered successfully"}


@router.get("/", response_model=list)
async def read_all(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You're not authorized to create a user. Only admins can create users.")
    result = db["users"].find()
    users = []
    for user in result:
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@router.post("/", response_model=dict)
async def create_user(user: User, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You're not authorized to create a user. Only admins can create users.")
    doesExist = db["users"].find_one({"email": user.email})
    if doesExist:
        return {"error": "User already exists"}
    result = db["users"].insert_one(user.serialized())
    insert = db["users"].find_one({"_id": result.inserted_id})

    insert["_id"] = str(insert["_id"])
    return insert

@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: str, user: User, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You're not authorized to create a user. Only admins can create users.")
    result = db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": user.serialized()})
    return {"modified_count": result.modified_count}


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You're not authorized to create a user. Only admins can create users.")
    
    if user_id == current_user["_id"]:
        raise HTTPException(status_code=403, detail="You can't delete yourself")
    
    if db["users"].count_documents({"_id": ObjectId(user_id)}) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    

    result = db["users"].delete_one({"_id": ObjectId(user_id)})
    return {"deleted_count": result.deleted_count}