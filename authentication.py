import datetime
from decouple import config
from pymongo import MongoClient
from fastapi import APIRouter , Request
import re

router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)


# connection to the database
client = MongoClient(config("DB_URL"))
mydb=client[config("DB_NAME")]              


# Authentication APIs

@router.post('/register')
async def register_user(request:Request):
    '''
    API Endpoint for registering user
    body = {
            "mobile":mobile, 
            "username": username,
            "password":password 
    }
    '''  
    data = await request.json()
    data["created_at"]=datetime.datetime.now()
    data["updated_at"]=datetime.datetime.now()
    data["is_loggedin"] = False
    existing_user = mydb.registered_user.find_one({"mobile":data['mobile']})
    if existing_user:
        response = {   
            "message":"User already exists",
            "success":True
            }
        return response
    mydb.registered_user.insert(data)
    response = {
        "message":"User registered successfully",
        "success":True
    }
    return response
    
@router.post('/login')
async def login(request: Request):
    '''
    API Endpoint for user login
    body = {
            "mobile":mobile, 
            "password":password, 
    }
    '''
    user= await request.json()
    mobile=str(user.get("mobile", ""))
    password = user.get("password", "")
    if len(mobile)==0 or not password:
        response={
            "message":"Please Enter a Number/Password",
            "success":False
        }
        return response

    if not re.match(r'[6789]\d{9}$', mobile):
        response={
            "message":"Please Enter Valid Number",
            "success":False
        }
        return response

    if len(mobile)!=10:
        response={
            "message":"Please Enter Valid Number",
            "success":False
        }
        return response

    registered_user = mydb.registered_user.find_one({"mobile":int(mobile)})
    if not registered_user:
        response = {
            "message":"Registered first to login", 
            "status":True
        }
        return response
    user = mydb.registered_user.find_one({"mobile":int(mobile), "password":password})
    if user:
        mydb.registered_user.find_one_and_update({"mobile":int(mobile)}, {"$set":{"is_loggedin":True}})
        response = {
            "message":"Login successfully", 
            "status":True
        }
        return response
    else:
        response = {
            "message":"Password incorrect", 
            "success":True
        }
        return response

@router.post('/logout')
async def logout(request: Request, payload=None):
    '''
    API Endpoint for user logout
    body = {
            "mobile":mobile
    '''
    user= await request.json()
    mobile=str(user['mobile'])
    if len(mobile)==0 :
        response={
            "message":"Please Enter a Number/Password",
            "success":False
        }
        return response

    if not re.match(r'[6789]\d{9}$', mobile):
        response={
            "message":"Please Enter Valid Number",
            "success":False
        }
        return response

    if len(mobile)!=10:
        response={
            "message":"Please Enter Valid Number",
            "success":False
        }
        return response

    registered_user = mydb.registered_user.find_one({"mobile":int(mobile)})
    if not registered_user:
        response = {
            "message":"User not found", 
            "status":True
        }
        return response

    #check if user is already logged out 
    user = mydb.registered_user.find_one({"mobile":int(mobile), "is_loggedin":False})
    if user:
        response = {
            "message":"Already Logged out", 
            "status":True
        }
        return response
    else:
        user = mydb.registered_user.find_one_and_update({"mobile":int(mobile)}, {"$set":{"is_loggedin":False}})
        response = {
            "message":"Logged Out Successfully", 
            "success":True
        }
        return response

