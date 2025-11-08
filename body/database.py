import motor.motor_asyncio
from info import *

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB)
db = client.captions_with_chnl
chnl_ids = db.chnl_ids
users = db.users

async def addCap(chnl_id, caption):
    dets = {"chnl_id": chnl_id, "caption": caption}
    await chnl_ids.insert_one(dets)


async def updateCap(chnl_id, caption):
    await chnl_ids.update_one({"chnl_id": chnl_id}, {"$set": {"caption": caption}})

async def insert(user_id):
    user_det = {"_id": user_id}
    try:
        await users.insert_one(user_det)
    except:
        pass
        
async def total_user():
    user = await users.count_documents({})
    return user

async def getid():
    all_users = users.find({})
    return all_users

async def delete(id):
    await users.delete_one(id)

# Add these at the end of your database.py file

banned_users = db.banned_users
banned_channels = db.banned_channels

# For Banning Users
async def is_user_banned(user_id: int) -> bool:
    return bool(await banned_users.find_one({"user_id": user_id}))

async def add_user_ban(user_id: int):
    if not await is_user_banned(user_id):
        await banned_users.insert_one({"user_id": user_id})

async def rm_user_ban(user_id: int):
    if await is_user_banned(user_id):
        await banned_users.delete_one({"user_id": user_id})

# For Banning Channels
async def is_chnl_banned(chnl_id: int) -> bool:
    return bool(await banned_channels.find_one({"chnl_id": chnl_id}))

async def add_chnl_ban(chnl_id: int):
    if not await is_chnl_banned(chnl_id):
        await banned_channels.insert_one({"chnl_id": chnl_id})

async def rm_chnl_ban(chnl_id: int):
    if await is_chnl_banned(chnl_id):
        await banned_channels.delete_one({"chnl_id": chnl_id})
