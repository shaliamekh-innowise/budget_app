from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.domain.category import Category


@dataclass
class Expense:
    user_id: UUID
    name: str
    category: Category
    price: float
    quantity: int = 1
    id: Optional[UUID] = None
    price_usd: Optional[float] = None

    @property
    def total_amount(self) -> float:
        return self.quantity * self.price

    def convert_usd(self, rate: float) -> None:
        self.price_usd = self.price / rate
