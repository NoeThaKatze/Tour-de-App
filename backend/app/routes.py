from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .models import Member as MemberModel
from .models import Product as ProductModel
from .models import Team as TeamModel
from .schemas import Product, ProductCreate

router = APIRouter(prefix="/api/product", tags=["products"])

DbSession = Annotated[Session, Depends(get_db)]

v1_router = APIRouter(prefix="/api/v1", tags=["health"])


@v1_router.get("/health")
def health():
    return {"status": "ok"}


@v1_router.get("/team")
def get_team(db: DbSession):
    team = db.scalars(select(TeamModel)).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team does not exist")

    members = db.scalars(
        select(MemberModel).where(MemberModel.team_id == team.id).order_by(MemberModel.id)
    ).all()
    return {"name": team.name, "members": [m.name for m in members]}


@router.get("", response_model=list[Product])
def list_products(db: DbSession):
    return db.scalars(select(ProductModel).order_by(ProductModel.id)).all()


@router.post("", response_model=Product)
def create_product(data: ProductCreate, db: DbSession):
    product = ProductModel(name=data.name, cost=data.cost)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, data: ProductCreate, db: DbSession):
    product = db.get(ProductModel, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product does not exist")

    product.name = data.name
    product.cost = data.cost
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: DbSession):
    product = db.get(ProductModel, product_id)
    if product is not None:
        db.delete(product)
        db.commit()

    return {"message": "Product was deleted permanently from DB."}
