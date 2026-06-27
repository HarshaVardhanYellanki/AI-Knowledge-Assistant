from bson import ObjectId

from app.database.mongodb import users_collection


async def get_users():
    return await users_collection.find().to_list(length=None)


async def get_user_by_id(user_id: str):

    return await users_collection.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )