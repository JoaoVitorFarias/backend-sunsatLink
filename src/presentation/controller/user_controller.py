from domain.entities.user import PerfilUsuarioEnum, UserRequest, UserResponse
from domain.entities.user import UserDB, UserBase
from security import get_password_hash
from fastapi import APIRouter, status, HTTPException, Response, Query, Header, Depends
from presentation.controller import userService
from security import get_password_hash
from database import engine, Base
from typing import List

def get_current_user(authorization: str = Header(...)):
    user = userService.verifyToken(authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or token expired"
        )
    user.senha = None  # Assegura que a senha não será retornada
    return user

Base.metadata.create_all(bind=engine)

router_user = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

@router_user.post("/", status_code=status.HTTP_201_CREATED)
def create(user_request: UserRequest):
    fieldsValidation = userService.validate_user(user_request)

    if not fieldsValidation['completeStatus']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)

    if userService.exists_by_email(user_request.email):
        raise HTTPException(status_code=400, detail="User already registered") 
        
    user_model = UserDB(
        **user_request.__dict__
    )

    userService.save(user_model)  

    return user_model


@router_user.get("/", response_model=List[UserBase])
def find_all(page: int = Query(1, alias="page"), 
             offset: int = Query(10, alias="offset")):
    skip = (page - 1) * offset
    limit = skip + offset

    user_DB = userService.find_all()
    return user_DB[skip:limit]


@router_user.get("/{email}", response_model = UserResponse)
def find_by_email(email : str, current_user: str = Depends(get_current_user)):
    user = userService.find_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "User not found"
        )
    return UserResponse.from_orm(user)


@router_user.put("/{email}", response_model=UserResponse)
def update_by_email(request: UserRequest, current_user: str = Depends(get_current_user)):
    fieldsValidation = userService.validate_user(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)

    if not userService.exists_by_email(request.email):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    
    user = userService.update(request)

    return UserResponse.from_orm(user)


@router_user.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_email(email: str, current_user: str = Depends(get_current_user)):
    if not userService.exists_by_email(email):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
        
    userService.delete_by_email(email)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router_user.patch("/{email}", response_model=UserResponse)
def update_approval_status(email: str, status: int):
    user = userService.find_by_email(email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User não encontrado"
        )
    
    updated_user = userService.update_approval_status(user, status)
    return UserResponse.from_orm(updated_user)

@router_user.patch("/{email}/promote-to-admin/", response_model=UserResponse)
def promote_user_to_admin(email: str, current_user: str = Depends(get_current_user)):
    user = userService.find_by_email(email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User não encontrado"
        )
    
    updated_user = userService.promote_user_to_admin(user)
    return UserResponse.from_orm(updated_user)
