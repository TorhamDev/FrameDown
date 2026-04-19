from fastapi import FastAPI

from app.api.v1.user import router as user_router
from app.api.v1.videos import router as videos_router

app = FastAPI(debug=True)

app.include_router(user_router)
app.include_router(videos_router)
