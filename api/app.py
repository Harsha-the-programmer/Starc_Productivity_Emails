from fastapi import FastAPI
from api.routes.email_routes import router as email_router

app = FastAPI(
    title="Productivity AI API",
    description="Generates productivity emails",
    version="1.0"
)

app.include_router(email_router)


@app.get("/health")
def health():
    return {"status": "running"}
