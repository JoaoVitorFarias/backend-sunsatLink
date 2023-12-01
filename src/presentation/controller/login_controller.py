from domain.entities.user import Status
from fastapi import APIRouter, Form, Header, HTTPException
from fastapi import status as fstatus
from presentation.controller import userService

routerLoginUser = APIRouter(
    prefix="/login",
    tags=["login: user"],
    responses={404: {"description": "Not found"}},
)

@routerLoginUser.post("/user/")
async def login(email: str = Form(...), password: str = Form(...)):
    access_token, refresh_token, role, status = userService.login(
        email=email, password=password
    )

    print("-------------------------", status)

    if not access_token:
        raise HTTPException(
            status_code=fstatus.HTTP_403_FORBIDDEN,
            detail="Email or username incorrect"
        )

    if status == Status.REJECTED:
        raise HTTPException(
            status_code=fstatus.HTTP_403_FORBIDDEN,
            detail="User was rejected by admin"
        )
    
    if status == Status.PENDING:
        raise HTTPException(
            status_code=fstatus.HTTP_403_FORBIDDEN,
            detail="User is not approved by admin yet"
        )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": role,
        "status": status
    }

@routerLoginUser.get("/user/token", status_code=201)
async def verificarToken(authorization: str = Header(...)):
    user = userService.verifyToken(authorization)
    user.senha = None
    return user

@routerLoginUser.post("/user/token/refresh", status_code=201)
async def refreshToken(refresh_token: str = Header(...)):
    tokens = userService.refreshSession(refresh_token=refresh_token)
    if tokens:
        return {
            "access_token": tokens[0],
            "refresh_token": tokens[1],
            "token_type": "bearer",
        }

    raise HTTPException(401, "Not Allowed")

@routerLoginUser.post("/user/logout")
def logout(refresh_token: str = Header(...)):
    userService.delete_refresh_token(refresh_token)

    return {"message": "Logout successfully performed"}