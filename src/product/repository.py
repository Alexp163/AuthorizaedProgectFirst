from http.client import HTTPException

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from product.models import Product
from product.schemas import ProductCreateSchema, ProductReadSchema, ProductUpdateSchema


class Repository:

    async def create_product(self, product: ProductCreateSchema, session: AsyncSession):
        statement = insert(Product).values(
            title=product.title,
            data=product.data,
            user_id=product.user_id,
        ).returning(Product)
        result = await session.scalar(statement)
        await session.commit()
        return result

    async def get_products(self, session: AsyncSession) -> list[ProductReadSchema]:
        statement = select(Product)
        result = await session.scalars(statement)
        return result

    async def get_product_by_id(self, product_id: int, session: AsyncSession) -> ProductReadSchema:
        statement = select(Product).where(Product.id == product_id)
        result = await session.scalar(statement)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого id не существует")
        return result

    async def delete_product_by_id(self, product_id: int, session: AsyncSession) -> None:
        statement = select(Product).where(Product.id == product_id)
        result = await session.scalar(statement)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого id не существует")
        statement = delete(Product).where(Product.id == product_id)
        await session.execute(statement)
        await session.commit()

    async def update_product_by_id(self,product_id: int, product: ProductUpdateSchema,
                                   session: AsyncSession) -> ProductReadSchema:
        statement = update(Product).where(Product.id == product_id).values(
            title=product.title,
            data=product.data,
        ).returning(Product)
        result = await session.scalar(statement)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого id не существует")
        await session.commit()
        return result

