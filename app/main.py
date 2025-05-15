from fastapi import FastAPI
from app.api.v1.routers.email_router import router as email_router

app = FastAPI(title="Email Sending Service")
app.include_router(email_router, prefix="/api/v1")
