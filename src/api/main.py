from fastapi import FastAPI
from starlette import middleware
from src.api.router import router

app = FastAPI(title="personal chatbot", version="1.0.0")


middlewares = [
    middleware.CORSMiddleware(
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

# Include router
app.include_router(router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to the personal chatbot API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

