import datetime
from decouple import config
from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi import APIRouter , Request

router = APIRouter(
    prefix='/groups',
    tags=['group']
)

# connection to the database
client = MongoClient(config("DB_URL"))
mydb=client[config("DB_NAME")]              


# Group CRUD APIs

@router.post('/create_group')
async def create_grp(request:Request):
    try:
        data = await request.json()
        members = data.get("members" , "")
        group_name = data.get("group_name" , "")
        if group_name and members:
            group_check = mydb.groups.find_one({"group_name":group_name})
            print(group_check)
            if group_check:
                response = {
                "msg":"Group with this name already exists",
                "status":True
            }
            else:
                mydb.groups.insert({"group_name":group_name , "members":members})
                response = {
                        "msg":"Group created successfully.",
                        "status":True
                    }
            
        if not members or not group_name:
            response = {
                "msg":"Please input members/grp name",
                "status":True
            }
            return response
        if not isinstance(members , list) or not isinstance(group_name , str):
            response = {
                "msg":"Please provide members/group_name in proper format",
                "status":True
            }
        return response
    except Exception as e:
        response = {
            "msg":str(e),
            "status":False
            }
        return response

@router.delete('/delete_group')
def delete_group(request:Request , group_id:str = None):
    try:
        group_id = request.query_params.get("group_id")
        if group_id:
            deleted_group = mydb.groups.find_one_and_delete({"_id":ObjectId(group_id)}, {"members":1})
            if deleted_group:
                response = {
                    "msg":"Group Deleted Successfully.",
                    "status":True
                }
            else:
                response = {
                    "msg":"Group not found.",
                    "status":True
                }
        else:
            response = {
                "msg":"Please provide group id",
                "status":True
            }
        return response
    except Exception as e:
        response = {
            "msg":str(e),
            "status":True
            }
        return response

@router.patch('/update_group_details')
async def update_group(request:Request , group_id:str= None):
    try:
        group_id = request.query_params.get("group_id")
        data = await request.json()
        data["updated_at"]=datetime.datetime.now()
        if group_id:
            updated_details = mydb.groups.find_one_and_update({"_id":ObjectId(group_id)} , {"$set":data})
            if updated_details:
                response = {
                    "msg":"Data updated successfully",
                    "data":data, 
                    "success":True
                }
            else:
                response = {
                    "msg":"Group not found.",
                    "status":True
                }
        else:
            response = {
            "msg":"Provide Group ID", 
            "success":True
        }
        return response
    except Exception as e:
        response = {
            "msg":str(e),
            "success":False 
        }
        return response


# Group Members APIs

@router.post('/add-member')
async def create_grp(request:Request):
    try:
        data = await request.json()
        members = data.get("members" , "")
        group_id = data.get("group_id" , "")
        if group_id and members:
            existing_members_list = mydb.groups.find_one({"_id":ObjectId(group_id)} , {"members":1})
            
            duplicate_members_list = []
            for member in members:
                if member in existing_members_list['members']:
                    duplicate_members_list.append(member)

            final_members_to_be_add = list(set(members)-set(duplicate_members_list))

            if existing_members_list:
                for i in members:
                    existing_members_list.get("members").append(i)
                mydb.groups.find_one_and_update({"_id":ObjectId(group_id)},{"$set":{"members":final_members_to_be_add}})                
                response = {
                        "msg":"Participants added successfully.",
                        "status":True
                    }
            else:
                response = {
                        "msg":"Group does not exists.",
                        "status":True
                    }
        if not members or not group_id:
            response = {
                "msg":"Please input members/grp name",
                "status":True
            }
            return response
        if not isinstance(members , list) or not isinstance(group_id , str):
            response = {
                "msg":"Please provide members/group_name in proper format",
                "status":True
            }
        return response
    except Exception as e:
        response = {
            "msg":str(e),
            "status":False
            }
        return response

@router.delete('/delete-member')
def delete_user(request:Request , user_id:str= None , group_id:str= None):
    try:
        user_id = request.query_params.get("user_id")
        group_id = request.query_params.get("group_id")
        if user_id and group_id:
            deleted_user = mydb.user.find_one_and_delete({"user_id":ObjectId(user_id) , "group_id":ObjectId(group_id)})
            if deleted_user:
                response = {
                    "msg":"Deleted user successfully.",
                    "status":True
                }
            else:
                response = {
                    "msg":"User/Group not found.",
                    "status":True
                }
        else:
            response = {
                "msg":"Please provide user id/group id",
                "status":True
            }
        return response
    except Exception as e:
        response = {
            "msg":str(e),
            "status":True, 
            }
        return response

