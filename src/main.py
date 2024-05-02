import sys
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from src.users.views import user_router

app = FastAPI()

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix='/user')

app.include_router(main_api_router)


if __name__ == '__main__':
    print(sys.path)
    uvicorn.run(app, host="0.0.0.0", port=5000)
    