from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.category import Category


@dataclass
class Expense:
    user_id: UUID
    name: str
    price: float
    quantity: int = 1
    category: Category = None
    id: Optional[UUID] = None
    price_usd: Optional[float] = None

    @property
    def total_amount(self) -> float:
        return self.quantity * self.price

    def convert_usd(self, rate: float) -> None:
        self.price_usd = self.price / rate
