from fastapi import FastAPI
from routers.products.controller import router as products_router
from routers.users.controller import router as users_router
from routers.auth.controller import router as auth_router


def register_routes(app: FastAPI):
    app.include_router(products_router)
    app.include_router(auth_router)
    app.include_router(users_router)