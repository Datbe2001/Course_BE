import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from app.core.settings import settings
from app.route import route

app = FastAPI(title="Course", version="1.1.1")

app.include_router(route, prefix="")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, debug=settings.DEBUG)