@router.get('/get-all-members')
def get_user_list(request:Request , group_id:str = None):
    try:
        group_id = request.query_params.get("group_id")
        data = []
        if group_id:
            user = mydb.groups.find_one({"_id":ObjectId(group_id)}, {"members":1})
            for i in user['members']:
                user_detail = mydb.user.find_one({"_id":ObjectId(i)}, {"_id":0, "name":1 , "mobile":1})
                data.append(user_detail)
            if user:
                response = {
                    "msg":"Here is the complete members list.",
                    "data":data,
                    "status":True
                }
            else:
                response = {
                    "msg":"No member found.",
                    "status":True
                }
        else:
            response = {
                "msg":"Please provide group id",
                "status":True
            }
        return response
    except Exception as e:
        response = {
            "msg":str(e),
            "status":True
            }
        return response

@router.get('/search_member')
def search_member(request:Request , mobile:int=None , group_id:str=None):
    try:
        mobile = int(request.query_params.get("mobile"))
        group_id = request.query_params.get("group_id")
        user_id = mydb.user.find_one({"mobile":mobile})
        user_id['_id'] = str(user_id['_id'])
        member = mydb.groups.find_one({"members":{"$all":[user_id['_id']]} , "_id":ObjectId(group_id)})
        if not mobile or not group_id or not user_id:
            response = {
                "msg":"provide complete data" , 
                "status":True
            }
            return response
        if member:
            response = {
                "msg":"user found" , 
                "data":user_id ,
                "status":True
            }
            return response
        else:
            response = {
            "msg":"user not found" , 
            "status":True
            }
            return response
    except Exception as e:
        response = {
                "msg":str(e) , 
                "status":False
        }
        return response


# Group Chat APIs

@router.post('/send_messages')
async def send_msgs(request:Request):
    try:
        data = await request.json()
        message = data.get("msg", "")
        user_id = data.get("user_id", "")
        group_id = data.get("group_id", "")
        if user_id and message and group_id:
            group_member = mydb.groups.find_one({"_id":ObjectId(group_id), "members":{"$all":[user_id]}})
            if group_member:
                grp = mydb.chat.find_one({"group_id":ObjectId(group_id)})
                users = []
                if grp:
                    users = grp.get("users" , [])
                user_chat = mydb.chat.find_one({"group_id":ObjectId(group_id), "users":{"$elemMatch":{"user_id":ObjectId(user_id)}}} , {"users.$":1})
                print("mss", user_chat)
                if user_chat:
                    msgs = user_chat["users"][0]['msgs']
                    msg = ObjectId()
                    msgs.append(msg)
                    mydb.messages.insert({"_id":msg,"message":message , "liked":False , "send_at":datetime.datetime.now()})
                    mydb.chat.find_one_and_update({"group_id":ObjectId(group_id) , "users.user_id":ObjectId(user_id)}, {"$set":{"users.$.msgs":user_chat['users'][0]['msgs']}})
                else:
                    msg = {"user_id":ObjectId(user_id) , "msgs":[ObjectId()]}
                    users.append(msg)
                    mydb.messages.insert({"_id":msg['msgs'][0],"message":message , "liked":False , "send_at":datetime.datetime.now()})
                    mydb.chat.find_one_and_update({"group_id":ObjectId(group_id)}, {"$set":{"users":users}} , upsert=True)
                response = {
                        "msg":"Message send successfully.",
                        "status":True
                    }
            else:
                response = {
                        "msg":"User does not belong to this grp.",
                        "status":True
                    }
        if not user_id or not message or not group_id:
            response = {
                "msg":"Please input msg/user id/group_id",
                "status":True
            }
            return response
        if not isinstance(user_id , str) or not isinstance(message , str) or not isinstance(group_id , str):
            response = {
                "msg":"Please provide user id/message in proper format",
                "status":True
            }
        return response
    except Exception as e:
        response = {
            "msg":str(e),
            "status":False
            }
        return response

@router.post('/like-message')
async def like_msg(request:Request):
    try:
        data = await request.json()
        message_id = data.get("msg_id" , "")
        user_id = data.get("user_id" , "") 
        group_id = data.get("group_id" , "")
        if user_id and message_id and group_id:
            in_grp = mydb.groups.find_one({"members":{"$all":[user_id]} , "_id":ObjectId(group_id)})
            if in_grp:
                msg= mydb.messages.find_one_and_update({"_id":ObjectId(message_id)},{"$set":{"liked":True}})
                if msg:
                    response = {
                        "msg":"Liked message Successfully",
                        "status":True
                    }
                else:
                    response = {
                        "msg":"Wrong msg id",
                        "status":True
                    }
            else:
                response = {
                    "msg":"User does not belong to this group",
                    "status":True
                }
        if not user_id or not message_id or not group_id:
            response = {
                "msg":"Please input msg/user id/group_id",
                "status":True
            }
            return response
        if not isinstance(user_id , str) or not isinstance(message_id , str) or not isinstance(group_id , str):
            response = {
                "msg":"Please provide user id/message/group_id in proper format",
                "status":True
            }
        return response
    except Exception as e:
        response = {
            "msg":str(e),
            "status":False
            }
        return response


