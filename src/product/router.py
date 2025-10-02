from fastapi import APIRouter, Depends, status, HTTPException

from database import get_async_session
from product.repository import Repository
from product.schemas import ProductCreateSchema, ProductReadSchema, ProductUpdateSchema
from user.jwt_repository import CredentialsRepository
from user.router import get_token

router = APIRouter(tags=["products"], prefix="/products")

@router.post("/", status_code=status.HTTP_201_CREATED)  # создание продукта
async def create_product(product: ProductCreateSchema, repository: Repository = Depends(),
                         session = Depends(get_async_session), token: str = Depends(get_token),
                         jwt_repository: CredentialsRepository = Depends()):
    token_user_id = jwt_repository.valid_and_decode_token(token)
    if token_user_id == product.user_id:
        return await repository.create_product(product, session)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="В доступе отказано")

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)  # удалить продукт по id
async def delete_product_by_id(product_id: int, repository: Repository = Depends(),
                               session = Depends(get_async_session), token: str = Depends(get_token),
                               jwt_repository: CredentialsRepository = Depends()) -> None:
    product = await repository.get_product_by_id(product_id, session)
    token_user_id = jwt_repository.valid_and_decode_token(token)
    if token_user_id == product.user_id:
        product = await repository.delete_product_by_id(product_id, session)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="В доступе отказано!")


@router.put("/{product_id}", status_code=status.HTTP_200_OK)  # обновление продукта по id
async def update_product_by_id(product_id: int, product: ProductUpdateSchema,
                               repository: Repository = Depends(),
                               session = Depends(get_async_session), token: str = Depends(get_token),
                               jwt_repository: CredentialsRepository = Depends()):
    product_update = await repository.get_product_by_id(product_id, session)
    token_user_id = jwt_repository.valid_and_decode_token(token)
    if token_user_id == product_update.user_id:
        await repository.update_product_by_id(product_id, product, session)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="В доступе отказано!")



@router.get("/", status_code=status.HTTP_200_OK)  # список всех продуктов
async def get_products(repository: Repository = Depends(),
                       session = Depends(get_async_session)) -> list[ProductReadSchema]:
    return await repository.get_products(session)


@router.get("/{product_id}", status_code=status.HTTP_200_OK)  # получить продукт по id
async def get_product_by_id(product_id: int, repository: Repository = Depends(),
                            session = Depends(get_async_session)) -> ProductReadSchema:
    return await repository.get_product_by_id(product_id, session)


