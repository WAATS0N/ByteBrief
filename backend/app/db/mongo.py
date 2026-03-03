from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.MONGODB_DB_NAME]

# Collections
articles_col = db["articles"]
users_col = db["users"]
events_col = db["user_events"]
profiles_col = db["user_profiles"]
