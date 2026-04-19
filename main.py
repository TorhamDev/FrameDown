from fastapi import FastAPI

from app.api.v1.user import router as user_router

app = FastAPI(debug=True)

app.include_router(user_router)
