import datetime
from decouple import config
from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi import APIRouter , Request

router = APIRouter(
    prefix='/users',
    tags=['users']
)

# connection to the database
client = MongoClient(config("DB_URL"))
mydb=client[config("DB_NAME")]              

# User CRUD APIs

@router.post('/create')
async def create_user(request:Request):
    try:    
        data = await request.json()
        if data is None:
            return {"message":"provide data" , "success":True}
        data["created_at"]=datetime.datetime.now()
        data["updated_at"]=datetime.datetime.now()
        mydb.user.insert(data)
        response = {
            "message":"user created successfully",
            "success":True
        }
        return response
        
    except Exception as e:
        response = {
            "message":str(e),
            "success":False 
        }
        return response

@router.patch('/update')
async def update_user(request:Request , user_id:str=None):
    try:    
        user_id = request.query_params.get("user_id")
        data = await request.json()
        data["updated_at"]=datetime.datetime.now()
        if user_id:
            updated_user = mydb.user.find_one_and_update({"_id":ObjectId(user_id)} , {"$set":data})
            if updated_user:
                response = {
                    "message":"Data updated successfully",
                    "data":data, 
                    "success":True
                }
            else:
                response = {
                    "message":"User not found.",
                    "status":True
                }
        else:
            response = {
            "message":"User does not exists/ Incorrect User ID", 
            "success":True
        }
        return response
    except Exception as e:
        response = {
            "message":str(e),
            "success":False 
        }
        return response

@router.delete('/delete')
def delete_user(request:Request , user_id:str=None):
    try:
        user_id = request.query_params.get("user_id")
        if user_id:
            deleted_user = mydb.user.find_one_and_delete({"_id":ObjectId(user_id)})
            if deleted_user:
                response = {
                    "message":"Deleted user successfully.",
                    "status":True
                }
            else:
                response = {
                    "message":"User not found.",
                    "status":True
                }
        else:
            response = {
                "message":"Please provide user id",
                "status":True
            }
        return response
    except Exception as e:
        response = {
            "message":str(e),
            "status":True
            }
        return response
