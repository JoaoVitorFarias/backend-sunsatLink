from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from presentation.controller.satellite_controller import router_satellite
from presentation.controller.antenna_controller import router_antenna

from presentation.controller.login_controller import (
    routerLoginUser,
)
from presentation.controller.user_controller import router_user

load_dotenv()
app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(router_satellite)
app.include_router(router_antenna)
app.include_router(router_user)
app.include_router(routerLoginUser)

@app.get("/")
def read_root():
    return {"hello": "world"}
