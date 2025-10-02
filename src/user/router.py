from fastapi import APIRouter, Depends, status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from user.schemas import UserReadSchema, UserCreateSchema, UserUpdateSchema, AccessTokenSchema
from .jwt_repository import CredentialsRepository
from .repository import Repository

router = APIRouter(tags=["users"], prefix="/users")
get_token = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post("/register")  # регистрация
async def register(user: UserCreateSchema, session: AsyncSession = Depends(get_async_session),
                   repository: Repository = Depends()) -> None:
    user = await repository.create_user(user, session)

@router.post("/login")
async def login(session: AsyncSession = Depends(get_async_session),
                credentials: OAuth2PasswordRequestForm = Depends(),
                repository_user: Repository = Depends(),
                repository: CredentialsRepository = Depends()) -> AccessTokenSchema:
    user = await repository_user.get_user(credentials.username, credentials.password, session)
    token = repository.make_token(user.id)
    return AccessTokenSchema(
        access_token=token,
        token_type="Bearer"
    )

@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(repository: Repository = Depends(),
                    session = Depends(get_async_session)) -> list[UserReadSchema]:
    return await repository.get_users(session)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: int, token: str = Depends(get_token),
                            repository_user: Repository = Depends(),
                            repository: CredentialsRepository = Depends(),
                            session: AsyncSession = Depends(get_async_session)) -> None:
        token_user_id = repository.valid_and_decode_token(token)
        if token_user_id == user_id:
            user = await repository_user.delete_user_by_id(user_id, session)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Отказано в доступе")


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user_by_id(user_id: int, user: UserUpdateSchema, token: str = Depends(get_token),
                            session=Depends(get_async_session),
                            repository_user: Repository = Depends(),
                            repository: CredentialsRepository = Depends()) -> UserReadSchema:
    token_user_id = repository.valid_and_decode_token(token)
    if token_user_id == user_id:
        user_token = await repository_user.update_user_by_id(user_id, user, session)
        return user_token
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе"
        )
