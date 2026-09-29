from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.jobs import router as jobs_router


app = FastAPI(
    title="ATS API",
    description="API-first Applicant Tracking System",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API routers
app.include_router(jobs_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }

