from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from schemas import OrderBase, OrderCreate, OrderResponse
from database import SessionDep
from models.model import Order
from datetime import datetime


router = APIRouter(
    prefix="/orders", 
    tags=["Orders"]
)


# @router.get()