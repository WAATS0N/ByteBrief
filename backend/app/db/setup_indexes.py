import asyncio
from app.db.mongo import articles_col, users_col, events_col, profiles_col
from loguru import logger

async def setup_indexes():
    logger.info("Setting up MongoDB indexes...")

    # Articles
    await articles_col.create_index("article_id", unique=True)
    await articles_col.create_index("publish_date")
    await articles_col.create_index("source_name")
    await articles_col.create_index("category")
    await articles_col.create_index("whoosh_indexed")
    await articles_col.create_index("digest_generated")
    await articles_col.create_index([("title", "text"), ("content_clean", "text")])
    logger.info("Articles indexes created.")

    # Users
    await users_col.create_index("email", unique=True)
    await users_col.create_index("username", unique=True)
    logger.info("Users indexes created.")

    # Events
    await events_col.create_index("user_id")
    await events_col.create_index("article_id")
    await events_col.create_index("timestamp")
    logger.info("Events indexes created.")

    # Profiles
    await profiles_col.create_index("user_id", unique=True)
    logger.info("Profiles indexes created.")

    logger.info("All indexes created successfully.")

if __name__ == "__main__":
    asyncio.run(setup_indexes())
