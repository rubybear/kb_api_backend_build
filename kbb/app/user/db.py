import motor.motor_asyncio

from kbb.core.config import settings

database_url = settings.MONGODB_URI
client = motor.motor_asyncio.AsyncIOMotorClient(
    database_url,
    uuidRepresentation="standard"
)
user_db = client.kettlebell_barbell
