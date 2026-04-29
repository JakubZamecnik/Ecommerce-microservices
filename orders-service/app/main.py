from typing import Optional, List
from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
import time
import pika
import json
from app.config import settings
from pydantic import BaseModel, Field as PydanticField


# --- 1. MODEL ---
class OrderCreate(BaseModel):
    customer_id: int = PydanticField(gt=0)
    product_name: str = PydanticField(min_length=2, max_length=50)
    quantity: int = PydanticField(gt=0)

# 2. Model pro DATABÁZI (SQLModel)
class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int
    product_name: str
    quantity: int
    status: str = "PENDING"

# --- 2. DATABÁZE A KONFIGURACE ---
engine = create_engine(settings.database_url)

# --- 3. POMOCNÉ FUNKCE (RABBITMQ) ---
def publish_order_created(order: Order):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.rabbitmq_host))
        channel = connection.channel()
        
        # Vytvoříme ústřednu typu 'fanout'
        channel.exchange_declare(exchange='order_events', exchange_type='fanout')
        
        message = {
            "order_id": order.id,
            "product_name": order.product_name,
            "quantity": order.quantity
        }
        
        # Publikujeme do EXCHANGE, ne do fronty (routing_key je prázdný)
        channel.basic_publish(
            exchange='order_events',
            routing_key='',
            body=json.dumps(message)
        )
        connection.close()
        print(f" [📣] Objednávka {order.id} publikována přes Exchange!")
    except Exception as e:
        print(f" [!] Chyba RabbitMQ: {e}")


# --- 4. LIFESPAN (STARTUP LOGIKA) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Logika při startu: Čekání na DB a vytvoření tabulek
    for i in range(5):
        try:
            SQLModel.metadata.create_all(engine)
            print("Databáze úspěšně připojena!")
            break
        except Exception:
            print(f"Čekám na databázi... (pokus {i+1}/5)")
            time.sleep(2)
    yield
    # Zde můžeš dopsat logiku, co se má stát při vypnutí (např. uzavření spojení)

# --- 5. FASTAPI APLIKACE ---
app = FastAPI(title="Orders Service", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "online", "service": "Orders"}

@app.post("/orders/", response_model=Order)
def create_order(order_data: OrderCreate): # Používáme OrderCreate pro validaci
    with Session(engine) as session:
        # Převedeme validovaná data na databázový model
        db_order = Order.model_validate(order_data) 
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        
        publish_order_created(db_order)
        return db_order

@app.get("/orders/", response_model=List[Order])
def get_orders():
    with Session(engine) as session:
        return session.exec(select(Order)).all()
