from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="ATS API",
    description="API-first Applicant Tracking System",
    version="0.1.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


# --------------------------------------------------
# Mock Jobs Endpoint
# --------------------------------------------------

@app.get("/api/jobs")
def get_jobs():
    return [
        {
            "id": 1,
            "title": "Software Engineer",
            "department": "Engineering",
            "location": "Manila, Philippines",
            "employment_type": "Full-time",
        },
        {
            "id": 2,
            "title": "Data Analyst",
            "department": "Data",
            "location": "Remote",
            "employment_type": "Full-time",
        },
    ]