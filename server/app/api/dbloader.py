from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from schemas import OrderBase, OrderCreate, OrderResponse
from database import SessionDep, engine
from models.model import Order, Product, OrderItem
from datetime import datetime
import csv


def load_csv_to_db(file_path: str):
    with Session(engine) as session:
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
                product = session.exec(
                    select(Product).where(Product.name == row["Product"].strip())
                ).first()
                if not product:
                    product = Product(
                        name=row["Product"].strip(),
                        price_each=float(row["Price Each"])
                    )
                    session.add(product)
                    session.commit()
                    session.refresh(product)

                # --- Order ---
                order = session.exec(
                    select(Order).where(Order.order_id == int(order_id_value))
                ).first()
                if not order:
                    order = Order(
                        order_id=int(order_id_value),
                        order_date=row["Order Date"].strip(),
                        purchase_address=row["Purchase Address"].strip()
                    )
                    session.add(order)
                    session.commit()
                    session.refresh(order)

                # --- OrderItem ---
                order_item = OrderItem(
                    order_id=order.order_id,
                    product_id=product.product_id,
                    quantity=int(row["Quantity Ordered"]),
                    price_each=float(row["Price Each"]),
                    line_total=float(row["Price Each"]) * int(row["Quantity Ordered"])
                )
                session.add(order_item)

            session.commit()
