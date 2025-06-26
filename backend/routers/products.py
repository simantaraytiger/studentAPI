from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from backend.db import get_async_db
from backend.models import Product
from backend.schemas import ProductCreate, ProductResponse, ProductUpdate, ProductOut

router = APIRouter()


@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate, db: AsyncSession = Depends(get_async_db)
):
    new_product = Product(
        name=product.name, price=product.price, description=product.description
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return {
        "message": "Product created successfully",
        "data": jsonable_encoder(new_product),
    }


@router.get("/", response_model=ProductResponse)
async def get_all_products(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return {
        "message": "All products retrieved successfully",
        "data": jsonable_encoder(products),
    }


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "message": "Product retrieved successfully",
        "data": jsonable_encoder(product),
    }


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_data.name is not None:
        product.name = product_data.name  # type: ignore
    if product_data.price is not None:
        product.price = product_data.price  # type: ignore
    if product_data.description is not None:
        product.description = product_data.description  # type: ignore

    await db.commit()
    await db.refresh(product)
    return {
        "message": "Product updated successfully",
        "data": jsonable_encoder(product),
    }


@router.delete("/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()
    return {
        "message": "Product deleted successfully",
        "data": jsonable_encoder(product),
    }
