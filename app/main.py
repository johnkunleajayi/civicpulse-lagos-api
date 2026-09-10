from fastapi import FastAPI

app = FastAPI(
    title="CivicPulse Lagos API",
    description="Trusted civic information for Lagos residents.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "CivicPulse Lagos",
        "tagline": "Know. Verify. Act.",
        "status": "online",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }