from fastapi import FastAPI
from routers import router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)