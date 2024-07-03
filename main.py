from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import json_util

app = FastAPI(
    docs_url='/'
)

# MongoDB connection
client = AsyncIOMotorClient("mongodb+srv://allGroup:Estiam75020@nfcreader.5mrffd4.mongodb.net/")
db = client["NFCReader"]
collection = db["users"]

class User(BaseModel):
    sub: str
    name: str
    email: str
    iat: int
    exp: int
    role: str

@app.post("/users/")
async def create_user(user: User):
    try:
        await collection.insert_one(user.dict())
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/")
async def read_users():
    try:
        users = await collection.find().to_list(length=100)
        return json_util.dumps(users)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{sub}")
async def read_user(sub: str):
    try:
        user = await collection.find_one({"sub": sub})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return json_util.dumps(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/users/{sub}")
async def update_user(sub: str, user: User):
    try:
        await collection.update_one({"sub": sub}, {"$set": user.dict()})
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{sub}")
async def delete_user(sub: str):
    try:
        await collection.delete_one({"sub": sub})
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))