from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# MongoDB connection
client = AsyncIOMotorClient("mongodb+srv://allGroup:Estiam75020@nfcreader.5mrffd4.mongodb.net/")
db = client["NFCReader"]
collection = db["users"]

class User(BaseModel):
    id: int
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
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{id}")
async def read_user(id: int):
    try:
        user = await collection.find_one({"id": id})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/users/{id}")
async def update_user(id: str, user: User):
    try:
        await collection.update_one({"id": id}, {"$set": user.dict()})
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{id}")
async def delete_user(id: int):
    try:
        await collection.delete_one({"id": id})
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))