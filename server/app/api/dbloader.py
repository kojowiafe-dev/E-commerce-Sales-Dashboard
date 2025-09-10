from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import OrderBase, OrderCreate, OrderResponse
from database import SessionDep, engine
from models.model import Order, Product, OrderItem
from datetime import datetime
import csv


async def load_csv_to_db(file_path: str):
    async with AsyncSession(engine) as session:
        with open(file_path, newline="", encoding="utf-8-sig") as csvfile:
            # utf-8-sig handles BOMs if present
            reader = csv.DictReader(csvfile)

            for row in reader:
                order_id_value = row.get("Order ID", "").strip()

                # 🔒 Skip header or bad rows
                if not order_id_value.isdigit():
                    print(f"⏩ Skipping invalid row: {row}")
                    continue

                # --- Product ---
                product_result = await session.execute(
                    select(Product).where(Product.name == row["Product"].strip())
                )
                product = product_result.scalars().first()
                if not product:
                    product = Product(
                        name=row["Product"].strip(),
                        price_each=float(row["Price Each"])
                    )
                    session.add(product)
                    await session.flush()

                # --- Order ---
                order_result = await session.execute(
                    select(Order).where(Order.order_id == int(order_id_value))
                )
                order = order_result.scalars().first()
                if not order:
                    order = Order(
                        order_id=int(order_id_value),
                        order_date=row["Order Date"].strip(),
                        purchase_address=row["Purchase Address"].strip()
                    )
                    session.add(order)
                    await session.flush()

                # --- OrderItem ---
                order_item = OrderItem(
                    order_id=order.order_id,
                    product_id=product.product_id,
                    quantity=int(row["Quantity Ordered"]),
                    price_each=float(row["Price Each"]),
                    line_total=float(row["Price Each"]) * int(row["Quantity Ordered"])
                )
                session.add(order_item)

            await session.commit()