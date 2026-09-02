from pydantic import BaseModel, computed_field
from datetime import datetime


class Product(BaseModel):
    """A single product listing from a store."""
    id: str
    name: str
    price: float
    store: str
    in_stock: bool
    shipping_cost: float = 0.0
    last_updated: datetime

    @computed_field
    @property
    def total_cost(self) -> float:
        return self.price + self.shipping_cost