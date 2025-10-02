import hashlib
from random import choices
from string import ascii_letters

from fastapi import status, HTTPException, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .models import User
from .schemas import UserCreateSchema, UserReadSchema, UserUpdateSchema


class Repository:

    def get_hash(self, password: str, salt:str) -> str:
        password_hash = hashlib.sha256(password.encode() + salt.encode()).hexdigest()
        return password_hash


    async def create_user(self, user: UserCreateSchema, session: AsyncSession) -> UserReadSchema:
        statement = select(User).where(User.nickname == user.nickname)
        result = await session.scalar(statement)
        if result is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой пользователь уже есть")
        salt = "".join(choices(ascii_letters, k=16))
        password_hash = self.get_hash(user.password, salt)
        statement = insert(User).values(
            nickname=user.nickname,
            password_hash=password_hash,
            password_salt=salt,
        ).returning(User)
        result = await session.scalar(statement)
        await session.commit()
        return result


    async def get_users(self, session: AsyncSession) -> list[UserReadSchema]:
        statement = select(User)
        result = await session.scalars(statement)
        return result

    async def get_user(self, nickname: str, password: str, session: AsyncSession) -> UserReadSchema:
        statement = select(User).where(User.nickname == nickname)
        result = await session.scalar(statement)
        if result is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")
        password_hash = self.get_hash(password, result.password_salt)
        if result.password_hash == password_hash:
            return result
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")

    async def delete_user_by_id(self, user_id: int, session: AsyncSession) -> None:
        statement = select(User).where(User.id == user_id)
        user = await session.scalar(statement)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого пользователя нет")
        statement = delete(User).where(User.id == user_id)
        await session.execute(statement)
        await session.commit()


    async def update_user_by_id(self, user_id: int, user: UserUpdateSchema,
                                session: AsyncSession) -> UserReadSchema:
        statement = select(User).where(User.id == user_id)
        result = await session.scalar(statement)
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого id  не существует")
        if result.id == user_id:
            salt = "".join(choices(ascii_letters, k=16))
            password_hash = self.get_hash(user.password, salt)
            statement = update(User).where(User.id == user_id).values(
                nickname=user.nickname,
                password_hash=password_hash,
                password_salt=salt,
            ).returning(User)
            result = await session.scalar(statement)
            await session.commit()
            return result
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Отказано в доступе")