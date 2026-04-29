from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int
    item_name: str
    quantity: int
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)
