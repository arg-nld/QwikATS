from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.tenants import router as tenants_router
from app.api.jobs import router as jobs_router
from app.api.candidates import router as candidates_router
from app.api.applications import router as applications_router


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
app.include_router(tenants_router)
app.include_router(jobs_router)
app.include_router(candidates_router)
app.include_router(applications_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }