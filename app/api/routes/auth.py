from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.exceptions import EmailAlreadyExistsError
from app.core.security import create_access_token, get_current_user, verify_password
from app.db.base import get_db
from app.db.models.user import User
from app.schemas.user import LoginRequest, TokenResponse, UserCreate, UserResponse
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, user_data)
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Email already registered")
    

# @router.post("/login", response_model=TokenResponse)
# def login(credentials: LoginRequest, db: Session = Depends(get_db)):
#     user = user_service.get_user_by_email(db, credentials.email)
#     if user is None or not verify_password(credentials.password, user.password_hash):
#         raise HTTPException(status_code=401, detail="Invalid email or password")

#     token = create_access_token(str(user.id))
#     return TokenResponse(access_token=token, token_type="bearer")


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_service.get_user_by_email(db, form_data.username)  # note: .username carries the email
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token, token_type="bearer")



@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user