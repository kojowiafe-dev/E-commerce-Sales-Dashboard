from fastapi import APIRouter
from ...routers.products import schemas, service
from ...database.core import SessionDep


router = APIRouter(
    prefix="/products", 
    tags=["Products"]
)


@router.get("/top-products")
async def get_top_products(session: SessionDep, limit: int = 10):
    result = await service.get_top_products(session, limit)
    return result

@router.get("/total_products")
async def get_number_of_products(session: SessionDep):
    result = await service.get_number_of_products(session)
    return result


@router.get("/{product_name}")
async def get_product_name(product_name: str, session: SessionDep):
    product = await service.get_product_name(product_name, session)
    return product



@router.get("/{product_id}", response_model=schemas.ProductResponse)
async def get_product(product_id: int, session: SessionDep):
    product = await service.get_product(product_id, session)
    return product



@router.get("/", response_model=schemas.PaginatedProducts)
async def get_products(
    session: SessionDep,
    page: int = 1,
    limit: int = 10,
    search: str = None
):
    return await service.get_products(session, page, limit, search)

