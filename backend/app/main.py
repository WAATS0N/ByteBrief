from fastapi import FastAPI
from app.api import news, search, users, events
from app.core.config import settings

app = FastAPI(
    title="ByteBrief API",
    description="AI-Powered News Aggregation & Digest Platform",
    version="1.0.0"
)

# Routes
app.include_router(news.router)
app.include_router(search.router)
# Users and events routers will be implemented in later phases
# app.include_router(users.router)
# app.include_router(events.router)

@app.get("/")
async def root():
    return {"message": "Welcome to ByteBrief API", "docs": "/docs"}
