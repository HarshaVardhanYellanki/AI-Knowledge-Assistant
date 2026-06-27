from fastapi import FastAPI

from app.routes.auth_route import router as auth_router
from app.routes.user_route import router as user_router
from app.routes.document_route import router as document_router

app = FastAPI(
    title="AI Knowledge Assistant API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(document_router)