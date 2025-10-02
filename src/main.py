from fastapi import FastAPI
from product.router import router as product_router
from user.router import router as user_router

app = FastAPI()
app.include_router(product_router)
app.include_router(user_router)