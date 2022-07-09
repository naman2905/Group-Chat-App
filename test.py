try:    
    import requests
    import json
    from jsonschema import validate
    import json
except:
    print("Some modules are missing")


BASE_URL = "http://localhost:9008/"

# Test Cases for Authentication

class TestRegister:
    url = f"{BASE_URL}auth/register"
    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    data = json.dumps({"mobile":9999999999, "username":"test", "password":"test-password"})
    
    def test_status_code(self):
        response = requests.post(self.url, data=self.data)
        assert response.status_code == 200
        
        
    def test_response_type(self):
        response = requests.post(self.url, data=self.data)
        assert response.headers["Content-Type"] == "application/json"
        
        
    def test_api_hit(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        assert response_body["success"] == True
        
    def test_response_body(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)
    
class TestLogin:
    url = f"{BASE_URL}auth/login"

    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    
    data = json.dumps({"mobile":9999999999, "password":"test-password"})
    
    def test_status_code(self):
        response = requests.post(self.url, data=self.data)
        assert response.status_code == 200
        
    def test_response_type(self):
        response = requests.post(self.url, data=self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.post(self.url, data = self.data)
        response_body = response.json()
        assert response_body["success"] == True
        
    def test_response_body(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)
             
class TestLogout:
    url =  f"{BASE_URL}auth/logout"

    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    data=json.dumps({"mobile":9999999999})
    def test_status_code(self):
        response = requests.post(self.url, data=self.data)
        assert response.status_code == 200
        
        
    def test_response_type(self):
        response = requests.post(self.url, data=self.data)
        assert response.headers["Content-Type"] == "application/json"
        
        
    def test_api_hit(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.post(self.url,data= self.data)
        response_body = response.json()
        assert response_body["success"] == True   # for 2 min gap in sending otp
        
    def test_response_body(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)


# Test Cases for User CRUD

class TestCreateUser:
    url =  f"{BASE_URL}users/create"
    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    data=json.dumps({"mobile":9999999999,"name":"test-name", "email":"test-email"})

    def test_status_code(self): 
        response = requests.post(self.url, data = self.data)
        response_body = response.json()
        assert response.status_code == 200
        
        
    def test_response_type(self):
        response = requests.post(self.url, data = self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.post(self.url, data = self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.post(self.url, data = self.data)
        response_body = response.json()
        assert response_body["success"] == True
    
    def test_response_body(self):
        response = requests.post(self.url, data = self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)

class TestUpdateUser:
    url =  f"{BASE_URL}users/update"
    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            },
            "data": {
            "type": "object"
            }
        }
    }
    data=json.dumps({"name":"test-name", "email":"test-email"})

    def test_status_code(self): 
        response = requests.patch(self.url, data = self.data)
        response_body = response.json()
        assert response.status_code == 200
        
        
    def test_response_type(self):
        response = requests.patch(self.url, data = self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.patch(self.url, data = self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.patch(self.url, data = self.data)
        response_body = response.json()
        assert response_body["success"] == True
    
    def test_response_body(self):
        response = requests.patch(self.url, data = self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)

class TestDeleteUser:
    url =  f"{BASE_URL}users/delete"
    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    data={"user_id":"62c6a6a35a9fa5b9f08a1544"}

    def test_status_code(self): 
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert response.status_code == 200
        
        
    def test_response_type(self):
        response = requests.delete(self.url, params = self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert response_body["success"] == True
    
    def test_response_body(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)



# Test Cases for Group CRUD

class TestCreateGroup:
    url =  f"{BASE_URL}groups/create-group"
    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    data = {
            "members":["62c6a5881704bd596a64a151"],
            "group_name":"test-group"
        }
    data=json.dumps(data)

    def test_status_code(self): 
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert response.status_code == 200
        
        
    def test_response_type(self):
        response = requests.delete(self.url, params = self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert response_body["success"] == True
    
    def test_response_body(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)

class TestUpdateGroup:
    url =  f"{BASE_URL}groups/update-group"
    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    data = {
        "group_id":"",
        "group_name":"updated-group-name"
    }
    data=json.dumps(data)

    def test_status_code(self): 
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert response.status_code == 200
        
        
    def test_response_type(self):
        response = requests.delete(self.url, params = self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert response_body["success"] == True
    
    def test_response_body(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)

class TestDeleteGroup:
    url =  f"{BASE_URL}groups/delete-group"
    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    data={"group_id":""}

    def test_status_code(self): 
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert response.status_code == 200
        
        
    def test_response_type(self):
        response = requests.delete(self.url, params = self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        assert response_body["success"] == True
    
    def test_response_body(self):
        response = requests.delete(self.url, params = self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)



# Test Cases for Group Members CRUD

class TestAddMember:
    url = f"{BASE_URL}groups/add-member"

    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    data = {
            "members":["62c70663c676238ae08c97bb", "62c6a853e67c2a6c52cd4a10"],
            "group_id":"62c70aa8358c505d1d965ea2"
        }
    
    data = json.dumps(data)
    
    def test_status_code(self):
        response = requests.post(self.url, data=self.data)
        assert response.status_code == 200
        
    def test_response_type(self):
        response = requests.post(self.url, data=self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.post(self.url, data = self.data)
        response_body = response.json()
        assert response_body["success"] == True
        
    def test_response_body(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)
   
class TestDeleteMember:
    url = f"{BASE_URL}groups/delete-member"

    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    
    data = {
        "user_id":"62c6a853e67c2a6c52cd4a10",
        "group_id":"62c70aa8358c505d1d965ea2"
    }    
    def test_status_code(self):
        response = requests.delete(self.url, params= self.data)
        assert response.status_code == 200
        
    def test_response_type(self):
        response = requests.delete(self.url, params= self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.delete(self.url, params= self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.delete(self.url, params= self.data)
        response_body = response.json()
        assert response_body["success"] == True
        
    def test_response_body(self):
        response = requests.delete(self.url, params= self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)
   
class TestSearchMember:
    url = f"{BASE_URL}groups/search-member"

    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    
    data = {
        "mobile": "9999999999",
        "group_id":"62c6a8a80416009a8b1af01f"
    }
    
    def test_status_code(self):
        response = requests.get(self.url, params = self.data)
        assert response.status_code == 200
        
    def test_response_type(self):
        response = requests.get(self.url, params = self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.get(self.url, params = self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.get(self.url, params = self.data)
        response_body = response.json()
        assert response_body["success"] == True
        
    def test_response_body(self):
        response = requests.get(self.url, params = self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)
   
class TestGetAllMember:
    url = f"{BASE_URL}groups/get-all-members"

    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    
    
    def test_status_code(self):
        response = requests.get(self.url)
        assert response.status_code == 200
        
    def test_response_type(self):
        response = requests.get(self.url)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.get(self.url)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.get(self.url)
        response_body = response.json()
        assert response_body["success"] == True
        
    def test_response_body(self):
        response = requests.get(self.url)
        response_body = response.json()
        validate(response_body, schema=self.schema)
   


# Test Cases for Group Chat Messages

class TestSendMessage:
    url = f"{BASE_URL}groups/send-messages"

    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    data = {
            "msg":"Hii!",
            "user_id":"62c6a5881704bd596a64a151",
            "group_id":"62c70aa8358c505d1d965ea2"
        }
    
    data = json.dumps(data)
    
    def test_status_code(self):
        response = requests.post(self.url, data=self.data)
        assert response.status_code == 200
        
    def test_response_type(self):
        response = requests.post(self.url, data=self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.post(self.url, data = self.data)
        response_body = response.json()
        assert response_body["success"] == True
        
    def test_response_body(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)
   
class TestLikeMessage:
    url = f"{BASE_URL}groups/like-message"

    schema = {
        "type" : "object",
        "properties" : {
            "message": {
            "type": "string"
            },
            "success": {
            "type": "boolean"
            }
        }
    }
    data = {
            "user_id":"62c6a83de67c2a6c52cd4a0f",
            "msg_id":"62c6d4629df6f4c2e316b360", 
            "group_id":"62c6a8a80416009a8b1af01f"
        }
    
    data = json.dumps(data)
    
    def test_status_code(self):
        response = requests.post(self.url, data=self.data)
        assert response.status_code == 200
        
    def test_response_type(self):
        response = requests.post(self.url, data=self.data)
        assert response.headers["Content-Type"] == "application/json"
        
    def test_api_hit(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        assert "success" in response_body

    def test_response_body_status(self):
        response = requests.post(self.url, data = self.data)
        response_body = response.json()
        assert response_body["success"] == True
        
    def test_response_body(self):
        response = requests.post(self.url, data=self.data)
        response_body = response.json()
        validate(response_body, schema=self.schema)
   
